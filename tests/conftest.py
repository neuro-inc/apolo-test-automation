import logging
import os
import subprocess
from collections import defaultdict

import pytest
from _pytest.config import Config
from _pytest.reports import TestReport

# --- Paths and Directories ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")
LOGS_DIR = os.path.join(BASE_REPORT_DIR, "logs")
SCREENSHOTS_DIR = os.path.join(BASE_REPORT_DIR, "screenshots")
ALLURE_RESULTS_DIR = os.path.join(BASE_REPORT_DIR, "allure-results")
ALLURE_REPORT_DIR = os.path.join(BASE_REPORT_DIR, "allure-report")

# --- Create necessary directories ---
for path in [LOGS_DIR, SCREENSHOTS_DIR, ALLURE_RESULTS_DIR, ALLURE_REPORT_DIR]:
    os.makedirs(path, exist_ok=True)

# --- Clean old report files ---
for root, dirs, files in os.walk(BASE_REPORT_DIR):
    for f in files:
        os.remove(os.path.join(root, f))

# --- Per-worker log file ---
worker_id = os.getenv("PYTEST_XDIST_WORKER", "main")
LOG_FILE_PATH = os.path.join(LOGS_DIR, f"test_run_{worker_id}.log")

# --- Logging Configuration ---
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

while root_logger.hasHandlers():
    root_logger.removeHandler(root_logger.handlers[0])

file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

logger = logging.getLogger("[🛠️TEST CONFIG]")

CONFIG_PATH = os.path.join(PROJECT_ROOT, "tests", "test_data.yaml")

_SUITE_OUTCOMES: dict[str, dict[str, int]] = defaultdict(
    lambda: {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "rerun": 0,
    }
)


def pytest_configure(config: Config) -> None:
    config.option.allure_report_dir = ALLURE_RESULTS_DIR
    config.option.allure_report = ALLURE_RESULTS_DIR
    config.option.alluredir = ALLURE_RESULTS_DIR


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
        logger.info(f"🔁 Rerun attempt for: {report.nodeid}")
        return

    _SUITE_OUTCOMES[suite_name][report.outcome] += 1


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    logger.info("=" * 60)
    passed = 0
    failed = 0
    skipped = 0
    rerun = 0

    for suite, results in _SUITE_OUTCOMES.items():
        passed += results["passed"]
        failed += results["failed"]
        skipped += results["skipped"]
        rerun += results["rerun"]

    summary_path = os.path.join(LOGS_DIR, "summary.log")
    try:
        with open(summary_path, "w") as f:
            if exitstatus == 11:
                f.write("Test setup failed. Cannot signup user for tests...\n")
            cleanup_note = getattr(session, "cleanup_warning", None)
            if cleanup_note:
                f.write(cleanup_note)

            f.write(
                f"    PASSED: {passed}   FAILED: {failed}   SKIPPED: {skipped}   RERUNS: {rerun}\n"
            )
            logger.info(f"📝 Summary written to: {summary_path}")
    except Exception as e:
        logger.error(f"❌ Failed to write summary.log: {e}")

    # --- Merge per-worker logs into test_run.log ---
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
