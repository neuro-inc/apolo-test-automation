import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.common_steps.cli_steps.cli_common_steps import CLICommonSteps
from tests.test_cases.common_steps.ui_steps.ui_common_steps import UICommonSteps
from tests.components.ui.page_manager import PageManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager


@async_suite("CLI Organization Structure Setup")
class TestCLIOrganizationStructureSetup:
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

        email = self._test_config.auth.email
        password = self._test_config.auth.password
        # Login via UI to get access token
        await self.ui_common_steps.ui_login(email, password)
        # Verify CLI client installed
        await self.cli_common_steps.verify_cli_client_installed()

    @async_title("User creates a first organization via CLI")
    @pytest.mark.xfail(reason="BUG-ENG-747", strict=True)
    async def test_create_first_organization_cli(self) -> None:
        await self.cli_common_steps.cli_login_with_token()
        await self.cli_common_steps.verify_cli_organization_count(0)
        await self.cli_common_steps.cli_add_new_organization("My-organization")
        await self.cli_common_steps.verify_cli_organization_count(1)
        await self.cli_common_steps.verify_cli_organization_listed("My-organization")
