import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Disks", parent="UI Tests")
class TestUIDisks(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps

    @async_title("Create First Disk without project via UI")
    async def test_create_first_disk_no_project_via_ui(self) -> None:
        """
        Verify that:
            - User cannot create first Disk if no project created yet
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_pass_new_user_onboarding(
            user=user,
            gherkin_name="Default-organization",
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
        Verify that:
            - User can create first Disk after project created
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_pass_new_user_onboarding(
            user=user,
            gherkin_name="Default-organization",
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")

        await steps.main_page.ui_click_create_proj_button_main_page()
        await steps.create_proj_popup.verify_ui_popup_displayed(org.org_name)

        await steps.create_proj_popup.ui_enter_proj_name(proj.project_name)
        await steps.create_proj_popup.ui_select_role("Reader")
        await steps.create_proj_popup.ui_click_create_button()
        await steps.create_proj_popup.ui_wait_to_disappear(org_name=org.org_name)

        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_disk(
            disk_name="first-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
        )
        await steps.disks_page.verify_ui_disk_btn_displayed(disk_name="first-disk")

    @async_title("Create Second Disk via UI")
    async def test_create_second_disk_via_ui(self) -> None:
        """
        Verify that:
            - User can create second Disk
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_pass_new_user_onboarding(
            user=user,
            gherkin_name="Default-organization",
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")

        await steps.main_page.ui_click_create_proj_button_main_page()
        await steps.create_proj_popup.verify_ui_popup_displayed(org.org_name)

        await steps.create_proj_popup.ui_enter_proj_name(proj.project_name)
        await steps.create_proj_popup.ui_select_role("Reader")
        await steps.create_proj_popup.ui_click_create_button()
        await steps.create_proj_popup.ui_wait_to_disappear(org_name=org.org_name)

        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_disk(
            disk_name="first-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
        )
        await steps.disks_page.verify_ui_disk_btn_displayed(disk_name="first-disk")

        await steps.ui_create_disk(
            disk_name="second-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
            first_disk=False,
        )
        await steps.disks_page.verify_ui_disk_btn_displayed(disk_name="first-disk")
        await steps.disks_page.verify_ui_disk_btn_displayed(disk_name="second-disk")

    @async_title("Search Disk via UI")
    async def test_search_disk_via_ui(self) -> None:
        """
        Verify that:
            - User can search for Disk
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_pass_new_user_onboarding(
            user=user,
            gherkin_name="Default-organization",
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")

        await steps.main_page.ui_click_create_proj_button_main_page()
        await steps.create_proj_popup.verify_ui_popup_displayed(org.org_name)

        await steps.create_proj_popup.ui_enter_proj_name(proj.project_name)
        await steps.create_proj_popup.ui_select_role("Reader")
        await steps.create_proj_popup.ui_click_create_button()
        await steps.create_proj_popup.ui_wait_to_disappear(org_name=org.org_name)

        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_disk(
            disk_name="first-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
        )
        await steps.disks_page.verify_ui_disk_btn_displayed(disk_name="first-disk")

        await steps.ui_create_disk(
            disk_name="second-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
            first_disk=False,
        )
        await steps.disks_page.verify_ui_disk_btn_displayed(disk_name="first-disk")
        await steps.disks_page.verify_ui_disk_btn_displayed(disk_name="second-disk")

        await steps.disks_page.ui_enter_disk_name_into_search_input(
            disk_name="second-disk"
        )
        await steps.disks_page.verify_ui_disk_btn_not_displayed(disk_name="first-disk")
        await steps.disks_page.verify_ui_disk_btn_displayed(disk_name="second-disk")

    @async_title("Open Disk info view by click on disk button")
    async def test_disk_info_view_via_ui(self) -> None:
        """
        Verify that:
            - After click on disk button Disk info view appears
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_pass_new_user_onboarding(
            user=user,
            gherkin_name="Default-organization",
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")

        await steps.main_page.ui_click_create_proj_button_main_page()
        await steps.create_proj_popup.verify_ui_popup_displayed(org.org_name)

        await steps.create_proj_popup.ui_enter_proj_name(proj.project_name)
        await steps.create_proj_popup.ui_select_role("Reader")
        await steps.create_proj_popup.ui_click_create_button()
        await steps.create_proj_popup.ui_wait_to_disappear(org_name=org.org_name)

        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_disk(
            disk_name="first-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
        )
        await steps.disks_page.verify_ui_disk_btn_displayed(disk_name="first-disk")

        await steps.disks_page.ui_click_disk_btn(disk_name="first-disk")
        await steps.disks_page.verify_ui_disk_info_view_displayed(
            disk_name="first-disk",
            owner=user.username,
            storage_value="1GB",
            lifespan_value="1d",
        )

    @async_title("Delete Disk via UI")
    async def test_delete_disk_via_ui(self) -> None:
        """
        Verify that:
            - User can delete Disk
        """
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_pass_new_user_onboarding(
            user=user,
            gherkin_name="Default-organization",
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")

        await steps.main_page.ui_click_create_proj_button_main_page()
        await steps.create_proj_popup.verify_ui_popup_displayed(org.org_name)

        await steps.create_proj_popup.ui_enter_proj_name(proj.project_name)
        await steps.create_proj_popup.ui_select_role("Reader")
        await steps.create_proj_popup.ui_click_create_button()
        await steps.create_proj_popup.ui_wait_to_disappear(org_name=org.org_name)

        await steps.apps_page.verify_ui_page_displayed()

        await steps.ui_create_disk(
            disk_name="first-disk",
            storage_value="1",
            storage_units="GB",
            lifespan_value="1d",
        )
        await steps.disks_page.verify_ui_disk_btn_displayed(disk_name="first-disk")

        await steps.disks_page.ui_click_disk_btn(disk_name="first-disk")
        await steps.disks_page.verify_ui_disk_info_view_displayed(
            disk_name="first-disk",
            owner=user.username,
            storage_value="1GB",
            lifespan_value="1d",
        )

        await steps.disks_page.ui_click_delete_disk_btn()
        await steps.delete_disk_popup.verify_ui_popup_displayed(disk_name="first-disk")

        await steps.delete_disk_popup.ui_click_delete_btn()
        await steps.delete_disk_popup.ui_wait_to_disappear(disk_name="first-disk")
        await steps.disks_page.verify_ui_disk_btn_not_displayed(disk_name="first-disk")
        await steps.disks_page.verify_ui_no_disks_message_displayed()
