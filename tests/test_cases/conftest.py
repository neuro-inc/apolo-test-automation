from __future__ import annotations

from collections.abc import AsyncGenerator
import logging
import os

import pytest
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from tests.components.ui.page_manager import PageManager
from tests.utils.api_helper import APIHelper
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.schema_data import SchemaData
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager

logger = logging.getLogger("[🛠️TEST CONFIG]")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "tests", "test_data.yaml")


@pytest.fixture(scope="function")
async def browser() -> AsyncGenerator[Browser, None]:
    async with async_playwright() as p:
        logger.info("Launching browser")
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        yield browser
        await browser.close()
        logger.info("Browser closed")


@pytest.fixture(scope="function")
async def page_manager(
    browser: Browser,
    test_config: ConfigManager,
    data_manager: DataManager,
    request: pytest.FixtureRequest,
) -> AsyncGenerator[PageManager, None]:
    context: BrowserContext = await browser.new_context(no_viewport=True)
    page: Page = await context.new_page()
    logger.info(f"Navigating to: {test_config.base_url}")
    await page.goto(test_config.base_url)

    test_config.context = context
    page_manager = PageManager(page, test_config.auth.email, test_config.auth.username)
    request.node.page = page
    yield page_manager
    await context.close()
    logger.info("Browser context closed")


@pytest.fixture
def test_config() -> ConfigManager:
    logger.info("Loading test configuration")
    return ConfigManager(CONFIG_PATH)


@pytest.fixture
def data_manager() -> DataManager:
    logger.info("Creating data manager")
    return DataManager()


@pytest.fixture
def schema_data() -> SchemaData:
    logger.info("Creating schema data manager")
    return SchemaData("components/json_schema/saved_schemas")


@pytest.fixture
async def api_helper(test_config: ConfigManager) -> AsyncGenerator[APIHelper, None]:
    logger.info("Creating API helper")
    helper = await APIHelper(config=test_config).init()
    yield helper
    await helper._close()


@pytest.fixture
def apolo_cli() -> ApoloCLI:
    logger.info("Creating Apolo CLI instance")
    return ApoloCLI()


@pytest.fixture
def users_manager() -> UsersManager:
    logger.info("Creating users manager")
    return UsersManager()


@pytest.fixture(autouse=True)
async def clean_up(
    test_config: ConfigManager,
    data_manager: DataManager,
    apolo_cli: ApoloCLI,
) -> AsyncGenerator[None, None]:
    yield
    logger.info("Running post-test cleanup")

    organizations = data_manager.get_all_organizations()
    logger.info(f"Cleaning up {len(organizations)} organizations")
    if organizations:
        logger.info("Logging in to Apolo CLI for cleanup")
        token = test_config.token
        url = test_config.cli_login_url
        await apolo_cli.login_with_token(token, url)
        for organization in organizations:
            await apolo_cli.remove_organization(organization.org_name)
            logger.info(f"Removed organization: {organization.org_name}")
