from pytest_bdd import scenarios

from tests.features.steps.common_steps.ui_common_steps import *
from tests.features.steps.common_steps.cli_common_steps import *

scenarios('../../test_cli/test_organization_structure_setup.feature')

@given("the organizations list is empty")
def step_impl(apolo_cli):
    organizations = apolo_cli.get_organizations()
    assert len(organizations) == 0, f"Expected 0 organizations, got {len(organizations)}"

@when(parsers.parse('I add a new organization "{gherkin_name}" via apolo CLI'))
def step_impl(data_manager, apolo_cli, gherkin_name):
    organization = data_manager.add_organization(gherkin_name=gherkin_name)
    apolo_cli.create_organization(org_name=organization.org_name)

@when("I list organizations via apolo CLI")
def step_impl(apolo_cli):
    apolo_cli.get_organizations()

@then(parsers.parse('"{gherkin_name}" should be listed'))
def step_imp(data_manager, apolo_cli, gherkin_name):
    created_organizations = data_manager.get_all_organizations()
    org = next((o for o in created_organizations if o.gherkin_name == gherkin_name), None)
    assert org is not None, f"No organization found with gherkin_name '{gherkin_name}'"

    assert org.org_name in apolo_cli.parsed_get_orgs_output, (
        f"Organization '{org.org_name}' (for gherkin_name '{gherkin_name}') "
        f"not found in CLI output: {apolo_cli.parsed_get_orgs_output}"
    )

@then(parsers.parse("{organization_count} organizations should be listed"))
def step_impl(data_manager, organization_count):
    created_organizations = data_manager.get_all_organizations()
    actual_count = len(created_organizations)
    assert actual_count == organization_count, f"Expected {organization_count} organizations, but found {actual_count}"
