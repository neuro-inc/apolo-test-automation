import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.base_test_class import BaseTestClass


@async_suite("UI Disks", parent="UI Tests")
class TestUIDisks(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_ui_test_steps()
        self._steps: UISteps = steps

    @async_title("Create First Disk without project via UI")
    async def test_create_first_disk_no_project_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.

        ### Verify that:

        - User **cannot** create first Disk if **no project created** yet.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        await steps.main_page.ui_click_disks_btn()
        await steps.disks_page.verify_ui_page_not_displayed()
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.main_page.verify_ui_create_project_message_displayed(
            org_name=org.org_name
        )

    @async_title("Create First Disk via UI")
    async def test_create_first_disk_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.

        ### Verify that:

        - User can create first Disk after project created.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj = org.add_project(gherkin_name="Default-project")
        await steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )
        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_disk(
            disk_name="first-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
        )
        await steps.disks_page.verify_ui_disk_row_displayed(disk_name="first-disk")

    @async_title("Create Second Disk via UI")
    async def test_create_second_disk_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.
        - Create new Disk.

        ### Verify that:

        - User can create second Disk.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")
        await steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )
        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_disk(
            disk_name="first-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
        )
        await steps.disks_page.verify_ui_disk_row_displayed(disk_name="first-disk")

        await steps.ui_create_disk(
            disk_name="second-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
            first_disk=False,
        )
        await steps.disks_page.verify_ui_disk_row_displayed(disk_name="first-disk")
        await steps.disks_page.verify_ui_disk_row_displayed(disk_name="second-disk")

    @async_title("Search Disk via UI")
    async def test_search_disk_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.
        - Create new Disk.
        - Create second Disk.

        ### Verify that:

        - User can search for Disk via UI with the `Search` field.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")
        await steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )
        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_disk(
            disk_name="first-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
        )
        await steps.disks_page.verify_ui_disk_row_displayed(disk_name="first-disk")

        await steps.ui_create_disk(
            disk_name="second-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
            first_disk=False,
        )
        await steps.disks_page.verify_ui_disk_row_displayed(disk_name="first-disk")
        await steps.disks_page.verify_ui_disk_row_displayed(disk_name="second-disk")

        await steps.disks_page.ui_enter_disk_name_into_search_input(
            disk_name="second-disk"
        )
        await steps.disks_page.verify_ui_disk_row_not_displayed(disk_name="first-disk")
        await steps.disks_page.verify_ui_disk_row_displayed(disk_name="second-disk")

    @async_title("Open Disk info view by click on disk button")
    async def test_disk_info_view_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.
        - Create new Disk.

        ### Verify that:

        - After click on disk button Disk info view appears.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")
        await steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )
        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_disk(
            disk_name="first-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
        )
        await steps.disks_page.verify_ui_disk_row_displayed(disk_name="first-disk")

        await steps.disks_page.verify_ui_valid_disk_info_displayed(
            disk_name="first-disk",
            owner=user.username,
            storage_value="1GB",
        )

    @async_title("Delete Disk via UI")
    async def test_delete_disk_via_ui(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Create new project via **API**.
        - Create new Disk.

        ### Verify that:

        - User can delete Disk.
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")
        await steps.ui_add_proj_api(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            default_role="reader",
            proj_default=False,
        )
        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_disk(
            disk_name="first-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
        )
        await steps.disks_page.verify_ui_disk_row_displayed(disk_name="first-disk")

        await steps.disks_page.verify_ui_valid_disk_info_displayed(
            disk_name="first-disk",
            owner=user.username,
            storage_value="1GB",
        )

        await steps.disks_page.ui_click_delete_disk_btn(disk_name="first-disk")
        await steps.delete_disk_popup.verify_ui_popup_displayed(disk_name="first-disk")

        await steps.delete_disk_popup.ui_click_delete_btn()
        await steps.delete_disk_popup.ui_wait_to_disappear(disk_name="first-disk")
        await steps.disks_page.verify_ui_disk_row_not_displayed(disk_name="first-disk")
        await steps.disks_page.verify_ui_no_disks_message_displayed()
