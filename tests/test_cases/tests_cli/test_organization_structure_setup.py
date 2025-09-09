import pytest

from tests.reporting_hooks.reporting import async_suite, async_title

from tests.test_cases.base_test_class import BaseTestClass


@async_suite("CLI Organization Structure Setup", parent="CLI Tests")
class TestCLIOrganizationStructureSetup(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._ui_steps = await self.init_ui_test_steps()
        self._cli_steps = await self.init_cli_test_steps()

        # Verify CLI client installed
        await self._cli_steps.verify_cli_client_installed()

    @async_title("User creates a first organization via CLI")
    async def test_create_first_organization_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Login with Bearer auth token via **CLI**.

        ### Verify that:

        - User can create first organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.config.cli_login_with_token(token=user.token)
        await self._cli_steps.admin.verify_cli_organization_count(0)
        await self._cli_steps.admin.cli_add_new_organization(
            "My-organization", user=user
        )
        await self._cli_steps.admin.verify_cli_organization_count(1)
        await self._cli_steps.admin.verify_cli_organization_listed("My-organization")

    @async_title("User creates a second organization via CLI")
    async def test_create_second_organization_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Login with Bearer auth token via **CLI**.
        - Create first organization via **CLI**.

        ### Verify that:

        - User can create second organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.config.cli_login_with_token(token=user.token)
        await self._cli_steps.admin.verify_cli_organization_count(0)
        await self._cli_steps.admin.cli_add_new_organization(
            "My-organization", user=user
        )
        await self._cli_steps.admin.verify_cli_organization_count(1)
        await self._cli_steps.admin.verify_cli_organization_listed("My-organization")

        await self._cli_steps.admin.cli_add_new_organization(
            "Second-organization", user=user
        )
        await self._cli_steps.admin.verify_cli_organization_count(2)
        await self._cli_steps.admin.verify_cli_organization_listed("My-organization")
        await self._cli_steps.admin.verify_cli_organization_listed(
            "Second-organization"
        )

    @async_title("User removes organization via CLI")
    async def test_remove_organization_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Login with Bearer auth token via **CLI**.
        - Create first organization via **CLI**.
        - Create second organization via **CLI**.

        ### Verify that:

        - User can remove organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.config.cli_login_with_token(token=user.token)
        await self._cli_steps.admin.verify_cli_organization_count(0)

        await self._cli_steps.admin.cli_add_new_organization(
            "My-organization", user=user
        )
        await self._cli_steps.admin.verify_cli_organization_count(1)
        await self._cli_steps.admin.verify_cli_organization_listed("My-organization")

        await self._cli_steps.admin.cli_remove_org("My-organization")
        await self._cli_steps.admin.verify_cli_organization_count(0)

    @async_title("User verifies config show output via CLI")
    async def test_config_show_output_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Login with Bearer auth token via **CLI**.
        - Create first organization via **CLI**.
        - Run `apolo config show` command via **CLI**.

        ### Verify that:

        - `apolo config show` command output is valid.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.config.cli_login_with_token(token=user.token)
        await self._cli_steps.admin.cli_add_new_organization(
            "My-organization", user=user
        )
        await self._cli_steps.config.cli_show_config()
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.config.verify_cli_show_command_output(
            expected_username=user.username, expected_org=org.org_name
        )

    @async_title("User switch organization via CLI")
    async def test_switch_org_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Login with Bearer auth token via **CLI**.
        - Create first organization via **CLI**.
        - Create second organization via **CLI**.

        ### Verify that:

        - User can switch between organizations via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.config.cli_login_with_token(token=user.token)
        await self._cli_steps.admin.cli_add_new_organization(
            "My-organization", user=user
        )
        await self._cli_steps.admin.cli_add_new_organization(
            "Second-organization", user=user
        )

        org = self._data_manager.get_organization_by_gherkin_name("Second-organization")
        await self._cli_steps.config.cli_switch_org(org_name=org.org_name)
        await self._cli_steps.config.cli_show_config()
        await self._cli_steps.config.verify_cli_show_command_output(
            expected_username=user.username, expected_org=org.org_name
        )

    @async_title("Invite user to org via CLI")
    async def test_invite_user_to_org_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Signup `second` user via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Create first organization via **CLI**.

        ### Verify that:

        - User can invite registered user to organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        await self._cli_steps.admin.cli_add_new_organization(
            "My-organization", user=user
        )
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.config.cli_verify_login_output(
            second_user.username, org_name=org.org_name
        )

    @async_title("Invite user to organization with default project via CLI")
    async def test_invite_user_to_org_with_default_proj_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Signup `second user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Create first organization via **CLI**.
        - Create first project with 'default' option via **CLI**.

        ### Verify that:

        - User can invite registered user to organization via **CLI**.
        - Newly invited user is member of default project.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        await self._cli_steps.admin.cli_add_new_organization(
            "My-organization", user=user
        )
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            default_proj=True,
        )
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.config.cli_verify_login_output(
            second_user.username, org_name=org.org_name, proj_name=proj.project_name
        )

    @async_title("User verifies admin get-org-users output via CLI")
    async def test_verify_get_org_users_output_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Signup `second user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Create first organization via **CLI**.
        - Invite `second user` to organization via **CLI**.
        - Run `apolo admin get-org-users` command via **CLI**.

        ### Verify that:

        - Organization members are listed with valid data in command output.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        await self._cli_steps.admin.cli_add_new_organization(
            "My-organization", user=user
        )
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=user.username, role="Admin", email=user.email, credits="unlimited"
        )

        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="User",
            email=second_user.email,
            credits="unlimited",
        )

    @async_title("Set default user credits via CLI")
    async def test_set_user_credits_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Signup `second user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Create first organization via **CLI**.
        - Set default user credits via **CLI**.
        - Invite `second user` to organization via **CLI**.
        - `Second user` login with Bearer auth token via **CLI**.
        - Run `apolo config show` command via **CLI**.

        ### Verify that:

        - Valid user credits amount is displayed in command output.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        await self._cli_steps.admin.cli_add_new_organization(
            "My-organization", user=user
        )

        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.config.cli_show_config()
        await self._cli_steps.config.verify_cli_show_command_output(
            expected_username=user.username,
            expected_org=org.org_name,
            expected_org_credits=500,
        )

        await self._cli_steps.admin.cli_set_org_default_credits(
            org_name=org.org_name, credits_amount=234
        )
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="User",
            email=second_user.email,
            credits=234,
        )
