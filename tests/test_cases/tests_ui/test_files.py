import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Files", parent="UI Tests")
class TestUIFiles(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps

    @async_title("Verify Writer can create new folder")
    async def test_writer_create_folder(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Writer role.
        Verify that:
            - Writer can create new folder
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=second_user.email,
            role="User",
        )

        await u2_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=second_user.email,
            username=second_user.username,
            role="Writer",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_enabled()

        await u2_steps.files_page.ui_click_add_folder_btn()
        await u2_steps.new_folder_popup.verify_ui_popup_displayed()

        await u2_steps.new_folder_popup.ui_enter_folder_name(name="New Folder 1")
        await u2_steps.new_folder_popup.ui_click_create_btn()
        await u2_steps.new_folder_popup.ui_wait_to_disappear()

        await u2_steps.files_page.verify_ui_folder_displayed(name="New Folder 1")

    @async_title("Verify Manager can create new folder")
    async def test_manager_create_folder(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Manager role.
        Verify that:
            - Manager can create new folder
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=second_user.email,
            role="User",
        )

        await u2_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=second_user.email,
            username=second_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_enabled()

        await u2_steps.files_page.ui_click_add_folder_btn()
        await u2_steps.new_folder_popup.verify_ui_popup_displayed()

        await u2_steps.new_folder_popup.ui_enter_folder_name(name="New Folder 1")
        await u2_steps.new_folder_popup.ui_click_create_btn()
        await u2_steps.new_folder_popup.ui_wait_to_disappear()

        await u2_steps.files_page.verify_ui_folder_displayed(name="New Folder 1")

    @async_title("Verify Admin can create new folder")
    async def test_admin_create_folder(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Admin role.
        Verify that:
            - Admin can create new folder
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=second_user.email,
            role="User",
        )

        await u2_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=second_user.email,
            username=second_user.username,
            role="Admin",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_enabled()

        await u2_steps.files_page.ui_click_add_folder_btn()
        await u2_steps.new_folder_popup.verify_ui_popup_displayed()

        await u2_steps.new_folder_popup.ui_enter_folder_name(name="New Folder 1")
        await u2_steps.new_folder_popup.ui_click_create_btn()
        await u2_steps.new_folder_popup.ui_wait_to_disappear()

        await u2_steps.files_page.verify_ui_folder_displayed(name="New Folder 1")
