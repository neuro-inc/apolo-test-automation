import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Organization Remove Members", parent="UI Tests")
class TestUIOrganizationRemoveMembers(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps

    @async_title("Verify Admin can remove User from organization")
    async def test_admin_remove_user_from_org(self) -> None:
        """
        Invite member with User role.
        Verify that:
            - Admin can remove User from organization
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
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_reload_page()
        await steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await steps.org_people_page.verify_ui_remove_user_btn_enabled()

        await steps.org_people_page.ui_click_remove_user_btn()
        await steps.remove_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.remove_org_user_popup.ui_click_remove_button()
        await steps.remove_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.org_people_page.verify_ui_page_displayed()
        await steps.org_people_page.verify_ui_user_not_displayed_in_users_list(
            email=second_user.email
        )

        await u2_steps.ui_reload_page()
        await u2_steps.welcome_new_user_page.verify_ui_page_displayed(
            email=second_user.email
        )

    @async_title("Verify Admin can remove Manager from organization")
    async def test_admin_remove_manager_from_org(self) -> None:
        """
        Invite member with Manager role.
        Verify that:
            - Admin can remove Manager from organization
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
            role="Manager",
        )

        await u2_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "Manager"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_reload_page()
        await steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await steps.org_people_page.verify_ui_remove_user_btn_enabled()

        await steps.org_people_page.ui_click_remove_user_btn()
        await steps.remove_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.remove_org_user_popup.ui_click_remove_button()
        await steps.remove_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.org_people_page.verify_ui_page_displayed()
        await steps.org_people_page.verify_ui_user_not_displayed_in_users_list(
            email=second_user.email
        )

        await u2_steps.ui_reload_page()
        await u2_steps.welcome_new_user_page.verify_ui_page_displayed(
            email=second_user.email
        )

    @async_title("Verify Admin can remove another Admin from organization")
    async def test_admin_remove_admin_from_org(self) -> None:
        """
        Invite member with Admin role.
        Verify that:
            - Admin can remove Admin from organization
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
            role="Admin",
        )

        await u2_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "Admin"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_reload_page()
        await steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await steps.org_people_page.verify_ui_remove_user_btn_enabled()

        await steps.org_people_page.ui_click_remove_user_btn()
        await steps.remove_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.remove_org_user_popup.ui_click_remove_button()
        await steps.remove_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.org_people_page.verify_ui_page_displayed()
        await steps.org_people_page.verify_ui_user_not_displayed_in_users_list(
            email=second_user.email
        )

        await u2_steps.ui_reload_page()
        await u2_steps.welcome_new_user_page.verify_ui_page_displayed(
            email=second_user.email
        )

    @async_title("Verify Admin cannot remove himself from organization")
    async def test_admin_remove_himself_from_org(self) -> None:
        """
        Invite member with Admin role.
        Verify that:
            - Admin cannot remove himself from organization
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
            role="Admin",
        )

        await u2_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "Admin"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await u2_steps.org_people_page.verify_ui_remove_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_remove_user_btn()
        await u2_steps.remove_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await u2_steps.remove_org_user_popup.ui_click_remove_button()
        await u2_steps._pm.page.wait_for_timeout(1000)
        await u2_steps.remove_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )
        await u2_steps.ui_reload_page()
        await steps.org_people_page.verify_ui_user_displayed_in_users_list(
            email=second_user.email
        )

    @async_title("Verify Manager can remove User from organization")
    async def test_manager_remove_user_from_org(self) -> None:
        """
        Invite member1 with Manager role. Invite member2 with User role.
        Verify that:
            - Manager can remove User from organization
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
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
            role="Manager",
        )

        await u2_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "Manager"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        third_user = await u3_steps.ui_signup_new_user_ver_link()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=third_user.email,
            role="User",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u3_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await u3_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=third_user.email)
        await u2_steps.org_people_page.verify_ui_remove_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_remove_user_btn()
        await u2_steps.remove_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.remove_org_user_popup.ui_click_remove_button()
        await u2_steps.remove_org_user_popup.ui_wait_to_disappear(
            username=third_user.username
        )
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.verify_ui_user_not_displayed_in_users_list(
            email=third_user.email
        )

        await u3_steps.ui_reload_page()
        await u3_steps.welcome_new_user_page.verify_ui_page_displayed(
            email=third_user.email
        )

    @async_title("Verify Manager can remove another Manager from organization")
    async def test_manager_remove_manager_from_org(self) -> None:
        """
        Invite member1 with Manager role. Invite member2 with Manager role.
        Verify that:
            - Manager can remove another Manager from organization
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
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
            role="Manager",
        )

        await u2_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "Manager"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        third_user = await u3_steps.ui_signup_new_user_ver_link()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=third_user.email,
            role="Manager",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u3_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "Manager"
        )
        await u3_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=third_user.email)
        await u2_steps.org_people_page.verify_ui_remove_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_remove_user_btn()
        await u2_steps.remove_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.remove_org_user_popup.ui_click_remove_button()
        await u2_steps.remove_org_user_popup.ui_wait_to_disappear(
            username=third_user.username
        )
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.verify_ui_user_not_displayed_in_users_list(
            email=third_user.email
        )

        await u3_steps.ui_reload_page()
        await u3_steps.welcome_new_user_page.verify_ui_page_displayed(
            email=third_user.email
        )

    @async_title("Verify Manager cannot remove Admin from organization")
    async def test_manager_remove_admin_from_org(self) -> None:
        """
        Invite member1 with Manager role. Invite member2 with Admin role.
        Verify that:
            - Manager cannot remove another Admin from organization
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        u2_steps = await self.init_test_steps()
        u3_steps = await self.init_test_steps()
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
            role="Manager",
        )

        await u2_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "Manager"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        third_user = await u3_steps.ui_signup_new_user_ver_link()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=third_user.email,
            role="Manager",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()
        await u3_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "Manager"
        )
        await u3_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=third_user.email)
        await u2_steps.org_people_page.verify_ui_remove_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_remove_user_btn()
        await u2_steps.remove_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.remove_org_user_popup.ui_click_remove_button()
        await u2_steps.remove_org_user_popup.ui_wait_to_disappear(
            username=third_user.username
        )
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.verify_ui_user_not_displayed_in_users_list(
            email=third_user.email
        )

        await u3_steps.ui_reload_page()
        await u3_steps.welcome_new_user_page.verify_ui_page_displayed(
            email=third_user.email
        )

    @async_title("Verify Manager cannot remove himself from organization")
    async def test_manager_remove_himself_from_org(self) -> None:
        """
        Invite member with Manager role.
        Verify that:
            - Manager cannot remove himself from organization
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
            role="Manager",
        )

        await u2_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await u2_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "Manager"
        )
        await u2_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await u2_steps.org_people_page.verify_ui_remove_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_remove_user_btn()
        await u2_steps.remove_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await u2_steps.remove_org_user_popup.ui_click_remove_button()
        await u2_steps._pm.page.wait_for_timeout(1000)
        await u2_steps.remove_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )
        await u2_steps.ui_reload_page()
        await steps.org_people_page.verify_ui_user_displayed_in_users_list(
            email=second_user.email
        )
