import allure
import pytest

from tests.test_cases.common_steps.cli_steps.cli_common_steps import CLICommonSteps
from tests.test_cases.common_steps.ui_steps.ui_common_steps import UICommonSteps
from tests.reporting_hooks.reporting import async_step, async_title, async_suite

@allure.feature("CLI Login")
@async_suite("CLI Login")
@pytest.mark.asyncio
class TestCLILogin():

    @pytest.fixture(autouse=True)
    async def setup(self, page_manager, data_manager, apolo_cli, test_config):
        """
        Initialize shared resources for the test methods.
        """
        self.__page_manager = page_manager
        self.__data_manager = data_manager
        self.__apolo_cli = apolo_cli
        self.__test_config = test_config
        self.ui_common_steps = UICommonSteps(self.__page_manager, self.__test_config, self.__data_manager)
        self.cli_common_steps = CLICommonSteps(self.__test_config, self.__apolo_cli, self.__data_manager)

        #Login via UI to get access token
        await self.ui_common_steps.ui_login()
        #Verify CLI client installed
        await self.cli_common_steps.verify_cli_client_installed()

    @async_title("User logs in to Apolo CLI with auth token and verifies login success")
    async def test_login_with_token_cli(self):
        await self.cli_common_steps.cli_login_with_token()
        await self.cli_verify_login_successfull()
        await self.cli_verify_login_output()

    @async_step("Verify CLI login successfull")
    async def cli_verify_login_successfull(self):
        assert self.__apolo_cli.login_successful

    @async_step("Verify CLI login output")
    async def cli_verify_login_output(self):
        url = self.__test_config.cli_login_url
        username = self.__test_config.auth.username
        if self.__data_manager.default_organization:
            organization_name = self.__data_manager.default_organization.org_name
            if self.__data_manager.default_organization.default_project:
                project_name = self.__data_manager.default_organization.default_project.project_name
            else:
                project_name = None
        else:
            organization_name = None
            project_name = None
        assert await self.__apolo_cli.verify_login_output(url, username, organization_name, project_name)

