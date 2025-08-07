import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.tests_cli.base_cli_test import BaseCLITest


@async_suite("CLI Organization Structure Setup", parent="CLI Tests")
class TestCLIOrganizationStructureSetup(BaseCLITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._ui_steps = await self.init_ui_test_steps()
        self._cli_steps = await self.init_test_steps()

        # Verify CLI client installed
        await self._cli_steps.verify_cli_client_installed()

    @async_title("User creates a first organization via CLI")
    async def test_create_first_organization_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.verify_cli_organization_count(0)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        await self._cli_steps.verify_cli_organization_count(1)
        await self._cli_steps.verify_cli_organization_listed("My-organization")

    @async_title("User creates a second organization via CLI")
    async def test_create_second_organization_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.verify_cli_organization_count(0)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        await self._cli_steps.verify_cli_organization_count(1)
        await self._cli_steps.verify_cli_organization_listed("My-organization")

        await self._cli_steps.cli_add_new_organization("Second-organization", user=user)
        await self._cli_steps.verify_cli_organization_count(2)
        await self._cli_steps.verify_cli_organization_listed("My-organization")
        await self._cli_steps.verify_cli_organization_listed("Second-organization")

    @async_title("User removes organization via CLI")
    async def test_remove_organization_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.verify_cli_organization_count(0)

        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        await self._cli_steps.verify_cli_organization_count(1)
        await self._cli_steps.verify_cli_organization_listed("My-organization")

        await self._cli_steps.cli_remove_org("My-organization")
        await self._cli_steps.verify_cli_organization_count(0)

    @async_title("User verifies config show output via CLI")
    async def test_config_show_output_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        await self._cli_steps.cli_show_config()
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.verify_cli_show_command_output(
            expected_username=user.username, expected_org=org.org_name
        )

    @async_title("User switch organization via CLI")
    async def test_switch_org_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        await self._cli_steps.cli_add_new_organization("Second-organization", user=user)

        org = self._data_manager.get_organization_by_gherkin_name("Second-organization")
        await self._cli_steps.cli_switch_org(org_name=org.org_name)
        await self._cli_steps.cli_show_config()
        await self._cli_steps.verify_cli_show_command_output(
            expected_username=user.username, expected_org=org.org_name
        )

    @async_title("Invite user to org via CLI")
    async def test_invite_user_to_org_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        await self._cli_steps.cli_verify_login_output(
            second_user.username, org_name=org.org_name
        )

    @async_title("Invite user to organization with default project via CLI")
    async def test_invite_user_to_org_with_default_proj_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            default_proj=True,
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        await self._cli_steps.cli_verify_login_output(
            second_user.username, org_name=org.org_name, proj_name=proj.project_name
        )

    @async_title("User verifies admin get-org-users output via CLI")
    async def test_verify_get_org_users_output_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.verify_cli_user_in_orgs_users_output(
            username=user.username, role="Admin", email=user.email, credits="unlimited"
        )

        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="User",
            email=second_user.email,
            credits="unlimited",
        )

    @async_title("Set default user credits via CLI")
    async def test_set_user_credits_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)

        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_show_config()
        await self._cli_steps.verify_cli_show_command_output(
            expected_username=user.username,
            expected_org=org.org_name,
            expected_org_credits=500,
        )

        await self._cli_steps.cli_set_org_default_credits(
            org_name=org.org_name, credits_amount=234
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_login_with_token(token=second_user.token)
        await self._cli_steps.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="User",
            email=second_user.email,
            credits=234,
        )
