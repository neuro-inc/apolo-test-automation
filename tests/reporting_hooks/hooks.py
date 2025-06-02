"""
Pytest configuration hooks and logging setup for automation tests.

This module initializes logging, manages report directories, handles Allure report generation,
and defines BDD-related hooks for structured logging and exception handling. It also integrates
Playwright for capturing screenshots on test failures.

Key functionalities:
- Logging configuration for test runs.
- Allure report directory setup and generation.
- Handling of exceptions with detailed, human-readable messages.
- Playwright-based screenshot capture on test step failures.
- Dynamic Allure suite naming based on feature names.
"""

import os
import shutil
import logging
import subprocess
import pytest
import allure
from datetime import datetime
from tests.utils.exception_handling.exception_manager import ExceptionManager

# Paths for reports and logs
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE_REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")
LOGS_DIR = os.path.join(BASE_REPORT_DIR, "logs")
SCREENSHOTS_DIR = os.path.join(BASE_REPORT_DIR, "screenshots")
ALLURE_RESULTS_DIR = os.path.join(BASE_REPORT_DIR, "allure-results")
ALLURE_REPORT_DIR = os.path.join(BASE_REPORT_DIR, "allure-report")
LOG_FILE_PATH = os.path.join(LOGS_DIR, "test_run.log")

# Ensure clean start
if os.path.exists(BASE_REPORT_DIR):
    shutil.rmtree(BASE_REPORT_DIR)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)

# Logging configuration
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

if not root_logger.hasHandlers():
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

exception_manager = ExceptionManager(logger=root_logger)
_logged_features = set()

@pytest.hookimpl
def pytest_configure(config):
    """
    Pytest hook to configure test run settings.

    - Sets the Allure results directory for storing test results.
    """
    config.option.allure_report_dir = ALLURE_RESULTS_DIR
    root_logger.info(f"📂 Allure results directory set to: {ALLURE_RESULTS_DIR}")

@pytest.hookimpl
def pytest_sessionstart():
    """
    Pytest hook triggered at the start of the test session.

    - Logs session start information and ensures log directories are created.
    """
    root_logger.info(f"📂 Logs directory ensured at startup: {LOGS_DIR}")
    root_logger.info(f"✅ Pytest session started.")

@pytest.hookimpl
def pytest_sessionfinish():
    """
    Pytest hook triggered at the end of the test session.

    - Generates an Allure report if test results are available.
    """
    root_logger.info("✅ Pytest session finished.")
    if os.listdir(ALLURE_RESULTS_DIR):
        root_logger.info("📊 Generating Allure HTML report...")
        try:
            subprocess.run(
                ["allure", "generate", ALLURE_RESULTS_DIR, "-o", ALLURE_REPORT_DIR, "--clean"],
                check=True
            )
            report_path = os.path.abspath(os.path.join(ALLURE_REPORT_DIR, "index.html"))
            root_logger.info(f"✅ Allure report generated at: {report_path}")
        except subprocess.CalledProcessError as e:
            root_logger.error(f"❌ Failed to generate Allure report: {e}")
    else:
        root_logger.warning("⚠️ No Allure results found, skipping report generation.")

def pytest_bdd_before_scenario(feature, scenario):
    """
    Pytest-BDD hook executed before each scenario.

    - Logs feature and scenario start information.
    - Sets dynamic Allure suite name based on the feature, simplified to the last part of the module path.
    """
    feature_name = feature.name
    scenario_name = scenario.name

    allure.dynamic.suite(feature_name)

    if feature_name not in _logged_features:
        root_logger.info(f"\n\n📘 FEATURE: {feature_name}\n{'='*60}")
        _logged_features.add(feature_name)

    root_logger.info(f"\n▶️ START SCENARIO: {scenario_name}\n{'='*60}")

def pytest_bdd_before_step(step):
    """
    Pytest-BDD hook executed before each step.

    - Logs the step keyword and name.
    """
    step_text = f"{step.keyword} {step.name}"
    root_logger.info(f"➡️ STEP: {step_text}")

def pytest_bdd_step_error(request, feature, scenario, exception):
    """
    Pytest-BDD hook executed when a step fails.

    - Handles exceptions using a custom exception manager.
    - Captures and logs a screenshot if Playwright is used.
    - Attaches error details and screenshots to the Allure report.
    - Raises an AssertionError with the readable exception message.
    """
    page = getattr(request.node, "page", None)
    readable_message = exception_manager.handle(
        exception,
        context=f"{feature.name}/{scenario.name}",
        page=page
    )
    root_logger.error(f"❌ STEP FAILED\n{readable_message}")

    is_playwright_error = page is not None

    if is_playwright_error:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_filename = f"{scenario.name}_{timestamp}.png".replace(" ", "_")
            screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_filename)
            page.screenshot(path=screenshot_path, full_page=True)
            root_logger.info(f"📸 Screenshot saved: {screenshot_path}")

            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name=f"{scenario.name}_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            root_logger.warning(f"⚠️ Failed to capture screenshot: {e}")

    allure.attach(
        readable_message,
        name="Exception Details",
        attachment_type=allure.attachment_type.TEXT
    )

    raise AssertionError(readable_message)

def pytest_bdd_after_scenario():
    """
    Pytest-BDD hook executed after each scenario.

    - Logs a separator line to indicate scenario completion.
    """
    root_logger.info(f"\n{'=' * 60}")
