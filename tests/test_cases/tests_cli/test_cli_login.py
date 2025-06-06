import pytest

from tests.components.ui.page_manager import PageManager
from tests.reporting_hooks.reporting import async_step, async_suite, async_title
from tests.test_cases.common_steps.cli_steps.cli_common_steps import CLICommonSteps
from tests.test_cases.common_steps.ui_steps.ui_common_steps import UICommonSteps
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager


@async_suite("CLI Login")
class TestCLILogin:
    @pytest.fixture(autouse=True)
    async def setup(
        self,
        page_manager: PageManager,
        data_manager: DataManager,
        apolo_cli: ApoloCLI,
        test_config: ConfigManager,
    ) -> None:
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

        # Login via UI to get access token
        await self.ui_common_steps.ui_login()
        # Verify CLI client installed
        await self.cli_common_steps.verify_cli_client_installed()

    @async_title("User logs in to Apolo CLI with auth token and verifies login success")
    async def test_login_with_token_cli(self) -> None:
        await self.cli_common_steps.cli_login_with_token()
        await self.cli_verify_login_successfull()
        await self.cli_verify_login_output()

    @async_step("Verify CLI login successfull")
    async def cli_verify_login_successfull(self) -> None:
        assert self._apolo_cli.login_successful

    @async_step("Verify CLI login output")
    async def cli_verify_login_output(
        self, check_org: bool = False, check_proj: bool = False
    ) -> None:
        url: str = self._test_config.cli_login_url
        username: str = self._test_config.auth.username

        organization_name = (
            self._data_manager.default_organization.org_name if check_org else None
        )
        project_name = (
            self._data_manager.default_organization.default_project.project_name
            if check_proj
            else None
        )

        assert await self._apolo_cli.verify_login_output(
            url, username, organization_name, project_name
        )
