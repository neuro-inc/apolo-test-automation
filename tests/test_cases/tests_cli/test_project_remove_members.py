import pytest

from tests.reporting_hooks.reporting import async_suite, async_title

from tests.test_cases.base_test_class import BaseTestClass


@async_suite("CLI Project Remove Members", parent="CLI Tests")
class TestCLIProjectStructureSetup(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._ui_steps = await self.init_ui_test_steps()
        self._cli_steps = await self.init_cli_test_steps()

        # Verify CLI client installed
        await self._cli_steps.verify_cli_client_installed()

    @async_title("Admin removes Reader from project via CLI")
    async def test_admin_remove_reader_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Signup second user via UI.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Add second user to organization via CLI.
        -Add second user to project with Reader role via CLI.
        Verify that:
            - Admin can remove Reader from project via CLI.
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

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Reader",
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Reader", email=second_user.email
        )

        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_not_in_proj_users_output(
            username=second_user.username, role="Reader", email=second_user.email
        )

    @async_title("Admin removes Writer from project via CLI")
    async def test_admin_remove_writer_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Signup second user via UI.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Add second user to organization via CLI.
        -Add second user to project with Writer role via CLI.
        Verify that:
            - Admin can remove Writer from project via CLI.
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

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Writer",
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Writer", email=second_user.email
        )

        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_not_in_proj_users_output(
            username=second_user.username, role="Writer", email=second_user.email
        )

    @async_title("Admin removes Manager from project via CLI")
    async def test_admin_remove_manager_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Signup second user via UI.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Add second user to organization via CLI.
        -Add second user to project with Manager role via CLI.
        Verify that:
            - Admin can remove Manager from project via CLI.
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

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )

        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_not_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )

    @async_title("Admin removes Admin from project via CLI")
    async def test_admin_remove_admin_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Signup second user via UI.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Add second user to organization via CLI.
        -Add second user to project with Admin role via CLI.
        Verify that:
            - Admin can remove another Admin from project via CLI.
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

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Admin",
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Admin", email=second_user.email
        )

        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_not_in_proj_users_output(
            username=second_user.username, role="Admin", email=second_user.email
        )

    @async_title("Admin removes himself from project via CLI")
    async def test_admin_remove_himself_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        Verify that:
            - Admin cannot remove himself from project via CLI.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=user.username, role="Admin", email=user.email
        )

        expected_error = (
            "ERROR: Illegal argument(s) (Last project admin cannot be removed)"
        )
        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=user.username,
            expected_error=expected_error,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=user.username, role="Admin", email=user.email
        )

    @async_title("Manager removes Reader from project via CLI")
    async def test_manager_remove_reader_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Signup second user via UI.
        -Signup third user via UI.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Add second user to organization via CLI.
        -Add third user to organization via CLI.
        -Add second user to project with Manager role via CLI.
        -Add third user to project with Reader role via CLI.
        -Second user login with Bearer auth token via CLI.
        Verify that:
            - Manager can remove Reader from project via CLI.
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

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_not_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

    @async_title("Manager removes Writer from project via CLI")
    async def test_manager_remove_writer_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Signup second user via UI.
        -Signup third user via UI.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Add second user to organization via CLI.
        -Add third user to organization via CLI.
        -Add second user to project with Manager role via CLI.
        -Add third user to project with Writer role via CLI.
        -Second user login with Bearer auth token via CLI.
        Verify that:
            - Manager can remove Writer from project via CLI.
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

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Writer",
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Writer", email=third_user.email
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_not_in_proj_users_output(
            username=third_user.username, role="Writer", email=third_user.email
        )

    @async_title("Manager removes Manager from project via CLI")
    async def test_manager_remove_manager_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Signup second user via UI.
        -Signup third user via UI.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Add second user to organization via CLI.
        -Add third user to organization via CLI.
        -Add second user to project with Manager role via CLI.
        -Add third user to project with Manager role via CLI.
        -Second user login with Bearer auth token via CLI.
        Verify that:
            - Manager can remove another Manager from project via CLI.
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

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Manager",
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Manager", email=third_user.email
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_not_in_proj_users_output(
            username=third_user.username, role="Manager", email=third_user.email
        )

    @async_title("Manager removes Admin from project via CLI")
    async def test_manager_remove_admin_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Signup second user via UI.
        -Signup third user via UI.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Add second user to organization via CLI.
        -Add third user to organization via CLI.
        -Add second user to project with Manager role via CLI.
        -Add third user to project with Admin role via CLI.
        -Second user login with Bearer auth token via CLI.
        Verify that:
            - Manager cannot remove Admin from project via CLI.
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

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Admin",
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Admin", email=third_user.email
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        expected_error = f'ERROR: Not enough permissions ({{"missing": [{{"uri": "cluster://default/orgs/{org.org_name}/projects/{proj.project_name}/admins", "action": "write"}}]}})'
        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            expected_error=expected_error,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Admin", email=third_user.email
        )

    @async_title("Manager removes himself from project via CLI")
    @pytest.mark.xfail(reason="ENG-877", strict=True)
    async def test_manager_remove_himself_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Signup second user via UI.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Add second user to organization via CLI.
        -Add second user to project with Manager role via CLI.
        -Second user login with Bearer auth token via CLI.
        Verify that:
            - Manager cannot remove himself from project via CLI.
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

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )

    @async_title("Writer removes Reader from project via CLI")
    async def test_writer_remove_reader_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Signup second user via UI.
        -Signup third user via UI.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Add second user to organization via CLI.
        -Add third user to organization via CLI.
        -Add second user to project with Writer role via CLI.
        -Add third user to project with Reader role via CLI.
        -Second user login with Bearer auth token via CLI.
        Verify that:
            - Writer cannot remove members from project via CLI.
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

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Writer",
        )
        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Writer", email=second_user.email
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        expected_error = f'ERROR: Not enough permissions ({{"missing": [{{"uri": "cluster://default/orgs/{org.org_name}/projects/{proj.project_name}/users/{third_user.username}/delete", "action": "write"}}]}})'
        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            expected_error=expected_error,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

    @async_title("Reader removes Reader from project via CLI")
    async def test_reader_remove_reader_from_proj_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Signup second user via UI.
        -Signup third user via UI.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Add second user to organization via CLI.
        -Add third user to organization via CLI.
        -Add second user to project with Reader role via CLI.
        -Add third user to project with Reader role via CLI.
        -Second user login with Bearer auth token via CLI.
        Verify that:
            - Reader cannot remove members from project via CLI.
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

        proj = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Reader",
        )
        await self._cli_steps.admin.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
        )

        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Reader", email=second_user.email
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

        await self._cli_steps.config.cli_login_with_token(token=second_user.token)
        expected_error = f'ERROR: Not enough permissions ({{"missing": [{{"uri": "cluster://default/orgs/{org.org_name}/projects/{proj.project_name}/users/{third_user.username}/delete", "action": "write"}}]}})'
        await self._cli_steps.admin.cli_remove_user_from_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            expected_error=expected_error,
        )
        await self._cli_steps.admin.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.admin.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )
