import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Project Change Member Roles", parent="UI Tests")
class TestUIProjectChangeMemberRoles(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps

    @async_title("Verify Admin can promote Reader to Writer")
    async def test_admin_change_reader_to_writer(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Reader role.
        Verify that:
            - Admin can promote Reader to Writer
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Writer")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Writer"
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_enabled()
        await u2_steps.files_page.verify_ui_upload_btn_enabled()

    @async_title("Verify Admin can promote Reader to Manager")
    async def test_admin_change_reader_to_manager(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Reader role.
        Verify that:
            - Admin can promote Reader to Manager
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Manager")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Manager"
        )

    @async_title("Verify Admin can promote Reader to Admin")
    async def test_admin_change_reader_to_admin(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Reader role.
        Verify that:
            - Admin can promote Reader to Admin
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Admin")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Admin"
        )

    @async_title("Verify Admin can demote Writer to Reader")
    async def test_admin_change_writer_to_reader(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Writer role.
        Verify that:
            - Admin can demote Writer to Reader
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Reader")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Reader"
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_disabled()
        await u2_steps.files_page.verify_ui_upload_btn_disabled()

    @async_title("Verify Admin can promote Writer to Manager")
    async def test_admin_change_writer_to_manager(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Writer role.
        Verify that:
            - Admin can promote Writer to Manager
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Manager")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Manager"
        )

    @async_title("Verify Admin can promote Writer to Admin")
    async def test_admin_change_writer_to_admin(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Writer role.
        Verify that:
            - Admin can promote Writer to Admin
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Admin")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Admin"
        )

    @async_title("Verify Admin can demote Manager to Reader")
    async def test_admin_change_manager_to_reader(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Manager role.
        Verify that:
            - Admin can demote Manager to Reader
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Reader")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Reader"
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_disabled()
        await u2_steps.files_page.verify_ui_upload_btn_disabled()

    @async_title("Verify Admin can demote Manager to Writer")
    async def test_admin_change_manager_to_writer(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Manager role.
        Verify that:
            - Admin can demote Manager to Writer
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Writer")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Writer"
        )

    @async_title("Verify Admin can promote Manager to Admin")
    async def test_admin_change_manager_to_admin(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Manager role.
        Verify that:
            - Admin can promote Manager to Admin
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Admin")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Admin"
        )

    @async_title("Verify Admin can demote Admin to Reader")
    async def test_admin_change_admin_to_reader(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Admin role.
        Verify that:
            - Admin can demote Admin to Reader
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Reader")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Reader"
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_disabled()
        await u2_steps.files_page.verify_ui_upload_btn_disabled()

    @async_title("Verify Admin can demote Admin to Writer")
    async def test_admin_change_admin_to_writer(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Admin role.
        Verify that:
            - Admin can demote Admin to Writer
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Writer")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Writer"
        )

    @async_title("Verify Admin can demote Admin to Manager")
    async def test_admin_change_admin_to_manager(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Admin role.
        Verify that:
            - Admin can demote Admin to Manager
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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

        await steps.proj_people_page.ui_click_edit_member_btn(
            username=second_user.username
        )
        await steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_proj_member_popup.ui_select_new_user_role(role="Manager")
        await steps.edit_proj_member_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Manager"
        )

    @async_title("Verify Manager can promote Reader to Writer")
    async def test_manager_change_reader_to_writer(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Invite member2 to project with Reader role.
        Verify that:
            - Manager can promote Reader to Writer
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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
        await u2_steps.proj_people_page.ui_click_edit_member_btn(
            username=third_user.username
        )
        await u2_steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_proj_member_popup.ui_select_new_user_role(role="Writer")
        await u2_steps.edit_proj_member_popup.ui_click_save_button()
        await u2_steps.edit_org_user_popup.ui_wait_to_disappear(
            username=third_user.username
        )
        await u2_steps.proj_people_page.verify_ui_user_role(
            username=third_user.username, role="Writer"
        )

        await u3_steps._pm.page.wait_for_timeout(3000)
        await u3_steps.ui_reload_page()
        await u3_steps.main_page.ui_click_files_btn()
        await u3_steps.files_page.verify_ui_page_displayed()
        await u3_steps.files_page.verify_ui_add_folder_btn_enabled()
        await u3_steps.files_page.verify_ui_upload_btn_enabled()

    @async_title("Verify Manager can promote Reader to Manager")
    async def test_manager_change_reader_to_manager(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Invite member2 to project with Reader role.
        Verify that:
            - Manager can promote Reader to Manager
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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
        await u2_steps.proj_people_page.ui_click_edit_member_btn(
            username=third_user.username
        )
        await u2_steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_proj_member_popup.ui_select_new_user_role(role="Manager")
        await u2_steps.edit_proj_member_popup.ui_click_save_button()
        await u2_steps.edit_org_user_popup.ui_wait_to_disappear(
            username=third_user.username
        )
        await u2_steps.proj_people_page.verify_ui_user_role(
            username=third_user.username, role="Manager"
        )

    @async_title("Verify Manager cannot promote Reader to Admin")
    async def test_manager_change_reader_to_admin(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Invite member2 to project with Reader role.
        Verify that:
            - Manager cannot promote Reader to Admin
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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
        await u2_steps.proj_people_page.ui_click_edit_member_btn(
            username=third_user.username
        )
        await u2_steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_proj_member_popup.ui_select_new_user_role(role="Admin")
        await u2_steps.edit_proj_member_popup.ui_click_save_button()
        await u2_steps._pm.page.wait_for_timeout(2000)
        await u2_steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )
        await u2_steps.ui_reload_page()
        await u2_steps.proj_people_page.verify_ui_user_role(
            username=third_user.username, role="Reader"
        )

    @async_title("Verify Manager can demote Writer to Reader")
    async def test_manager_change_writer_to_reader(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Invite member2 to project with Writer role.
        Verify that:
            - Manager can demote Writer to Reader
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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
        await u2_steps.proj_people_page.ui_click_edit_member_btn(
            username=third_user.username
        )
        await u2_steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_proj_member_popup.ui_select_new_user_role(role="Reader")
        await u2_steps.edit_proj_member_popup.ui_click_save_button()
        await u2_steps.edit_org_user_popup.ui_wait_to_disappear(
            username=third_user.username
        )
        await u2_steps.proj_people_page.verify_ui_user_role(
            username=third_user.username, role="Reader"
        )

        await u3_steps._pm.page.wait_for_timeout(3000)
        await u3_steps.ui_reload_page()
        await u3_steps.main_page.ui_click_files_btn()
        await u3_steps.files_page.verify_ui_page_displayed()
        await u3_steps.files_page.verify_ui_add_folder_btn_disabled()
        await u3_steps.files_page.verify_ui_upload_btn_disabled()

    @async_title("Verify Manager can promote Writer to Manager")
    async def test_manager_change_writer_to_manager(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Invite member2 to project with Writer role.
        Verify that:
            - Manager can promote Writer to Manager
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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
        await u2_steps.proj_people_page.ui_click_edit_member_btn(
            username=third_user.username
        )
        await u2_steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_proj_member_popup.ui_select_new_user_role(role="Manager")
        await u2_steps.edit_proj_member_popup.ui_click_save_button()
        await u2_steps.edit_org_user_popup.ui_wait_to_disappear(
            username=third_user.username
        )
        await u2_steps.proj_people_page.verify_ui_user_role(
            username=third_user.username, role="Manager"
        )

    @async_title("Verify Manager cannot promote Writer to Admin")
    async def test_manager_change_writer_to_admin(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Invite member2 to project with Writer role.
        Verify that:
            - Manager cannot promote Writer to Admin
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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
        await u2_steps.proj_people_page.ui_click_edit_member_btn(
            username=third_user.username
        )
        await u2_steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_proj_member_popup.ui_select_new_user_role(role="Admin")
        await u2_steps.edit_proj_member_popup.ui_click_save_button()
        await u2_steps._pm.page.wait_for_timeout(2000)
        await u2_steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )
        await u2_steps.ui_reload_page()
        await u2_steps.proj_people_page.verify_ui_user_role(
            username=third_user.username, role="Writer"
        )

    @async_title("Verify Manager cannot demote Admin")
    async def test_manager_change_admin_to_manager(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Invite member2 to project with Admin role.
        Verify that:
            - Manager cannot demote Admin to Manager
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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
        await u2_steps.proj_people_page.ui_click_edit_member_btn(
            username=third_user.username
        )
        await u2_steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_proj_member_popup.ui_select_new_user_role(role="Manager")
        await u2_steps.edit_proj_member_popup.ui_click_save_button()
        await u2_steps._pm.page.wait_for_timeout(2000)
        await u2_steps.edit_proj_member_popup.verify_ui_popup_displayed(
            username=third_user.username
        )
        await u2_steps.ui_reload_page()
        await u2_steps.proj_people_page.verify_ui_user_role(
            username=third_user.username, role="Admin"
        )

    @async_title("Verify Writer cannot change member roles")
    async def test_writer_change_role(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Writer role.
        Invite member2 to project with Reader role.
        Verify that:
            - Writer cannot change member roles
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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
        await u2_steps.proj_people_page.verify_ui_edit_member_btn_disabled(
            username=third_user.username
        )

    @async_title("Verify Reader cannot change member roles")
    async def test_reader_change_role(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Writer role.
        Invite member2 to project with Reader role.
        Verify that:
            - Reader cannot change member roles
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        third_user = await u3_steps.ui_signup_new_user_ver_link()

        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        await steps.ui_pass_new_user_onboarding(
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
        await u2_steps.proj_people_page.verify_ui_edit_member_btn_disabled(
            username=third_user.username
        )
