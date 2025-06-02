from pytest_bdd import scenarios

from tests.features.steps.common_steps.ui_common_steps import *

scenarios('../../test_json_schema/aws_s3.feature')

@given(parsers.parse("the saved JSON Schema is loaded for '{app_name}' app"))
def step_impl(schema_data, app_name):
    schema_data.load_saved_schema(app_name)


@given(parsers.parse("I fetch the templates API response for '{app_name}' app"))
def step_impl(test_config, schema_data, api_helper, app_name):
    endpoint = test_config.get_template_url()
    token = test_config.auth.token

    response = api_helper.get(endpoint=endpoint, token=token)
    response.raise_for_status()
    data = response.json()
    schema_data.parse_live_schema(data, app_name)


@when("I validate the response against the JSON Schema")
def step_impl(schema_data):
    schema_data.validate()


@then("the response should conform to the schema")
def step_impl(test_data):
    assert test_data.schema_manager.error is None, test_data.schema_manager.error_message

