from pytest_bdd import scenarios
from tests.features.steps.common_steps.ui_common_steps import *

scenarios('../../test_ui/test_create_first_organization.feature')

@when("I press the let's do it button")
def step_imp(page_manager):
    page_manager.page.wait_for_timeout(500)
    page_manager.welcome_new_user_page.click_lets_do_it_button()

@then("I should be redirected to the join organization page")
def step_imp(page_manager):
    assert page_manager.join_organization_page.is_loaded()

@when("I press create organization button")
def step_imp(page_manager):
    page_manager.join_organization_page.click_create_organization_button()

@then("I should be redirected to the name your organization page")
def step_imp(page_manager):
    assert page_manager.name_your_organization_page.is_loaded()

@when(parsers.re(r'^I type "(?P<gherkin_name>.*)" to the input filed$'))
def step_imp(data_manager, page_manager, gherkin_name):
    organization = data_manager.add_organization(gherkin_name=gherkin_name)
    organization_name = organization.org_name
    page = page_manager.name_your_organization_page
    page.type_text_to_organization_name_input(organization_name)

@when("I press next button")
def step_imp(page_manager):
    page = page_manager.name_your_organization_page
    page.click_next_button()

@then("I should be redirected to the that's it page")
def step_imp(page_manager):
    assert page_manager.thats_it_page.is_loaded()
