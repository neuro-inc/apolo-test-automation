import logging
import os
import subprocess
from collections import defaultdict

import pytest

# --- Paths and Directories ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")
LOGS_DIR = os.path.join(BASE_REPORT_DIR, "logs")
SCREENSHOTS_DIR = os.path.join(BASE_REPORT_DIR, "screenshots")
ALLURE_RESULTS_DIR = os.path.join(BASE_REPORT_DIR, "allure-results")
ALLURE_REPORT_DIR = os.path.join(BASE_REPORT_DIR, "allure-report")

LOG_FILE_PATH = os.path.join(LOGS_DIR, "test_run.log")

# --- Prepare clean reporting environment ---
for path in [LOGS_DIR, SCREENSHOTS_DIR, ALLURE_RESULTS_DIR, ALLURE_REPORT_DIR]:
    os.makedirs(path, exist_ok=True)

# Remove previous reports but preserve folder structure
if os.path.exists(BASE_REPORT_DIR):
    for root, dirs, files in os.walk(BASE_REPORT_DIR):
        for f in files:
            os.remove(os.path.join(root, f))

# --- Logging Configuration ---
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Remove existing handlers to avoid duplicates
while root_logger.hasHandlers():
    root_logger.removeHandler(root_logger.handlers[0])

file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

logger = logging.getLogger("[🛠️TEST CONFIG]")

# --- Configuration ---
CONFIG_PATH = os.path.join(PROJECT_ROOT, "tests", "test_data.yaml")

# --- Test Summary Tracking ---
_SUITE_OUTCOMES = defaultdict(lambda: {"passed": 0, "failed": 0, "skipped": 0})


def pytest_configure(config):
    config.option.allure_report_dir = ALLURE_RESULTS_DIR
    config.option.allure_report = ALLURE_RESULTS_DIR  # Compatibility with some plugins
    config.option.alluredir = ALLURE_RESULTS_DIR  # ← main one used by allure-pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Track test outcome per suite.
    """
    outcome = yield
    report = outcome.get_result()

    if call.when == "call":
        cls = getattr(item, "cls", None)
        if cls:
            suite = getattr(cls, "__suite_name__", cls.__name__)
            _SUITE_OUTCOMES[suite][report.outcome] += 1


def pytest_sessionfinish(session, exitstatus):
    """
    Final test summary and Allure report generation.
    """
    logger.info("=" * 60)
    passed = failed = skipped = 0
    logger.info("📊 TEST SUITE SUMMARY")
    for suite, results in _SUITE_OUTCOMES.items():
        logger.info(f"📁 {suite}")
        logger.info(f"  ✅ Passed: {results['passed']}")
        passed += results["passed"]
        logger.info(f"  ❌ Failed: {results['failed']}")
        failed += results["failed"]
        logger.info(f"  ⏭️ Skipped: {results['skipped']}")
        skipped += results["skipped"]
        logger.info("-" * 60)
    logger.info("=" * 60)
    logger.info("📊 TOTAL TEST CASES SUMMARY:")
    logger.info(f"  ✅ Passed: {passed}")
    logger.info(f"  ❌ Failed: {failed}")
    logger.info(f"  ⏭️ Skipped: {skipped}")
    logger.info("=" * 60)

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
