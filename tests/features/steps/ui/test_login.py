from pytest_bdd import scenarios
from tests.features.steps.common_steps.ui_common_steps import *

scenarios('../../test_ui/test_login.feature')

@given("I am on the login page")
def step_imp(page_manager):
    page_manager.auth_page.click_log_in_button()

@when("I enter valid credentials")
def step_imp(page_manager, test_config):
    page_manager.login_page.enter_email(test_config.auth.email)
    page_manager.login_page.enter_password(test_config.auth.password)

@when("I press the login button")
def step_imp(page_manager):
    page_manager.login_page.click_continue_button()

