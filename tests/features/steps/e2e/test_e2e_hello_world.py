from pytest_bdd import scenarios

from tests.features.steps.common_steps.cli_common_steps import *
from tests.features.steps.common_steps.ui_common_steps import *
from tests.features.steps.ui.test_jobs_page import *

scenarios('../../test_e2e/test_e2e_hello_world.feature')

@when(parsers.re(r"^I run the '(?P<gherkin_name>.*)' job via CLI$"))
def step_impl(data_manager, apolo_cli, gherkin_name):
    organization = data_manager.default_organization
    project = organization.default_project
    command = "echo Hello, World"
    job = project.add_job(gherkin_name=gherkin_name, command=command)
    job_id = apolo_cli.run_job(job_name= job.job_name, image= job.image_name, command=command)
    job.job_id = job_id
