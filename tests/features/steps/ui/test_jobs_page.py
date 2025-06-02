from pytest_bdd import then, parsers, when


@then(parsers.re(r"^I should not see the '(?P<gherkin_name>.*)' job in the running jobs list$"))
def step_impl(page_manager, data_manager, gherkin_name):
    job = data_manager.get_job_from_default_project(gherkin_name)
    job_name = job.job_name
    assert not page_manager.jobs_page.is_jobs_button_displayed(job_name)

@then(parsers.re(r"^I should see the '(?P<gherkin_name>.*)' job in the list$"))
def step_impl(page_manager, data_manager, gherkin_name):
    job = data_manager.get_job_from_default_project(gherkin_name)
    job_name = job.job_name
    assert page_manager.jobs_page.is_jobs_button_displayed(job_name)

@when("I click the Show All Jobs button")
def step_impl(page_manager):
    page_manager.jobs_page.click_show_all_jobs_button()

@then(parsers.re(r"^The '(?P<gherkin_name>.*)' job status should be 'Successful'$"))
def step_impl(page_manager, data_manager, gherkin_name):
    job = data_manager.get_job_from_default_project(gherkin_name)
    job_name = job.job_name
    assert page_manager.jobs_page.is_job_status_successfull(job_name)