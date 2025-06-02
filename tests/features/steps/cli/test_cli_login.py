from pytest_bdd import scenarios

from tests.features.steps.common_steps.ui_common_steps import *
from tests.features.steps.common_steps.cli_common_steps import *

scenarios('../../test_cli/test_cli_login.feature')

@when("I login to Apolo CLI with an auth token")
def step_impl(test_config, apolo_cli):
    token = test_config.auth.token
    url = test_config.cli_login_url
    apolo_cli.login_with_token(token, url)


@then("I should see successful login confirmation in CLI output")
def step_impl(apolo_cli):
    assert apolo_cli.login_successful


@then("the valid organization and project should be displayed in CLI output")
def step_impl(test_config, data_manager, apolo_cli):
    url = test_config.cli_login_url
    username = test_config.auth.username
    if data_manager.default_organization:
        organization_name = data_manager.default_organization.org_name
        if data_manager.default_organization.default_project:
            project_name = data_manager.default_organization.default_project.project_name
        else:
            project_name = None
    else:
        organization_name = None
        project_name = None
    assert apolo_cli.verify_login_output(
        url, username, organization_name, project_name
    )
