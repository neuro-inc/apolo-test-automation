import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.tests_cli.base_cli_test import BaseCLITest


@async_suite("CLI Project Structure Setup", parent="CLI Tests")
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

    @async_title("User creates a first project via CLI")
    async def test_create_first_project_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)

        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name
        )

        await self._cli_steps.cli_show_config()
        await self._cli_steps.verify_cli_show_command_output(
            expected_username=user.username,
            expected_org=org.org_name,
            expected_project=proj1.project_name,
        )

    @async_title("User verifies admin get-projects command output via CLI")
    async def test_get_projects_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)

        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name,
            proj_name=proj1.project_name,
            default_role="reader",
            default_proj=False,
        )

        await self._cli_steps.cli_run_get_projects(org_name=org.org_name)
        await self._cli_steps.verify_cli_admin_get_projects_output(
            org_name=org.org_name,
            proj_name=proj1.project_name,
            default_role="reader",
            default_proj=False,
        )

    @async_title("User creates a second project via CLI")
    async def test_create_second_project_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)

        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name, default_role="reader"
        )

        await self._cli_steps.cli_show_config()
        await self._cli_steps.verify_cli_show_command_output(
            expected_username=user.username,
            expected_org=org.org_name,
            expected_project=proj1.project_name,
        )

        proj2 = org.add_project("project 2")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj2.project_name, default_role="writer"
        )
        await self._cli_steps.cli_run_get_projects(org_name=org.org_name)
        await self._cli_steps.verify_cli_admin_get_projects_output(
            org_name=org.org_name,
            proj_name=proj1.project_name,
            default_role="reader",
            default_proj=False,
        )
        await self._cli_steps.verify_cli_admin_get_projects_output(
            org_name=org.org_name,
            proj_name=proj2.project_name,
            default_role="writer",
            default_proj=False,
        )

    @async_title("Add user to project via CLI")
    async def test_add_user_to_proj_cli(self) -> None:
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

        proj1 = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name
        )

        await self._apolo_cli.add_proj_user(
            org_name=org.org_name,
            proj_name=proj1.project_name,
            username=second_user.username,
            role="reader",
        )
        await self._cli_steps.cli_login_with_token(token=second_user.token)
        await self._cli_steps.cli_show_config()
        await self._cli_steps.verify_cli_show_command_output(
            expected_username=second_user.username,
            expected_org=org.org_name,
            expected_project=proj1.project_name,
        )
