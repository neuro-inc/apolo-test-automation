from pytest_bdd import given, parsers


@given("the Apolo CLI client is installed")
def step_impl(apolo_cli):
    assert apolo_cli.is_cli_installed()


@given("I am logged in with Apolo CLI using an access token")
def step_impl(test_config, apolo_cli):
    token = test_config.auth.token
    url = test_config.cli_login_url
    apolo_cli.login_with_token(token, url)
    assert apolo_cli.login_successful


@given(parsers.re(r'^I created "(?P<gherkin_name>.+)" project via CLI$'))
def step_impl(data_manager, apolo_cli, gherkin_name):
    organization = data_manager.default_organization
    project = organization.add_project(gherkin_name)
    prject_name = project.project_name
    apolo_cli.create_project(project_name=prject_name)