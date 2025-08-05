import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Project Structure Setup", parent="UI Tests")
class TestUIProjectStructureSetup(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps

    @async_title("Create First Project from main page via UI")
    async def test_create_first_proj_main_page_via_ui(self) -> None:
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
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

        await steps.main_page.ui_click_proj_button_top_pane()
        await steps.proj_info_popup.verify_ui_popup_displayed(
            proj_name=proj.project_name
        )

    @async_title("Create First Project from top pane of main via UI")
    async def test_create_first_proj_top_pane_via_ui(self) -> None:
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj = org.add_project("Default-project")

        await steps.main_page.ui_click_proj_button_top_pane()
        await steps.no_proj_popup.verify_ui_popup_displayed(org.org_name)

        await steps.no_proj_popup.ui_click_create_new_proj_button()

        await steps.create_proj_popup.verify_ui_popup_displayed(org.org_name)

        await steps.create_proj_popup.ui_enter_proj_name(proj.project_name)
        await steps.create_proj_popup.ui_select_role("Reader")
        await steps.create_proj_popup.ui_click_create_button()
        await steps.create_proj_popup.ui_wait_to_disappear(org_name=org.org_name)

        await steps.apps_page.verify_ui_page_displayed()

        await steps.main_page.ui_click_proj_button_top_pane()
        await steps.proj_info_popup.verify_ui_popup_displayed(
            proj_name=proj.project_name
        )

    @async_title("Create second project via UI")
    async def test_create_second_proj_via_ui(self) -> None:
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj1 = org.add_project("project 1")

        await steps.ui_create_first_proj_from_main_page(
            org_name=org.org_name, proj_name=proj1.project_name, default_role="Reader"
        )

        await steps.main_page.ui_click_proj_button_top_pane()
        await steps.proj_info_popup.verify_ui_popup_displayed(
            proj_name=proj1.project_name
        )

        proj2 = org.add_project("Project2")
        await steps.proj_info_popup.ui_click_create_new_proj_button()

        await steps.create_proj_popup.verify_ui_popup_displayed(org.org_name)

        await steps.create_proj_popup.ui_enter_proj_name(proj2.project_name)
        await steps.create_proj_popup.ui_select_role("Reader")
        await steps.create_proj_popup.ui_click_create_button()
        await steps.create_proj_popup.ui_wait_to_disappear(org_name=org.org_name)

        await steps.apps_page.verify_ui_page_displayed()

        await steps.main_page.ui_click_proj_button_top_pane()
        await steps.proj_info_popup.verify_ui_popup_displayed(
            proj_name=proj2.project_name
        )
        await steps.proj_info_popup.verify_ui_other_proj_displayed_in_info(
            proj_name=proj1.project_name
        )

    @async_title("Invite member of organization to project via UI")
    async def test_invite_org_member_to_proj_via_ui(self) -> None:
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj1 = org.add_project("project 1")

        await steps.ui_create_first_proj_from_main_page(
            org_name=org.org_name, proj_name=proj1.project_name, default_role="Reader"
        )

        u2_steps = await self.init_test_steps()
        self.log("User2 login")
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        self.log("User1 invite User2 to organization")
        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=second_user.email
        )

        self.log("User 2 accept invite to organization")
        await u2_steps.ui_reload_page()
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "user"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        await u2_steps.main_page.verify_ui_create_project_button_displayed()

        self.log(f"User1 invite User2 to project {proj1.project_name}")
        await steps.main_page.ui_click_proj_button_top_pane()
        await steps.proj_info_popup.ui_click_people_btn()
        await steps.proj_people_page.verify_ui_page_displayed()

        await steps.proj_people_page.ui_click_invite_people_proj_people_btn()
        await steps.invite_proj_member_popup.verify_ui_popup_displayed(
            org_name=org.org_name, proj_name=proj1.project_name
        )

        await steps.invite_proj_member_popup.ui_enter_user_data(email=second_user.email)
        await steps.invite_proj_member_popup.ui_select_user_role(role="Reader")
        await steps.invite_proj_member_popup.verify_ui_invite_user_btn_displayed(
            email=second_user.email
        )
        await steps.invite_proj_member_popup.verify_ui_invite_bth_disabled()

        await steps.invite_proj_member_popup.ui_click_invite_user_btn(
            email=second_user.email
        )
        await steps.invite_proj_member_popup.verify_ui_invite_bth_enabled()

        await steps.invite_proj_member_popup.ui_click_invite_btn()
        await steps.invite_proj_member_popup.ui_wait_to_disappear(
            org_name=org.org_name, proj_name=proj1.project_name
        )
        await steps.proj_people_page.verify_ui_page_displayed()
        await steps.proj_people_page.verify_ui_user_displayed_in_users_list(
            username=second_user.username
        )
        await steps.proj_people_page.verify_ui_user_role(
            username=second_user.username, role="Reader"
        )
        await steps.proj_people_page.verify_ui_invited_user_email(
            username=second_user.username, email=second_user.email
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_proj_button_top_pane()
        await u2_steps.proj_info_popup.verify_ui_popup_displayed(
            proj_name=proj1.project_name
        )

    @async_title("Invite member that NOT in organization to project via UI")
    async def test_invite_not_org_member_to_proj_via_ui(self) -> None:
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj1 = org.add_project("project 1")

        await steps.ui_create_first_proj_from_main_page(
            org_name=org.org_name, proj_name=proj1.project_name, default_role="Reader"
        )

        self.log(f"User1 invite User2 to project {proj1.project_name}")
        await steps.main_page.ui_click_proj_button_top_pane()
        await steps.proj_info_popup.ui_click_people_btn()
        await steps.proj_people_page.verify_ui_page_displayed()

        await steps.proj_people_page.ui_click_invite_people_proj_people_btn()
        await steps.invite_proj_member_popup.verify_ui_popup_displayed(
            org_name=org.org_name, proj_name=proj1.project_name
        )

        u2_steps = await self.init_test_steps()
        self.log("User2 login")
        second_user = await u2_steps.ui_signup_new_user_ver_link()
        self.log("User2 password new user onboarding and create organization")
        await u2_steps.ui_pass_new_user_onboarding(
            user=second_user,
            gherkin_name="new-organization",
        )

        await steps.invite_proj_member_popup.ui_enter_user_data(email=second_user.email)
        await steps.invite_proj_member_popup.ui_select_user_role(role="Reader")
        await steps.invite_proj_member_popup.verify_ui_invite_user_btn_not_displayed(
            email=second_user.email
        )

    @async_title("Invite not registered user to project via UI")
    async def test_invite_not_registered_to_proj_via_ui(self) -> None:
        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )

        org = self._data_manager.default_organization
        proj1 = org.add_project("project 1")

        await steps.ui_create_first_proj_from_main_page(
            org_name=org.org_name, proj_name=proj1.project_name, default_role="Reader"
        )

        self.log(f"User1 invite User2 to project {proj1.project_name}")
        await steps.main_page.ui_click_proj_button_top_pane()
        await steps.proj_info_popup.ui_click_people_btn()
        await steps.proj_people_page.verify_ui_page_displayed()

        await steps.proj_people_page.ui_click_invite_people_proj_people_btn()
        await steps.invite_proj_member_popup.verify_ui_popup_displayed(
            org_name=org.org_name, proj_name=proj1.project_name
        )

        add_user = self._users_manager.generate_user()

        await steps.invite_proj_member_popup.ui_enter_user_data(email=add_user.email)
        await steps.invite_proj_member_popup.ui_select_user_role(role="Reader")
        await steps.invite_proj_member_popup.verify_ui_invite_user_btn_not_displayed(
            email=add_user.email
        )
