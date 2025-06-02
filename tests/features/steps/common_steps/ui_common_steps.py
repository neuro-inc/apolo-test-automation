from pytest_bdd import given, when, then, parsers

from tests.utils.browser_helper import extract_access_token_from_local_storage


@given("I am on the main page")
def step_impl(page_manager, test_config):
    page_manager.auth_page.click_log_in_button()
    page_manager.login_page.login(test_config)
    assert page_manager.main_page.is_loaded()
    token = extract_access_token_from_local_storage(page_manager.login_page.page)
    test_config.auth.token = token

@given("I am on the welcome new user page")
def step_impl(page_manager, test_config):
    page_manager.auth_page.click_log_in_button()
    page_manager.login_page.login(test_config)
    assert page_manager.welcome_new_user_page.is_loaded()
    token = extract_access_token_from_local_storage(page_manager.login_page.page)
    test_config.auth.token = token

@given(parsers.re(r'^"(?P<gherkin_name>.+)" organization created via UI and I on the main page$'))
def step_impl(page_manager, test_config, data_manager, gherkin_name):
    page_manager.auth_page.click_log_in_button()
    page_manager.login_page.login(test_config)
    assert page_manager.welcome_new_user_page.is_loaded()
    token = extract_access_token_from_local_storage(page_manager.login_page.page)
    test_config.auth.token = token

    page_manager.page.wait_for_timeout(500)
    page_manager.welcome_new_user_page.click_lets_do_it_button()

    page_manager.join_organization_page.click_create_organization_button()

    organization = data_manager.add_organization(gherkin_name=gherkin_name)
    organization_name = organization.org_name
    page = page_manager.name_your_organization_page
    page.type_text_to_organization_name_input(organization_name)

    page_manager.name_your_organization_page.click_next_button()

    page_manager.page.wait_for_timeout(500)
    page_manager.welcome_new_user_page.click_lets_do_it_button()

@when("I open the Jobs page")
def step_impl(page_manager):
    page_manager.main_page.page.reload()
    page_manager.main_page.click_jobs_button()


@then("I should be redirected to the dashboard")
def step_imp(page_manager):
    assert page_manager.main_page.is_loaded()


@then("I should be redirected to the welcome new user page")
def step_impl(page_manager):
    assert page_manager.welcome_new_user_page.is_loaded()


@then(parsers.re(r'^project creation message for "(?P<gherkin_name>.*)" is displayed$'))
def step_impl(data_manager, page_manager, gherkin_name):
    organization = data_manager.get_organization_by_gherkin_name(gherkin_name)
    page = page_manager.main_page
    assert page.is_create_first_project_text_field_displayed(organization.org_name)


@then("create project button is displayed")
def step_impl(page_manager):
    assert page_manager.main_page.is_create_first_project_button_displayed()