import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
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


@async_suite("CLI Organization Structure Setup")
class TestCLIOrganizationStructureSetup:
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
        self._page_manager = page_manager
        self._data_manager = data_manager
        self._apolo_cli = apolo_cli
        self._test_config = test_config
        self._users_manager = users_manager
        self._api_helper = api_helper
        self.ui_steps = UISteps(
            self._page_manager,
            self._test_config,
            self._data_manager,
            self._users_manager,
            self._api_helper,
        )
        self.cli_common_steps = CLICommonSteps(
            self._test_config, self._apolo_cli, self._data_manager
        )

        # Verify CLI client installed
        await self.cli_common_steps.verify_cli_client_installed()

    @async_title("User creates a first organization via CLI")
    async def test_create_first_organization_cli(self) -> None:
        user = self._users_manager.main_user
        await self.ui_steps.ui_login(user=user)
        await self.cli_common_steps.cli_login_with_token(token=user.token)
        await self.cli_common_steps.verify_cli_organization_count(0)
        await self.cli_common_steps.cli_add_new_organization(
            "My-organization", user=user
        )
        await self.cli_common_steps.verify_cli_organization_count(1)
        await self.cli_common_steps.verify_cli_organization_listed("My-organization")

    @async_title("User creates a second organization via CLI")
    async def test_create_second_organization_cli(self) -> None:
        user = self._users_manager.main_user
        await self.ui_steps.ui_login(user=user)
        await self.cli_common_steps.cli_login_with_token(token=user.token)
        await self.cli_common_steps.verify_cli_organization_count(0)
        await self.cli_common_steps.cli_add_new_organization(
            "My-organization", user=user
        )
        await self.cli_common_steps.verify_cli_organization_count(1)
        await self.cli_common_steps.verify_cli_organization_listed("My-organization")

        await self.cli_common_steps.cli_add_new_organization(
            "Second-organization", user=user
        )
        await self.cli_common_steps.verify_cli_organization_count(2)
        await self.cli_common_steps.verify_cli_organization_listed("My-organization")
        await self.cli_common_steps.verify_cli_organization_listed(
            "Second-organization"
        )

    @async_title("User removes organization via CLI")
    async def test_remove_organization_cli(self) -> None:
        user = self._users_manager.main_user
        await self.ui_steps.ui_login(user=user)
        await self.cli_common_steps.cli_login_with_token(token=user.token)
        await self.cli_common_steps.verify_cli_organization_count(0)

        await self.cli_common_steps.cli_add_new_organization(
            "My-organization", user=user
        )
        await self.cli_common_steps.verify_cli_organization_count(1)
        await self.cli_common_steps.verify_cli_organization_listed("My-organization")

        await self.cli_common_steps.cli_remove_org("My-organization")
        await self.cli_common_steps.verify_cli_organization_count(0)
