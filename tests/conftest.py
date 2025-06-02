import logging
import os

import pytest
from playwright.sync_api import sync_playwright

from tests.components.ui.page_manager import PageManager
from tests.utils.api_helper import APIHelper
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.schema_data import SchemaData
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.test_data_manager import TestDataManager

logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "tests", "test_data.yaml")

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        logger.info("Initializing browser")
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page_manager(browser, test_config, data_manager, request):
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    logger.info(f"Opening page {test_config.base_url}")
    page.goto(test_config.base_url)
    test_config.context = context
    email = test_config.auth.email
    username = test_config.auth.username
    page_manager = PageManager(page, email, username)
    request.node.page = page
    yield page_manager
    context.close()

@pytest.fixture
def test_config():
    return ConfigManager(CONFIG_PATH)

@pytest.fixture
def data_manager():
    return DataManager()

@pytest.fixture
def schema_data():
    return SchemaData("components/json_schema/saved_schemas")

@pytest.fixture
def api_helper():
    return APIHelper()

@pytest.fixture
def apolo_cli():
    return ApoloCLI()

@pytest.fixture(autouse=True)
def clean_up(test_config, data_manager,apolo_cli):
    yield
    logger.info("Cleaning up created organizations")
    if test_config.auth.token:
        token = test_config.auth.token
        url = test_config.cli_login_url
        apolo_cli.login_with_token(token, url)
    for organization in data_manager.get_all_organizations():
        org_name = organization.org_name
        apolo_cli.remove_organization(org_name)




pytest_plugins = ["tests.reporting_hooks.hooks"]
