import pytest

from tests.test_cases.common_steps.cli_steps.cli_common_steps import CLICommonSteps
from tests.test_cases.common_steps.ui_steps.ui_common_steps import UICommonSteps
from tests.reporting_hooks.reporting import async_step, async_title, async_suite


@async_suite("CLI Organization Structure Setup")
class TestCLIOrganizationStructureSetup:

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

    @async_title("User creates a first organization via CLI")
    @pytest.mark.xfail(reason="BUG-ENG-747", strict=True)
    async def test_create_first_organization_cli(self):
        await self.cli_common_steps.cli_login_with_token()
        await self.cli_common_steps.verify_cli_organization_count(0)
        await self.cli_common_steps.cli_add_new_organization("My-organization")
        await self.cli_common_steps.verify_cli_organization_count(1)
        await self.cli_common_steps.verify_cli_organization_listed("My-organization")
