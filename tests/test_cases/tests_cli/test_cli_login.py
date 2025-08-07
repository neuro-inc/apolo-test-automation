import pytest

from tests.reporting_hooks.reporting import async_step, async_suite, async_title
from tests.test_cases.tests_cli.base_cli_test import BaseCLITest


@async_suite("CLI Login", parent="CLI Tests")
class TestCLILogin(BaseCLITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._ui_steps = await self.init_ui_test_steps()
        self._cli_steps = await self.init_test_steps()

        await self._cli_steps.verify_cli_client_installed()

    @async_title("User without organization logs in with auth token via CLI")
    async def test_login_with_token_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self.cli_verify_login_successful()
        await self._cli_steps.cli_verify_login_output(user.username)

    @async_title("User with organization logs in with auth token via CLI")
    async def test_login_org_with_token_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self.cli_verify_login_successful()
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await self._cli_steps.cli_verify_login_output(
            user.username, org_name=org.org_name
        )

    @async_title("User with organization and project logs in with auth token via CLI")
    async def test_login_org_proj_with_token_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project(gherkin_name="Default-project")
        await self._ui_steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self.cli_verify_login_successful()

        await self._cli_steps.cli_verify_login_output(
            user.username, org_name=org.org_name, proj_name=proj.project_name
        )

    @async_step("Verify CLI login successful")
    async def cli_verify_login_successful(self) -> None:
        assert self._apolo_cli.login_successful, "Login via CLI should be successful!"
