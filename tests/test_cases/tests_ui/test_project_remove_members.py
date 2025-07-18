import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Project Remove Members", parent="UI Tests")
class TestUIProjectRemoveMembers(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps

    @async_title("Verify Admin can remove Reader from project")
    async def test_admin_remove_reader_from_proj(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Reader role.
        Verify that:
            - Admin can remove Reader from project
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
            role="Reader",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await steps.proj_people_page.ui_click_delete_member_btn(
            username=second_user.username
        )
        await steps.remove_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.remove_proj_member_popup.ui_click_remove_button()
        await steps.remove_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_not_displayed_in_users_list(
            username=second_user.username
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

    @async_title("Verify Admin can remove Writer from project")
    async def test_admin_remove_writer_from_proj(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Writer role.
        Verify that:
            - Admin can remove Writer from project
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

        await steps.proj_people_page.ui_click_delete_member_btn(
            username=second_user.username
        )
        await steps.remove_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.remove_proj_member_popup.ui_click_remove_button()
        await steps.remove_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_not_displayed_in_users_list(
            username=second_user.username
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

    @async_title("Verify Admin can remove Manager from project")
    async def test_admin_remove_manager_from_proj(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Manager role.
        Verify that:
            - Admin can remove Manager from project
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

        await steps.proj_people_page.ui_click_delete_member_btn(
            username=second_user.username
        )
        await steps.remove_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.remove_proj_member_popup.ui_click_remove_button()
        await steps.remove_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_not_displayed_in_users_list(
            username=second_user.username
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

    @async_title("Verify Admin can remove another Admin from project")
    async def test_admin_remove_admin_from_proj(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Admin role.
        Verify that:
            - Admin can remove another Admin from project
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

        await steps.proj_people_page.ui_click_delete_member_btn(
            username=second_user.username
        )
        await steps.remove_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.remove_proj_member_popup.ui_click_remove_button()
        await steps.remove_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_not_displayed_in_users_list(
            username=second_user.username
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

    @async_title("Verify Admin cannot remove himself from project")
    async def test_admin_remove_himself_from_proj(self) -> None:
        """
        Verify that:
            - Admin cannot remove himself from project
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await steps.main_page.ui_click_proj_button_top_pane()
        await steps.proj_info_popup.ui_click_people_btn()

        await steps.proj_people_page.verify_ui_delete_member_btn_disabled(
            username=user.username
        )

    @async_title("Verify Manager can remove Reader from project")
    async def test_manager_remove_reader_from_proj(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Invite member2 to project with Reader role.
        Verify that:
            - Manager can remove Reader from project
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=second_user.email,
            role="User",
        )
        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=third_user.email,
            role="User",
        )

        await u2_steps.ui_reload_page()
        await u3_steps.ui_reload_page()

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

        await u3_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await u3_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
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
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=third_user.email,
            username=third_user.username,
            role="Reader",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u3_steps.ui_reload_page()
        await u3_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_proj_button_top_pane()
        await u2_steps.proj_info_popup.ui_click_people_btn()
        await u2_steps.proj_people_page.ui_click_delete_member_btn(
            username=third_user.username
        )
        await u2_steps.remove_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.remove_proj_member_popup.ui_click_remove_button()
        await u2_steps.remove_org_user_popup.ui_wait_to_disappear(
            username=third_user.username
        )
        await u2_steps.proj_people_page.verify_ui_user_not_displayed_in_users_list(
            username=third_user.username
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

    @async_title("Verify Manager can remove Writer from project")
    async def test_manager_remove_writer_from_proj(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Invite member2 to project with Writer role.
        Verify that:
            - Manager can remove Writer from project
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=second_user.email,
            role="User",
        )
        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=third_user.email,
            role="User",
        )

        await u2_steps.ui_reload_page()
        await u3_steps.ui_reload_page()

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

        await u3_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await u3_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
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
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=third_user.email,
            username=third_user.username,
            role="Writer",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u3_steps.ui_reload_page()
        await u3_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_proj_button_top_pane()
        await u2_steps.proj_info_popup.ui_click_people_btn()
        await u2_steps.proj_people_page.ui_click_delete_member_btn(
            username=third_user.username
        )
        await u2_steps.remove_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.remove_proj_member_popup.ui_click_remove_button()
        await u2_steps.remove_org_user_popup.ui_wait_to_disappear(
            username=third_user.username
        )
        await u2_steps.proj_people_page.verify_ui_user_not_displayed_in_users_list(
            username=third_user.username
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

    @async_title("Verify Manager can remove another Manager from project")
    async def test_manager_remove_manager_from_proj(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Invite member2 to project with Manager role.
        Verify that:
            - Manager can remove another Manager from project
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=second_user.email,
            role="User",
        )
        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=third_user.email,
            role="User",
        )

        await u2_steps.ui_reload_page()
        await u3_steps.ui_reload_page()

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

        await u3_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await u3_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
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
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=third_user.email,
            username=third_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u3_steps.ui_reload_page()
        await u3_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_proj_button_top_pane()
        await u2_steps.proj_info_popup.ui_click_people_btn()
        await u2_steps.proj_people_page.ui_click_delete_member_btn(
            username=third_user.username
        )
        await u2_steps.remove_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.remove_proj_member_popup.ui_click_remove_button()
        await u2_steps.remove_org_user_popup.ui_wait_to_disappear(
            username=third_user.username
        )
        await u2_steps.proj_people_page.verify_ui_user_not_displayed_in_users_list(
            username=third_user.username
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

    @async_title("Verify Manager cannot remove Admin from project")
    async def test_manager_remove_admin_from_proj(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Invite member2 to project with Admin role.
        Verify that:
            - Manager cannot remove Admin from project
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=second_user.email,
            role="User",
        )
        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=third_user.email,
            role="User",
        )

        await u2_steps.ui_reload_page()
        await u3_steps.ui_reload_page()

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

        await u3_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await u3_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
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
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=third_user.email,
            username=third_user.username,
            role="Admin",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u3_steps.ui_reload_page()
        await u3_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_proj_button_top_pane()
        await u2_steps.proj_info_popup.ui_click_people_btn()
        await u2_steps.proj_people_page.ui_click_delete_member_btn(
            username=third_user.username
        )
        await u2_steps.remove_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.remove_proj_member_popup.ui_click_remove_button()
        await u2_steps.ui_wait_for_timeout(1000)

        await u2_steps.remove_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )
        await u2_steps.ui_reload_page()
        await u2_steps.proj_people_page.verify_ui_user_displayed_in_users_list(
            username=third_user.username
        )

        await u3_steps.ui_reload_page()
        await u3_steps.apps_page.verify_ui_page_displayed()

    @async_title("Verify Manager cannot remove himself from project")
    async def test_manager_remove_himself_from_proj(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Manager role.
        Verify that:
            - Manager cannot remove himself from project
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

        await u2_steps.main_page.ui_click_proj_button_top_pane()
        await u2_steps.proj_info_popup.ui_click_people_btn()

        await u2_steps.proj_people_page.verify_ui_delete_member_btn_disabled(
            username=second_user.username
        )

    @async_title("Verify Writer cannot remove members from project")
    async def test_writer_remove_reader_from_proj(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Writer role.
        Invite member2 to project with Reader role.
        Verify that:
            - Writer cannot remove members from project
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=second_user.email,
            role="User",
        )
        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=third_user.email,
            role="User",
        )

        await u2_steps.ui_reload_page()
        await u3_steps.ui_reload_page()

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

        await u3_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await u3_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
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
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=third_user.email,
            username=third_user.username,
            role="Reader",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u3_steps.ui_reload_page()
        await u3_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_proj_button_top_pane()
        await u2_steps.proj_info_popup.ui_click_people_btn()
        await u2_steps.proj_people_page.verify_ui_delete_member_btn_disabled(
            username=third_user.username
        )

    @async_title("Verify Reader cannot remove members from project")
    async def test_reader_remove_reader_from_proj(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Reader role.
        Invite member2 to project with Reader role.
        Verify that:
            - Reader cannot remove members from project
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=second_user.email,
            role="User",
        )
        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=third_user.email,
            role="User",
        )

        await u2_steps.ui_reload_page()
        await u3_steps.ui_reload_page()

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

        await u3_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await u3_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
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
            role="Reader",
        )
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=third_user.email,
            username=third_user.username,
            role="Reader",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u3_steps.ui_reload_page()
        await u3_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_proj_button_top_pane()
        await u2_steps.proj_info_popup.ui_click_people_btn()
        await u2_steps.proj_people_page.verify_ui_delete_member_btn_disabled(
            username=third_user.username
        )
