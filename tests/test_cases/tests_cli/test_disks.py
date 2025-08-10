import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.tests_cli.base_cli_test import BaseCLITest


@async_suite("CLI Disks", parent="CLI Tests")
class TestCLIDisks(BaseCLITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._ui_steps = await self.init_ui_test_steps()
        self._cli_steps = await self.init_test_steps()

        # Verify CLI client installed
        await self._cli_steps.verify_cli_client_installed()

    @async_title("Admin create disk with no project created via CLI")
    async def test_admin_create_disk_no_proj_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")

        expected_error = "ERROR: The current project is not selected. Please create one with 'apolo admin add-project', or switch to the existing one with 'apolo config switch-project'."
        disk = self._data_manager.add_disk(
            gherkin_name="First disk",
            org_name=org.org_name,
            owner=user.username,
            storage_amount="1GB",
        )
        await self._cli_steps.cli_create_disk(disk=disk, expected_error=expected_error)

    @async_title("Admin create first disk via CLI")
    async def test_admin_create_first_disk_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        disk = self._data_manager.add_disk(
            gherkin_name="First disk",
            org_name=org.org_name,
            proj_name=proj.project_name,
            owner=user.username,
            storage_amount="1GB",
        )
        await self._cli_steps.cli_create_disk(disk=disk)
        await self._cli_steps.verify_cli_create_disk_output(disk=disk)

        await self._cli_steps.cli_list_disks(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_disk_in_list_disks_output(disk=disk)

    @async_title("Admin create second disk via CLI")
    async def test_admin_create_second_disk_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        disk = self._data_manager.add_disk(
            gherkin_name="First disk",
            org_name=org.org_name,
            proj_name=proj.project_name,
            owner=user.username,
            storage_amount="1GB",
        )
        await self._cli_steps.cli_create_disk(disk=disk)
        await self._cli_steps.verify_cli_create_disk_output(disk=disk)

        second_disk = self._data_manager.add_disk(
            gherkin_name="Second disk",
            org_name=org.org_name,
            proj_name=proj.project_name,
            owner=user.username,
            storage_amount="5GB",
        )
        await self._cli_steps.cli_create_disk(disk=second_disk)
        await self._cli_steps.verify_cli_create_disk_output(disk=second_disk)

        await self._cli_steps.cli_list_disks(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_disk_in_list_disks_output(disk=disk)
        await self._cli_steps.verify_cli_disk_in_list_disks_output(disk=second_disk)

    @async_title("Admin get disk by ID via CLI")
    async def test_admin_get_disk_by_id_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        disk = self._data_manager.add_disk(
            gherkin_name="First disk",
            org_name=org.org_name,
            proj_name=proj.project_name,
            owner=user.username,
            storage_amount="1GB",
        )
        await self._cli_steps.cli_create_disk(disk=disk)
        second_disk = self._data_manager.add_disk(
            gherkin_name="Second disk",
            org_name=org.org_name,
            proj_name=proj.project_name,
            owner=user.username,
            storage_amount="5GB",
        )
        await self._cli_steps.cli_create_disk(disk=second_disk)
        await self._cli_steps.cli_get_disk_by_id(
            org_name=org.org_name, proj_name=proj.project_name, disk_id=disk.id
        )
        await self._cli_steps.verify_cli_create_disk_output(disk=disk)

        await self._cli_steps.cli_get_disk_by_id(
            org_name=org.org_name, proj_name=proj.project_name, disk_id=second_disk.id
        )
        await self._cli_steps.verify_cli_create_disk_output(disk=second_disk)

    @async_title("Admin remove disk by ID via CLI")
    async def test_admin_remove_disk_by_id_cli(self) -> None:
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)

        await self._cli_steps.cli_login_with_token(token=user.token)
        await self._cli_steps.cli_add_new_organization("My-organization", user=user)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj = org.add_project("project 1")
        await self._cli_steps.cli_add_new_project(
            org_name=org.org_name, proj_name=proj.project_name
        )

        disk = self._data_manager.add_disk(
            gherkin_name="First disk",
            org_name=org.org_name,
            proj_name=proj.project_name,
            owner=user.username,
            storage_amount="1GB",
        )
        await self._cli_steps.cli_create_disk(disk=disk)
        second_disk = self._data_manager.add_disk(
            gherkin_name="Second disk",
            org_name=org.org_name,
            proj_name=proj.project_name,
            owner=user.username,
            storage_amount="5GB",
        )
        await self._cli_steps.cli_create_disk(disk=second_disk)
        await self._cli_steps.cli_list_disks(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_disk_in_list_disks_output(disk=disk)
        await self._cli_steps.verify_cli_disk_in_list_disks_output(disk=second_disk)

        await self._cli_steps.cli_remove_disk_by_id(
            org_name=org.org_name, proj_name=proj.project_name, disk_id=disk.id
        )
        await self._cli_steps.cli_list_disks(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await self._cli_steps.verify_cli_disk_not_in_list_disks_output(disk=disk)
        await self._cli_steps.verify_cli_disk_in_list_disks_output(disk=second_disk)
