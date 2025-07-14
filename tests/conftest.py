import logging
import os
import subprocess
import time
from collections import defaultdict

import allure
import pytest
from _pytest.config import Config
from _pytest.reports import TestReport
from allure_commons.types import AttachmentType

# --- Paths and Directories ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")
LOGS_DIR = os.path.join(BASE_REPORT_DIR, "logs")
SCREENSHOTS_DIR = os.path.join(BASE_REPORT_DIR, "screenshots")
ALLURE_RESULTS_DIR = os.path.join(BASE_REPORT_DIR, "allure-results")
ALLURE_REPORT_DIR = os.path.join(BASE_REPORT_DIR, "allure-report")
CONFIG_PATH = os.path.join(PROJECT_ROOT, "tests", "test_data.yaml")

# --- Create necessary directories (only once, master process) ---
if os.getenv("PYTEST_XDIST_WORKER") in [None, "main"]:
    for path in [LOGS_DIR, SCREENSHOTS_DIR, ALLURE_RESULTS_DIR, ALLURE_REPORT_DIR]:
        os.makedirs(path, exist_ok=True)
        # Clean old report files (except history)
        for root, dirs, files in os.walk(BASE_REPORT_DIR):
            for f in files:
                full_path = os.path.join(root, f)
                # Skip deleting history
                if "allure-results/history" in full_path.replace("\\", "/"):
                    continue
                os.remove(full_path)

# --- Suite-level test outcome tracking ---
_SUITE_OUTCOMES: dict[str, dict[str, int]] = defaultdict(
    lambda: {"passed": 0, "failed": 0, "skipped": 0, "rerun": 0, "xfail": 0}
)


def pytest_configure(config: Config) -> None:
    # Allure results directory setup
    config.option.allure_report_dir = ALLURE_RESULTS_DIR
    config.option.allure_report = ALLURE_RESULTS_DIR
    config.option.alluredir = ALLURE_RESULTS_DIR

    # Per-worker logging setup
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "main")
    log_path = os.path.join(LOGS_DIR, f"test_run_{worker_id}.log")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    while root_logger.hasHandlers():
        root_logger.removeHandler(root_logger.handlers[0])

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Optional: also log to console
    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        root_logger.addHandler(stream_handler)

    logging.getLogger().info(f"📁 Logging initialized for worker: {worker_id}")


@pytest.hookimpl
def pytest_runtest_logreport(report: TestReport) -> None:
    if report.when != "call":
        return

    suite = getattr(getattr(report, "item", None), "cls", None)
    suite_name = getattr(
        suite, "__suite_name__", suite.__name__ if suite else "unknown"
    )

    if getattr(report, "rerun", False):
        _SUITE_OUTCOMES[suite_name]["rerun"] += 1

    if report.passed:
        _SUITE_OUTCOMES[suite_name]["passed"] += 1
    elif report.failed:
        _SUITE_OUTCOMES[suite_name]["failed"] += 1
    elif report.skipped:
        if hasattr(report, "wasxfail") and report.wasxfail:
            _SUITE_OUTCOMES[suite_name]["xfail"] += 1
        else:
            _SUITE_OUTCOMES[suite_name]["skipped"] += 1


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    logger = logging.getLogger()
    logger.info("=" * 60)

    passed = failed = skipped = rerun = xfail = 0
    for suite, results in _SUITE_OUTCOMES.items():
        passed += results["passed"]
        failed += results["failed"]
        skipped += results["skipped"]
        rerun += results["rerun"]
        xfail += results["xfail"]

    summary_path = os.path.join(LOGS_DIR, "summary.log")
    try:
        with open(summary_path, "w") as f:
            if exitstatus == 11:
                f.write("Test setup failed. Cannot signup user for tests...\n")
            cleanup_note = getattr(session, "cleanup_warning", None)
            if cleanup_note:
                f.write(cleanup_note)
            f.write(
                f"    PASSED: {passed}   FAILED: {failed}   SKIPPED: {skipped}   XFAIL: {xfail}   RERUNS: {rerun}\n"
            )
        logger.info(f"📝 Summary written to: {summary_path}")
    except Exception as e:
        logger.error(f"❌ Failed to write summary.log: {e}")

    # --- Merge per-worker logs ---
    merged_log_path = os.path.join(LOGS_DIR, "test_run.log")
    try:
        with open(merged_log_path, "w") as outfile:
            for fname in sorted(os.listdir(LOGS_DIR)):
                if fname.startswith("test_run_") and fname.endswith(".log"):
                    path = os.path.join(LOGS_DIR, fname)
                    with open(path) as infile:
                        outfile.write(f"--- {fname} ---\n")
                        outfile.write(infile.read())
                        outfile.write("\n")
        logger.info(f"📦 Merged logs written to: {merged_log_path}")
    except Exception as e:
        logger.error(f"❌ Failed to merge logs: {e}")

    _attach_slowest_steps_to_allure()

    # --- Generate Allure report ---
    logger.info("📦 Generating Allure report...")
    try:
        subprocess.run(
            [
                "allure",
                "generate",
                ALLURE_RESULTS_DIR,
                "-o",
                ALLURE_REPORT_DIR,
                "--clean",
            ],
            check=True,
        )
        logger.info(f"✅ Allure report generated at: {ALLURE_REPORT_DIR}")
    except Exception as e:
        logger.error(f"❌ Failed to generate Allure report: {e}")


@pytest.fixture(scope="session", autouse=True)
def delay_worker_start() -> None:
    """
    Sync delay per xdist worker (safe for session scope).
    """
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "main")
    try:
        index = int(worker_id.replace("gw", ""))
    except ValueError:
        index = 0

    delay = 15 * index
    if delay > 0:
        logging.getLogger().info(f"[{worker_id}] ⏳ Delaying test start by {delay}s")
        time.sleep(delay)


def _attach_slowest_steps_to_allure() -> None:
    path = os.path.join(LOGS_DIR, "step_durations.log")
    if not os.path.exists(path):
        return

    try:
        with open(path) as f:
            lines = sorted(
                (line.strip() for line in f if " - " in line),
                key=lambda line: float(line.split(" - ")[-1][:-1]),
                reverse=True,
            )

        top_steps = "\n".join(lines[:5])
        allure.attach(
            top_steps,
            name="🐢 Top 5 Slowest Steps",
            attachment_type=AttachmentType.TEXT,
        )
    except Exception as e:
        logging.getLogger().warning(f"Could not attach slowest steps: {e}")
