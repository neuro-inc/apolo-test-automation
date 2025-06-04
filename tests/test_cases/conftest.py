import logging
import os

import pytest
from playwright.async_api import async_playwright

from tests.components.ui.page_manager import PageManager
from tests.utils.api_helper import APIHelper
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.schema_data import SchemaData
from tests.utils.test_data_management.test_data import DataManager

logger = logging.getLogger("[🛠️TEST CONFIG]")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "tests", "test_data.yaml")

@pytest.fixture(scope="function")
async def browser():
    async with async_playwright() as p:
        logger.info("Launching browser")
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        yield browser
        await browser.close()
        logger.info("Browser closed")

@pytest.fixture(scope="function")
async def page_manager(browser, test_config, data_manager, request):
    context = await browser.new_context(no_viewport=True)
    page = await context.new_page()
    logger.info(f"Navigating to: {test_config.base_url}")
    await page.goto(test_config.base_url)

    test_config.context = context
    page_manager = PageManager(page, test_config.auth.email, test_config.auth.username)
    request.node.page = page
    yield page_manager
    await context.close()
    logger.info("Browser context closed")

@pytest.fixture
def test_config():
    logger.info("Loading test configuration")
    return ConfigManager(CONFIG_PATH)

@pytest.fixture
def data_manager():
    logger.info("Creating data manager")
    return DataManager()

@pytest.fixture
def schema_data():
    logger.info("Creating schema data manager")
    return SchemaData("components/json_schema/saved_schemas")

@pytest.fixture
def api_helper():
    logger.info("Creating API helper")
    return APIHelper()

@pytest.fixture
def apolo_cli():
    logger.info("Creating Apolo CLI instance")
    return ApoloCLI()

@pytest.fixture(autouse=True)
async def clean_up(test_config, data_manager, apolo_cli):
    yield
    logger.info("Running post-test cleanup")

    if test_config.auth.token:
        logger.info("Logging in to Apolo CLI for cleanup")
        token = test_config.auth.token
        url = test_config.cli_login_url
        await apolo_cli.login_with_token(token, url)

    organizations = data_manager.get_all_organizations()
    logger.info(f"Cleaning up {len(organizations)} organizations")
    for organization in organizations:
        await apolo_cli.remove_organization(organization.org_name)
        logger.info(f"Removed organization: {organization.org_name}")