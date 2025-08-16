import pytest

from tests.reporting_hooks.reporting import async_suite, async_title

from tests.test_cases.base_test_class import BaseTestClass


@async_suite("CLI Organization Remove Members", parent="CLI Tests")
class TestCLIOrganizationRemoveMembers(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._ui_steps = await self.init_ui_test_steps()
        self._cli_steps = await self.init_cli_test_steps()

        # Verify CLI client installed
        await self._cli_steps.verify_cli_client_installed()

    @async_title("Admin removes User from org via **CLI**")
    async def test_admin_remove_user_from_org_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Signup `second user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Add `second user` to organization with `User` role via **CLI**.

        ### Verify that:

        - `Admin` can remove `User` from organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
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

        await self._cli_steps.admin.cli_remove_user_from_org(
            org_name=org.org_name, username=second_user.username
        )
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_not_in_orgs_users_output(
            username=second_user.username,
            role="User",
            email=second_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.config.cli_verify_login_output(second_user.username)

    @async_title("Admin removes Manager from org via **CLI**")
    async def test_admin_remove_manager_from_org_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Signup `second user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Add `second user` to organization with `Manager` role via **CLI**.

        ### Verify that:

        - `Admin` can remove `Manager` from organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="Manager"
        )

        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="Manager",
            email=second_user.email,
            credits="unlimited",
        )

        await self._cli_steps.admin.cli_remove_user_from_org(
            org_name=org.org_name, username=second_user.username
        )
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_not_in_orgs_users_output(
            username=second_user.username,
            role="Manager",
            email=second_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.config.cli_verify_login_output(second_user.username)

    @async_title("Admin removes Admin from org via **CLI**")
    async def test_admin_remove_admin_from_org_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Signup `second user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Add `second user` to organization with `Admin` role via **CLI**.

        ### Verify that:

        - `Admin` can remove `Admin` from organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="Admin"
        )

        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="Admin",
            email=second_user.email,
            credits="unlimited",
        )

        await self._cli_steps.admin.cli_remove_user_from_org(
            org_name=org.org_name, username=second_user.username
        )
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_not_in_orgs_users_output(
            username=second_user.username,
            role="Admin",
            email=second_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.config.cli_verify_login_output(second_user.username)

    @async_title("Admin removes himself from org via **CLI**")
    async def test_admin_remove_himself_from_org_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Signup `second user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Add `second user` to organization with `Admin` role via **CLI**.
        - `Second user` login with Bearer auth token via **CLI**.

        ### Verify that:

        - `Admin` **cannot** remove `himself` from organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="Admin"
        )

        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="Admin",
            email=second_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        expected_error = (
            "ERROR: Illegal argument(s) (Org users cannot remove themselves)"
        )
        await self._cli_steps.admin.cli_remove_user_from_org(
            org_name=org.org_name,
            username=second_user.username,
            expected_error=expected_error,
        )
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="Admin",
            email=second_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.config.cli_verify_login_output(
            second_user.username, org_name=org.org_name
        )

    @async_title("Manager removes User from org via **CLI**")
    async def test_manager_remove_user_from_org_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Signup `second user` via **UI**.
        - Signup `third user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Add `second user` to organization with `Manager` role via **CLI**.
        - Add `third user` to organization with `User` role via **CLI**.
        - `Second user` login with Bearer auth token via **CLI**.

        ### Verify that:

        - `Manager` can remove `User` from organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="Manager"
        )
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="Manager",
            email=second_user.email,
            credits="unlimited",
        )
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=third_user.username,
            role="User",
            email=third_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.admin.cli_remove_user_from_org(
            org_name=org.org_name, username=third_user.username
        )
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_not_in_orgs_users_output(
            username=third_user.username,
            role="User",
            email=third_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=third_user.token)
        await self._cli_steps.config.cli_verify_login_output(third_user.username)

    @async_title("Manager removes Manager from org via **CLI**")
    async def test_manager_remove_manager_from_org_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Signup `second user` via **UI**.
        - Signup `third user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Add `second user` to organization with `Manager` role via **CLI**.
        - Add `third user` to organization with `Manager` role via **CLI**.
        - `Second user` login with Bearer auth token via **CLI**.

        ### Verify that:

        - `Manager` can remove `Manager` from organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="Manager"
        )
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="Manager"
        )

        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="Manager",
            email=second_user.email,
            credits="unlimited",
        )
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=third_user.username,
            role="Manager",
            email=third_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.admin.cli_remove_user_from_org(
            org_name=org.org_name, username=third_user.username
        )
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_not_in_orgs_users_output(
            username=third_user.username,
            role="Manager",
            email=third_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=third_user.token)
        await self._cli_steps.config.cli_verify_login_output(third_user.username)

    @async_title("Manager removes Admin from org via **CLI**")
    async def test_manager_remove_admin_from_org_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Signup `second user` via **UI**.
        - Signup `third user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Add `second user` to organization with `Manager` role via **CLI**.
        - Add `third user` to organization with `Admin` role via **CLI**.
        - `Second user` login with Bearer auth token via **CLI**.

        ### Verify that:

        - `Manager` **cannot** remove `Admin` from organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="Manager"
        )
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="Admin"
        )

        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="Manager",
            email=second_user.email,
            credits="unlimited",
        )
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=third_user.username,
            role="Admin",
            email=third_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        expected_error = f"ERROR: Not enough permissions (User {second_user.username} has to have admin access to remove other admin users)"
        await self._cli_steps.admin.cli_remove_user_from_org(
            org_name=org.org_name,
            username=third_user.username,
            expected_error=expected_error,
        )
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=third_user.username,
            role="Admin",
            email=third_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=third_user.token)
        await self._cli_steps.config.cli_verify_login_output(
            third_user.username, org_name=org.org_name
        )

    @async_title("Manager removes himself from org via **CLI**")
    async def test_manager_remove_himself_from_org_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Signup `second user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Add `second user` to organization with `Manager` role via **CLI**.
        - `Second user` login with Bearer auth token via **CLI**.

        ### Verify that:

        - `Manager` **cannot** remove `himself` from organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="Manager"
        )

        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="Manager",
            email=second_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        expected_error = (
            "ERROR: Illegal argument(s) (Org users cannot remove themselves)"
        )
        await self._cli_steps.admin.cli_remove_user_from_org(
            org_name=org.org_name,
            username=second_user.username,
            expected_error=expected_error,
        )
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="Manager",
            email=second_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.config.cli_verify_login_output(
            second_user.username, org_name=org.org_name
        )

    @async_title("User removes User from org via **CLI**")
    async def test_user_remove_user_from_org_cli(self) -> None:
        """
        - Login with valid credentials via **UI**.
        - Get Bearer auth token from Playwright local storage.
        - Create new organization via **API**.
        - Signup `second user` via **UI**.
        - Signup `third user` via **UI**.
        - Login with Bearer auth token via **CLI**.
        - Add `second user` to organization with `User` role via **CLI**.
        - Add `third user` to organization with `User` role via **CLI**.
        - `Second user` login with Bearer auth token via **CLI**.

        ### Verify that:

        - `User` **cannot** remove members from organization via **CLI**.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.admin.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=second_user.username,
            role="User",
            email=second_user.email,
            credits="unlimited",
        )
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=third_user.username,
            role="User",
            email=third_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        expected_error = f'ERROR: Not enough permissions ({{"missing": [{{"uri": "org://{org.org_name}/users", "action": "write"}}]}})'
        await self._cli_steps.admin.cli_remove_user_from_org(
            org_name=org.org_name,
            username=third_user.username,
            expected_error=expected_error,
        )
        await self._cli_steps.admin.cli_get_org_users(org_name=org.org_name)
        await self._cli_steps.admin.verify_cli_user_in_orgs_users_output(
            username=third_user.username,
            role="User",
            email=third_user.email,
            credits="unlimited",
        )

        await self._cli_steps.config.cli_login_with_token(token=third_user.token)
        await self._cli_steps.config.cli_verify_login_output(
            third_user.username, org_name=org.org_name
        )
