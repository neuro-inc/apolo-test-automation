import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.tests_cli.base_cli_test import BaseCLITest


@async_suite("CLI Project Remove Members", parent="CLI Tests")
class TestCLIProjectStructureSetup(BaseCLITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._ui_steps = await self.init_ui_test_steps()
        self._cli_steps = await self.init_test_steps()

        # Verify CLI client installed
        await self._cli_steps.verify_cli_client_installed()

    @async_title("Admin change member role from Reader to Writer in project via CLI")
    async def test_admin_change_reader_to_writer_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Reader",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Reader", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Writer",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Writer", email=second_user.email
        )

    @async_title("Admin change member role from Reader to Manager in project via CLI")
    async def test_admin_change_reader_to_manager_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Reader",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Reader", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )

    @async_title("Admin change member role from Reader to Admin in project via CLI")
    async def test_admin_change_reader_to_admin_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Reader",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Reader", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Admin",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Admin", email=second_user.email
        )

    @async_title("Admin change member role from Writer to Reader in project via CLI")
    async def test_admin_change_writer_to_reader_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Writer",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Writer", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Reader",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Reader", email=second_user.email
        )

    @async_title("Admin change member role from Writer to Manager in project via CLI")
    async def test_admin_change_writer_to_manager_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Writer",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Writer", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )

    @async_title("Admin change member role from Writer to Admin in project via CLI")
    async def test_admin_change_writer_to_admin_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Writer",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Writer", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Admin",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Admin", email=second_user.email
        )

    @async_title("Admin change member role from Manager to Reader in project via CLI")
    async def test_admin_change_manager_to_reader_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Reader",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Reader", email=second_user.email
        )

    @async_title("Admin change member role from Manager to Writer in project via CLI")
    async def test_admin_change_manager_to_writer_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Writer",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Writer", email=second_user.email
        )

    @async_title("Admin change member role from Manager to Admin in project via CLI")
    async def test_admin_change_manager_to_admin_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Admin",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Admin", email=second_user.email
        )

    @async_title("Admin change member role from Admin to Reader in project via CLI")
    async def test_admin_change_admin_to_reader_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Admin",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Admin", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Reader",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Reader", email=second_user.email
        )

    @async_title("Admin change member role from Admin to Writer in project via CLI")
    async def test_admin_change_admin_to_writer_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Admin",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Admin", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Writer",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Writer", email=second_user.email
        )

    @async_title("Admin change member role from Admin to Manager in project via CLI")
    async def test_admin_change_admin_to_manager_cli(self) -> None:
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

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Admin",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Admin", email=second_user.email
        )

        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )

    @async_title("Admin demote himself to Manager in project via CLI")
    async def test_admin_demote_himself_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=user.username, role="Admin", email=user.email
        )

        expected_error = (
            "ERROR: Illegal argument(s) (Last project admin cannot be demoted)"
        )
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=user.username,
            role="Manager",
            expected_error=expected_error,
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=user.username, role="Admin", email=user.email
        )

    @async_title("Manager change member role from Reader to Writer in project via CLI")
    async def test_manager_change_reader_to_writer_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Writer",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Writer", email=third_user.email
        )

    @async_title("Manager change member role from Reader to Manager in project via CLI")
    async def test_manager_change_reader_to_manager_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Manager", email=third_user.email
        )

    @async_title("Manager change member role from Reader to Admin in project via CLI")
    async def test_manager_change_reader_to_admin_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        expected_error = f'ERROR: Not enough permissions ({{"missing": [{{"uri": "cluster://default/orgs/{org.org_name}/projects/{proj.project_name}/admins", "action": "write"}}]}})'
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Admin",
            expected_error=expected_error,
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

    @async_title("Manager change member role from Writer to Reader in project via CLI")
    async def test_manager_change_writer_to_reader_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Writer",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Writer", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

    @async_title("Manager change member role from Writer to Manager in project via CLI")
    async def test_manager_change_writer_to_manager_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Writer",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Writer", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

    @async_title("Manager change member role from Writer to Admin in project via CLI")
    async def test_manager_change_writer_to_admin_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Writer",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Writer", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        expected_error = f'ERROR: Not enough permissions ({{"missing": [{{"uri": "cluster://default/orgs/{org.org_name}/projects/{proj.project_name}/admins", "action": "write"}}]}})'
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Admin",
            expected_error=expected_error,
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Writer", email=third_user.email
        )

    @async_title("Manager change member role from Manager to Reader in project via CLI")
    async def test_manager_change_manager_to_reader_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Manager",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Manager", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

    @async_title("Manager change member role from Manager to Writer in project via CLI")
    async def test_manager_change_manager_to_writer_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Manager",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Manager", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Writer",
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Writer", email=third_user.email
        )

    @async_title("Manager change member role from Manager to Admin in project via CLI")
    async def test_manager_change_manager_to_admin_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Manager",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Manager", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        expected_error = f'ERROR: Not enough permissions ({{"missing": [{{"uri": "cluster://default/orgs/{org.org_name}/projects/{proj.project_name}/admins", "action": "write"}}]}})'
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Admin",
            expected_error=expected_error,
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Manager", email=third_user.email
        )

    @async_title("Manager change member role from Admin to Reader in project via CLI")
    async def test_manager_change_admin_to_reader_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Manager",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Admin",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Manager", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Admin", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        expected_error = f'ERROR: Not enough permissions ({{"missing": [{{"uri": "cluster://default/orgs/{org.org_name}/projects/{proj.project_name}/admins", "action": "write"}}]}})'
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
            expected_error=expected_error,
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Admin", email=third_user.email
        )

    @async_title("Writer change member role from Reader to Writer in project via CLI")
    async def test_writer_change_reader_to_writer_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Writer",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Writer", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        expected_error = f'ERROR: Not enough permissions ({{"missing": [{{"uri": "cluster://default/orgs/{org.org_name}/projects/{proj.project_name}/users", "action": "write"}}]}})'
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Writer",
            expected_error=expected_error,
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

    @async_title("Reader change member role from Reader to Writer in project via CLI")
    async def test_reader_change_reader_to_writer_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        u2_ui_steps = await self.init_ui_test_steps()
        second_user = await u2_ui_steps.ui_get_second_user()
        await u2_ui_steps.ui_login(second_user)
        u3_ui_steps = await self.init_ui_test_steps()
        third_user = await u3_ui_steps.ui_get_third_user()
        await u3_ui_steps.ui_login(third_user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=second_user.username, role="User"
        )
        await self._cli_steps.cli_add_user_to_org(
            org_name=org.org_name, username=third_user.username, role="User"
        )

        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=second_user.username,
            role="Reader",
        )
        await self._cli_steps.cli_add_org_member_to_project(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Reader",
        )

        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=second_user.username, role="Reader", email=second_user.email
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )

        await self._cli_steps.cli_login_with_token(token=second_user.token)
        expected_error = f'ERROR: Not enough permissions ({{"missing": [{{"uri": "cluster://default/orgs/{org.org_name}/projects/{proj.project_name}/users", "action": "write"}}]}})'
        await self._cli_steps.cli_update_proj_user_role(
            org_name=org.org_name,
            proj_name=proj.project_name,
            username=third_user.username,
            role="Writer",
            expected_error=expected_error,
        )
        await self._cli_steps.cli_get_proj_users(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_user_in_proj_users_output(
            username=third_user.username, role="Reader", email=third_user.email
        )
