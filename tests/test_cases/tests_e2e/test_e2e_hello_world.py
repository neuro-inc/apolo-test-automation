import asyncio
import pytest

from tests.reporting_hooks.reporting import async_step, async_suite, async_title
from tests.test_cases.steps.common_steps.cli_steps.cli_common_steps import (
    CLICommonSteps,
)
from tests.components.ui.page_manager import PageManager
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.utils.api_helper import APIHelper
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.users_manager import UsersManager


@async_suite("Apolo CLI Hello World Job Verification")
class TestHelloWorldJob:
    @pytest.fixture(autouse=True)
    async def setup(
        self,
        page_manager: PageManager,
        data_manager: DataManager,
        apolo_cli: ApoloCLI,
        test_config: ConfigManager,
        users_manager: UsersManager,
        api_helper: APIHelper,
    ) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._pm = page_manager
        self._data_manager = data_manager
        self._apolo_cli = apolo_cli
        self._test_config = test_config
        self._users_manager = users_manager
        self._api_helper = api_helper
        self.ui_steps = UISteps(
            self._pm,
            self._test_config,
            self._data_manager,
            self._users_manager,
            self._api_helper,
        )
        self.cli_common_steps = CLICommonSteps(
            self._test_config, self._apolo_cli, self._data_manager
        )
        user = await self.ui_steps.ui_signup_new_user_ver_link()
        self._email = user.email
        self._password = user.password

        # Verify CLI client installed
        await self.cli_common_steps.verify_cli_client_installed()

    @async_title("Run Hello World Job and Validate UI and CLI Results")
    async def test_run_hello_world_job(self) -> None:
        await self.ui_steps.ui_login(self._email, self._password)
        await self.ui_steps.ui_pass_new_user_onboarding("default")
        await self.cli_common_steps.cli_login_with_token()
        await asyncio.sleep(2)
        await self.create_project("my-project")
        await self.run_hello_world_job("my-project")
        await self.ui_steps.ui_reload_page()
        await self.ui_check_job_not_in_running()
        await self.verify_job_successful("Hello World")

    @async_step("Log in via UI")
    async def login(self) -> None:
        await self._pm.auth_page.click_log_in_button()
        await self._pm.login_page.login(self._email, self._password)

    @async_step("Create default organization")
    async def create_organization(self) -> None:
        organization = self._data_manager.add_organization("default")
        await self._apolo_cli.create_organization(org_name=organization.org_name)

    @async_step("Create my-project in the default organization")
    async def create_project(self, project_name: str) -> None:
        project = self._data_manager.default_organization.add_project(project_name)
        await self._apolo_cli.create_project(project_name=project.project_name)

    @async_step("Run Hello World job via CLI")
    async def run_hello_world_job(self, project_name: str) -> None:
        organization = self._data_manager.default_organization
        project = organization.get_project_by_gherkin_name(project_name)
        job = project.add_job("Hello World", command="echo Hello, World")
        job.job_id = await self._apolo_cli.run_job(
            job_name=job.job_name,
            image=job.image_name,
            command=job.command,
        )

    @async_step("Open Jobs page and verify job not in running list")
    async def ui_check_job_not_in_running(self) -> None:
        await self._pm.main_page.page.reload()
        await self._pm.main_page.click_jobs_button()
        assert not await self._pm.jobs_page.is_jobs_button_displayed("Hello World"), (
            "Job 'Hello World' should not be displayed in running jobs!"
        )

    @async_step("Show all jobs and verify job is successful")
    async def verify_job_successful(self, job_name: str) -> None:
        await self._pm.jobs_page.click_show_all_jobs_button()
        job = self._data_manager.get_job_from_default_project(job_name)
        assert await self._pm.jobs_page.is_jobs_button_displayed(job.job_name), (
            f"Job {job_name} should be displayed!"
        )
        assert await self._pm.jobs_page.is_job_status_successfull(job.job_name), (
            f"Job {job_name} status should be successful!"
        )
