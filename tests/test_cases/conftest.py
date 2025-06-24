from __future__ import annotations
from collections.abc import AsyncGenerator
from collections.abc import Callable
from collections.abc import Coroutine

import logging
import os
from typing import Any

import allure
import pytest
from allure_commons.types import AttachmentType
from playwright.async_api import async_playwright, Browser

from tests.components.ui.page_manager import PageManager
from tests.test_cases.steps.common_steps.ui_steps.ui_common_steps import UICommonSteps
from tests.utils.api_helper import APIHelper
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.exception_handling.exception_manager import ExceptionManager
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.schema_data import SchemaData
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager, UserData

logger = logging.getLogger("[🔧TEST CONFIG]")
exception_manager = ExceptionManager(logger=logger)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "tests", "test_data.yaml")

_default_user: UserData | None = None


@pytest.fixture(scope="function", autouse=True)
async def signup_default_user(
    test_config: ConfigManager,
    data_manager: DataManager,
    users_manager: UsersManager,
    api_helper: APIHelper,
    request: pytest.FixtureRequest,
) -> None:
    """
    Signs up and verifies a default user before each test.
    - Reuses cached user if already available.
    - Performs signup and email verification via UI steps.
    - Aborts the test session if signup fails.
    - Ensures browser context is cleaned up after execution.
    """
    global _default_user
    if _default_user:
        users_manager.default_user = _default_user
        return
    logger.info("Signup default user...")
    pm = await _create_page_manager(test_config, request)

    ui_common_steps = UICommonSteps(
        pm, test_config, data_manager, users_manager, api_helper
    )
    try:
        await ui_common_steps.ui_signup_new_user_ver_link()
    except Exception as e:
        logger.error(f"❌ Failed to sign up default user: {e}")
        pytest.exit(
            "🚫 Aborting test session: default user signup failed.", returncode=11
        )
    else:
        _default_user = users_manager.default_user
    finally:
        await pm._cleanup()  # type: ignore[attr-defined]


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
    created: list[PageManager] = []

    async def _factory() -> PageManager:
        pm = await _create_page_manager(test_config, request)
        created.append(pm)
        return pm

    try:
        yield _factory
    finally:
        for pm in reversed(created):
            await pm._cleanup()  # type: ignore[attr-defined]


@pytest.fixture(scope="function")
def test_config() -> ConfigManager:
    logger.info("Loading test configuration")
    return ConfigManager(CONFIG_PATH)


@pytest.fixture(scope="function")
def data_manager() -> DataManager:
    logger.info("Creating data manager")
    return DataManager()


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
    test_config: ConfigManager,
    data_manager: DataManager,
    apolo_cli: ApoloCLI,
    request: pytest.FixtureRequest,
) -> AsyncGenerator[None, None]:
    """
    Post-test cleanup:
    - logs in to Apolo CLI,
    - removes all organisations recorded in the DataManager,
    - logs any cleanup errors without failing the test run.
    """
    yield

    with allure.step("Post-test cleanup"):
        try:
            organisations = data_manager.get_all_organizations()
            logger.info("Cleaning up %d organisations", len(organisations))

            if not organisations:
                allure.attach(
                    "No organisations to clean up.",
                    name="Cleanup note",
                    attachment_type=AttachmentType.TEXT,
                )
                return

            with allure.step("CLI login for cleanup"):
                await apolo_cli.login_with_token(
                    test_config.token,
                    test_config.cli_login_url,
                )

            for org in organisations:
                with allure.step(f"Delete organisation: {org.org_name}"):
                    await apolo_cli.remove_organization(org.org_name)
                    data_manager.remove_organization(org.org_name)
                    logger.info("Removed organisation: %s", org.org_name)

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
            global _default_user
            logger.warning("Need to setup new user due to cleanup issues...")
            _default_user = None


async def _start_browser() -> Browser:
    """
    Launches a headless Chromium browser with CI-safe arguments.
    """
    playwright = await async_playwright().start()

    logger.info("Starting browser in a headless mode...")
    browser = await playwright.chromium.launch(
        headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"]
    )

    return browser


async def _create_page_manager(
    test_config: ConfigManager, request: pytest.FixtureRequest
) -> PageManager:
    browser = await _start_browser()
    logger.info("Initializing new browser context")
    context = await browser.new_context(no_viewport=True)
    page = await context.new_page()

    # Attach HTTP response logging
    page.on("response", _log_failed_requests)

    logger.info(f"Navigating to: {test_config.base_url}")
    await page.goto(test_config.base_url)
    await page.wait_for_load_state("networkidle", timeout=5000)

    test_config.context = context
    request.node.page = page
    pm = PageManager(page)

    async def _cleanup() -> None:
        await context.close()
        logger.info("Browser context closed")
        await browser.close()
        logger.info("Browser closed")

    pm._cleanup = _cleanup  # type: ignore[attr-defined]
    return pm


async def _log_failed_requests(response: Any) -> None:
    """
    Logs HTTP responses with 4xx and 5xx status codes.
    """
    status = response.status
    if status >= 400:
        url = response.url
        try:
            body = await response.text()
        except Exception:
            body = "<unavailable>"
        logger.warning(f"[HTTP {status}] {url}\nBody: {body[:500]}")
        allure.attach(
            f"URL: {url}\nStatus: {status}\n\nResponse body:\n{body[:1000]}",
            name=f"HTTP {status} - {os.path.basename(url)}",
            attachment_type=AttachmentType.TEXT,
        )
