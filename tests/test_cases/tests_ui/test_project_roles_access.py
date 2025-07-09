import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Project Roles Access", parent="UI Tests")
class TestUIProjectRolesAccess(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps
        self._user = self._users_manager.default_user

    @async_title("Verify Reader cannot modify files")
    async def test_reader_modify_files(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Reader role.
        Verify that:
            - Reader doesn't have access to modify Files
        """

        user = self._user
        steps = self._steps
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

        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_disabled()
        await u2_steps.files_page.verify_ui_upload_btn_disabled()

    @async_title("Verify Writer can modify files")
    async def test_writer_modify_files(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Writer role.
        Verify that:
            - Writer has access to modify Files
        """

        user = self._user
        steps = self._steps
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

        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_enabled()
        await u2_steps.files_page.verify_ui_upload_btn_enabled()

    @async_title("Verify Manager can modify files")
    async def test_manager_modify_files(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member1 to project with Manager role.
        Verify that:
            - Manager has access to modify Files
        """

        user = self._user
        steps = self._steps
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

        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_enabled()
        await u2_steps.files_page.verify_ui_upload_btn_enabled()

    @async_title("Verify Manager can invite Reader to a project")
    async def test_manager_invite_reader_to_project(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Verify that:
            - Manager can invite Reader to a project
        """

        user = self._user
        steps = self._steps
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
        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()
        await u2_steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=third_user.email,
            username=third_user.username,
            role="Reader",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.apps_page.verify_ui_page_displayed()

    @async_title("Verify Manager can invite Writer to a project")
    async def test_manager_invite_writer_to_project(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Verify that:
            - Manager can invite Writer to a project
        """

        user = self._user
        steps = self._steps
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
        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()
        await u2_steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=third_user.email,
            username=third_user.username,
            role="Writer",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.apps_page.verify_ui_page_displayed()

    @async_title("Verify Manager can invite Manager to a project")
    async def test_manager_invite_manager_to_project(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Verify that:
            - Manager can invite Manager to a project
        """

        user = self._user
        steps = self._steps
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
        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()
        await u2_steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=third_user.email,
            username=third_user.username,
            role="Manager",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.apps_page.verify_ui_page_displayed()

    @async_title("Verify Manager cannot invite Admin to a project")
    async def test_manager_invite_admin_to_project(self) -> None:
        """
        Invite member1 to organization with User role.
        Invite member2 to organization with User role.
        Invite member1 to project with Manager role.
        Verify that:
            - Manager cannot invite Admin to a project
        """

        user = self._user
        steps = self._steps
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
        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_proj_button_top_pane()
        await u2_steps.proj_info_popup.ui_click_people_btn()
        await u2_steps.proj_people_page.verify_ui_page_displayed()

        await u2_steps.proj_people_page.ui_click_invite_people_proj_people_btn()
        await u2_steps.invite_proj_member_popup.verify_ui_popup_displayed(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await u2_steps.invite_proj_member_popup.ui_enter_user_data(
            email=third_user.email
        )
        await u2_steps.invite_proj_member_popup.ui_select_user_role(role="Admin")
        await u2_steps.invite_proj_member_popup.verify_ui_invite_user_btn_displayed(
            email=third_user.email
        )
        await u2_steps.invite_proj_member_popup.verify_ui_invite_bth_disabled()

        await u2_steps.invite_proj_member_popup.ui_click_invite_user_btn(
            email=third_user.email
        )
        await u2_steps.invite_proj_member_popup.verify_ui_invite_bth_enabled()

        await u2_steps.invite_proj_member_popup.ui_click_invite_btn()
        await u2_steps._pm.page.wait_for_timeout(2000)
        await u2_steps.invite_proj_member_popup.verify_ui_popup_displayed(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.proj_people_page.verify_ui_user_not_displayed_in_users_list(
            username=third_user.username
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org_name=org.org_name
        )
