from __future__ import annotations

from collections.abc import AsyncGenerator
from collections.abc import Callable
from collections.abc import Coroutine

import logging
import os
from typing import Any
from urllib.parse import urlparse

import allure
import pytest
from allure_commons.types import AttachmentType
from playwright.async_api import async_playwright, Browser, BrowserContext

from tests.components.ui.page_manager import PageManager
from tests.utils.api_helper import APIHelper
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.exception_handling.exception_manager import ExceptionManager
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.schema_data import SchemaData
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager

logger = logging.getLogger("[🔧TEST CONFIG]")
exception_manager = ExceptionManager(logger=logger)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "tests", "test_data.yaml")

STORAGE_OBJECTS_PATH = os.path.join(PROJECT_ROOT, "storage_objects")
GENERATED_DATA_PATH = os.path.join(STORAGE_OBJECTS_PATH, "generated_objects")
DOWNLOAD_PATH = os.path.join(STORAGE_OBJECTS_PATH, "downloads")

_browser_context_pairs: list[tuple[Browser, BrowserContext]] = []


@pytest.fixture(scope="session", autouse=True)
def ensure_storage_directories() -> None:
    for path in (STORAGE_OBJECTS_PATH, GENERATED_DATA_PATH, DOWNLOAD_PATH):
        os.makedirs(path, exist_ok=True)


@pytest.fixture(scope="function")
async def page_manager(
    test_config: ConfigManager,
    request: pytest.FixtureRequest,
) -> PageManager:
    pm = await _create_page_manager(test_config, request)
    return pm


@pytest.fixture(scope="function")
async def add_page_manager(
    test_config: ConfigManager,
    request: pytest.FixtureRequest,
) -> AsyncGenerator[Callable[[], Coroutine[Any, Any, PageManager]], Any]:
    """
    Factory fixture.
    Call it inside a test as::

        pm1 = await add_page_manager()
        pm2 = await add_page_manager()

    All opened browsers/contexts are closed automatically after the test.
    """

    async def _factory() -> PageManager:
        pm = await _create_page_manager(test_config, request)
        return pm

    yield _factory


@pytest.fixture(scope="function")
def test_config() -> ConfigManager:
    logger.info("Loading test configuration")
    return ConfigManager(CONFIG_PATH)


@pytest.fixture(scope="function")
def data_manager() -> DataManager:
    logger.info("Creating data manager")
    return DataManager(gen_obj_path=GENERATED_DATA_PATH, download_path=DOWNLOAD_PATH)


@pytest.fixture
def schema_data() -> SchemaData:
    logger.info("Creating schema data manager")
    return SchemaData("components/json_schema/saved_schemas")


@pytest.fixture(scope="function")
async def api_helper(test_config: ConfigManager) -> AsyncGenerator[APIHelper, None]:
    logger.info("Creating API helper")
    helper = await APIHelper(config=test_config).init()
    yield helper
    await helper._close()


@pytest.fixture(scope="function")
def apolo_cli() -> ApoloCLI:
    logger.info("Creating Apolo CLI instance")
    return ApoloCLI()


@pytest.fixture(scope="function")
def users_manager() -> UsersManager:
    logger.info("Creating users manager")
    return UsersManager()


@pytest.fixture(autouse=True)
async def clean_up(
    request: pytest.FixtureRequest,
) -> AsyncGenerator[None, None]:
    """
    Post-test cleanup:
    - closes all browser sessions,
    - logs any cleanup errors without failing the test run.
    """
    yield

    with allure.step("Post-test cleanup"):
        try:
            await _cleanup_browsers()

        except Exception as exc:
            # Capture details but DO NOT fail the test
            if not hasattr(request.session, "cleanup_warning"):
                request.session.cleanup_warning = (  # type: ignore[attr-defined]
                    "Test cleanup failed. See log file for details!\n"
                )
            formatted_msg = exception_manager.handle(exc, context="Post-test cleanup")
            logger.exception("Post-test cleanup failed: %s", formatted_msg)

            allure.attach(
                formatted_msg,
                name="Cleanup exception",
                attachment_type=AttachmentType.TEXT,
            )

            logger.warning(f"Post-test cleanup failed: {formatted_msg}", RuntimeWarning)


async def _cleanup_browsers() -> None:
    logger.info("Closing all browser sessions")
    for browser, context in _browser_context_pairs:
        try:
            await context.close()
            logger.info("Closed context")
        except Exception as e:
            logger.warning(f"Failed to close context: {e}")

        try:
            if browser.is_connected():
                await browser.close()
                logger.info("Closed browser")
        except Exception as e:
            logger.warning(f"Failed to close browser: {e}")

    _browser_context_pairs.clear()
    logger.info("Closed all browser sessions")


async def _start_browser() -> Browser:
    """
    Launches a headless Chromium browser with CI-safe arguments.
    """
    playwright = await async_playwright().start()

    logger.info("Starting browser in a headless mode...")
    browser = await playwright.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage", "--window-size=1920,1080"],
    )

    return browser


async def _create_page_manager(
    test_config: ConfigManager, request: pytest.FixtureRequest
) -> PageManager:
    browser = await _start_browser()
    logger.info("Initializing new browser context")
    context = await browser.new_context(no_viewport=True, accept_downloads=True)
    _browser_context_pairs.append((browser, context))
    page = await context.new_page()

    # Attach HTTP response logging
    page.on("response", lambda response: _log_failed_requests(test_config, response))

    logger.info(f"Navigating to: {test_config.base_url}")
    await page.goto(test_config.base_url)
    await page.wait_for_load_state("networkidle", timeout=5000)

    test_config.context = context
    request.node.page = page
    pm = PageManager(page)
    return pm


async def _log_failed_requests(test_config: ConfigManager, response: Any) -> None:
    """
    Logs HTTP responses within product hostname, including:
    - Request method and URL
    - Request body (if available)
    - Response body (truncated)
    """
    status = response.status
    request = response.request
    url = request.url

    cli_login_url = test_config.cli_login_url
    product_hostname = urlparse(cli_login_url).hostname

    # Parse URL and check hostname
    parsed_url = urlparse(url)
    if parsed_url.hostname != product_hostname:
        return

    if status >= 200:
        method = request.method

        try:
            request_body = await request.post_data()
        except Exception:
            request_body = "<not available>"

        try:
            response_body = await response.text()
        except Exception:
            response_body = "<unavailable>"

        log_msg = (
            f"[HTTP {status}] {method} {url}\n"
            f"Request Body:\n{request_body}\n"
            f"Response Body (first 1000 chars):\n{response_body[:1000]}"
        )

        logger.warning(log_msg)
        allure.attach(
            log_msg,
            name=f"HTTP {status} - {method} {os.path.basename(url)}",
            attachment_type=AttachmentType.TEXT,
        )
