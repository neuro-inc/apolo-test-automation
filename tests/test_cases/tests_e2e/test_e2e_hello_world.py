import asyncio

import pytest

from tests.reporting_hooks.reporting import async_step, async_suite, async_title
from tests.test_cases.common_steps.cli_steps.cli_common_steps import CLICommonSteps
from tests.test_cases.common_steps.ui_steps.ui_common_steps import UICommonSteps


@async_suite("Apolo CLI Hello World Job Verification")
class TestHelloWorldJob:
    @pytest.fixture(autouse=True)
    async def setup(self, page_manager, data_manager, apolo_cli, test_config):
        """
        Initialize shared resources for the test methods.
        """
        self._page_manager = page_manager
        self._data_manager = data_manager
        self._apolo_cli = apolo_cli
        self._test_config = test_config
        self.ui_common_steps = UICommonSteps(
            self._page_manager, self._test_config, self._data_manager
        )
        self.cli_common_steps = CLICommonSteps(
            self._test_config, self._apolo_cli, self._data_manager
        )

        # Verify CLI client installed
        await self.cli_common_steps.verify_cli_client_installed()

    @async_title("Run Hello World Job and Validate UI and CLI Results")
    async def test_run_hello_world_job(self):
        await self.ui_common_steps.ui_pass_new_user_onboarding("default")
        await self.cli_common_steps.cli_login_with_token()
        await asyncio.sleep(2)
        await self.create_project()
        await self.run_hello_world_job()
        await self.check_job_not_in_running()
        await self.verify_job_successful()

    @async_step("Log in via UI")
    async def login(self):
        await self._page_manager.auth_page.click_log_in_button()
        await self._page_manager.login_page.login(self._test_config)

    @async_step("Create default organization")
    async def create_organization(self):
        organization = self._data_manager.add_organization("default")
        await self._apolo_cli.create_organization(org_name=organization.org_name)

    @async_step("Create my-project in the default organization")
    async def create_project(self):
        project = self._data_manager.default_organization.add_project("my-project")
        await self._apolo_cli.create_project(project_name=project.project_name)

    @async_step("Run Hello World job via CLI")
    async def run_hello_world_job(self):
        project = self._data_manager.default_organization.default_project
        job = project.add_job("Hello World", command="echo Hello, World")
        job.job_id = await self._apolo_cli.run_job(
            job_name=job.job_name, image=job.image_name, command=job.command
        )

    @async_step("Open Jobs page and verify job not in running list")
    async def check_job_not_in_running(self):
        await self._page_manager.main_page.page.reload()
        await self._page_manager.main_page.click_jobs_button()
        assert not await self._page_manager.jobs_page.is_jobs_button_displayed(
            "Hello World"
        )

    @async_step("Show all jobs and verify job is successful")
    async def verify_job_successful(self):
        await self._page_manager.jobs_page.click_show_all_jobs_button()
        job = self._data_manager.get_job_from_default_project("Hello World")
        assert await self._page_manager.jobs_page.is_jobs_button_displayed(job.job_name)
        assert await self._page_manager.jobs_page.is_job_status_successfull(
            job.job_name
        )
