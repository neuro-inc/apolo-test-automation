import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.base_test_class import BaseTestClass


@async_suite("UI Organization Change Member Roles", parent="UI Tests")
class TestUIOrganizationChangeMemberRoles(BaseTestClass):
    """
    This class tests the UI Organization Change Member Roles via UI.
    """

    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_ui_test_steps()
        self._steps: UISteps = steps

    @async_title("Verify Admin can change User role to Manager")
    async def test_admin_change_user_to_manager(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with User role via API.
        Verify that:
            - Admin can change user role from User to Manager
            - User after changing role from User to Manager:
                - Can access organization Settings
                - Can access organization Billing
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="User",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_reload_page()
        await steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await steps.org_people_page.ui_click_edit_user_btn()
        await steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_org_user_popup.ui_select_new_user_role(role="Manager")
        await steps.edit_org_user_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=second_user.email, role="Manager"
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.verify_ui_settings_btn_displayed()
        await u2_steps.org_settings_popup.verify_ui_billing_btn_displayed()

    @async_title("Verify Admin can change User role to Admin")
    async def test_admin_change_user_to_admin(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with User role via API.
        Verify that:
            - Admin can change user role from User to Admin
            - User after changing role from User to Admin:
                - Can access organization Settings
                - Can access organization Billing
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="User",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_reload_page()
        await steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await steps.org_people_page.ui_click_edit_user_btn()
        await steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_org_user_popup.ui_select_new_user_role(role="Admin")
        await steps.edit_org_user_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=second_user.email, role="Admin"
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.verify_ui_settings_btn_displayed()
        await u2_steps.org_settings_popup.verify_ui_billing_btn_displayed()

    @async_title("Verify Admin can change Manager role to User")
    async def test_admin_change_manager_to_user(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Manager role via API.
        Verify that:
            - Admin can change user role from Manager to User
            - User after changing role from Manager to User:
                - Cannot access organization Settings
                - Cannot access organization Billing
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_reload_page()
        await steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await steps.org_people_page.ui_click_edit_user_btn()
        await steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_org_user_popup.ui_select_new_user_role(role="User")
        await steps.edit_org_user_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=second_user.email, role="User"
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.verify_ui_settings_btn_not_displayed()
        await u2_steps.org_settings_popup.verify_ui_billing_btn_not_displayed()

    @async_title("Verify Admin can change Manager role to Admin")
    async def test_admin_change_manager_to_admin(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Manager role via API.
        Verify that:
            - Admin can change user role from Manager to Admin
            - User after changing role from Manager to Admin:
                - Can access organization Settings
                - Can access organization Billing
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_reload_page()
        await steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await steps.org_people_page.ui_click_edit_user_btn()
        await steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_org_user_popup.ui_select_new_user_role(role="Admin")
        await steps.edit_org_user_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=second_user.email, role="Admin"
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )

        await u2_steps.org_settings_popup.verify_ui_settings_btn_displayed()
        await u2_steps.org_settings_popup.verify_ui_billing_btn_displayed()

    @async_title("Verify Admin can change Admin role to User")
    async def test_admin_change_admin_to_user(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Admin role via API.
        Verify that:
            - Admin can change user role from Admin to User
            - User after changing role from Admin to User:
                - Cannot access organization Settings
                - Cannot access organization Billing
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Admin",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_reload_page()
        await steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await steps.org_people_page.ui_click_edit_user_btn()
        await steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_org_user_popup.ui_select_new_user_role(role="User")
        await steps.edit_org_user_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=second_user.email, role="User"
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )

        await u2_steps.org_settings_popup.verify_ui_settings_btn_not_displayed()
        await u2_steps.org_settings_popup.verify_ui_billing_btn_not_displayed()

    @async_title("Verify Admin can change Admin role to Manager")
    async def test_admin_change_admin_to_manager(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Admin role via API.
        Verify that:
            - Admin can change user role from Admin to Manager
            - User after changing role from Admin to Manager:
                - Can access organization Settings
                - Can access organization Billing
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Admin",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await steps.ui_reload_page()
        await steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await steps.org_people_page.ui_click_edit_user_btn()
        await steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await steps.edit_org_user_popup.ui_select_new_user_role(role="Manager")
        await steps.edit_org_user_popup.ui_click_save_button()
        await steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=second_user.email, role="Manager"
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )

        await u2_steps.org_settings_popup.verify_ui_settings_btn_displayed()
        await u2_steps.org_settings_popup.verify_ui_billing_btn_displayed()

    @async_title("Verify Admin cannot demote himself to User")
    async def test_admin_demote_himself_to_user(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Admin role via API.
        Verify that:
            - Admin cannot demote himself to User
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Admin",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await u2_steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_edit_user_btn()
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await u2_steps.edit_org_user_popup.ui_select_new_user_role(role="User")
        await u2_steps.edit_org_user_popup.ui_click_save_button()
        await u2_steps.ui_wait_for_timeout(1000)
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )
        await u2_steps.ui_reload_page()
        await u2_steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=second_user.email, role="Admin"
        )

    @async_title("Verify Admin cannot demote himself to Manager")
    async def test_admin_demote_himself_to_manager(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Admin role via API.
        Verify that:
            - Admin cannot demote himself to Manager
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Admin",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await u2_steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_edit_user_btn()
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await u2_steps.edit_org_user_popup.ui_select_new_user_role(role="Manager")
        await u2_steps.edit_org_user_popup.ui_click_save_button()
        await u2_steps.ui_wait_for_timeout(1000)
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )
        await u2_steps.ui_reload_page()
        await u2_steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=second_user.email, role="Admin"
        )

    @async_title("Verify Manager can change User role to Manager")
    async def test_manager_change_user_to_manager(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Manager role via API.
        -Signup third user.
        -Invite third user to organization with User role via API.
        Verify that:
            - Manager can change user role from User to Manager
            - User after changing role from User to Manager:
                - Can access organization Settings
                - Can access organization Billing
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        u3_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        third_user = await u3_steps.ui_get_third_user()
        await u3_steps.ui_login(third_user)
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=third_user.username,
            role="User",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=third_user.email)
        await u2_steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_edit_user_btn()
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_org_user_popup.ui_select_new_user_role(role="Manager")
        await u2_steps.edit_org_user_popup.ui_click_save_button()
        await u2_steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await u2_steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=second_user.email, role="Manager"
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.ui_click_organization_settings_button(
            email=third_user.email
        )

        await u3_steps.org_settings_popup.verify_ui_settings_btn_displayed()
        await u3_steps.org_settings_popup.verify_ui_billing_btn_displayed()

    @async_title("Verify Manager cannot change User role to Admin")
    async def test_manager_change_user_to_admin(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Manager role via API.
        -Signup third user.
        -Invite third user to organization with User role via API.
        Verify that:
            - Manager cannot change user role from User to Admin.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        u3_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        third_user = await u3_steps.ui_get_third_user()
        await u3_steps.ui_login(third_user)
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=third_user.username,
            role="User",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=third_user.email)
        await u2_steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_edit_user_btn()
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_org_user_popup.ui_select_new_user_role(role="Admin")
        await u2_steps.edit_org_user_popup.ui_click_save_button()
        await u2_steps.ui_wait_for_timeout(1000)
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )
        await u2_steps.ui_reload_page()
        await u2_steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=third_user.email, role="User"
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.ui_click_organization_settings_button(
            email=third_user.email
        )

        await u3_steps.org_settings_popup.verify_ui_settings_btn_not_displayed()
        await u3_steps.org_settings_popup.verify_ui_billing_btn_not_displayed()

    @async_title("Verify Manager can change Manager role to User")
    async def test_manager_change_manager_to_user(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Manager role via API.
        -Signup third user.
        -Invite third user to organization with Manager role via API.
        Verify that:
            - Manager can change user role from Manager to User
            - User after changing role from Manager to User:
                - Cannot access organization Settings
                - Cannot access organization Billing
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        u3_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        third_user = await u3_steps.ui_get_third_user()
        await u3_steps.ui_login(third_user)
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=third_user.username,
            role="Manager",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=third_user.email)
        await u2_steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_edit_user_btn()
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_org_user_popup.ui_select_new_user_role(role="User")
        await u2_steps.edit_org_user_popup.ui_click_save_button()
        await u2_steps.edit_org_user_popup.ui_wait_to_disappear(
            username=second_user.username
        )
        await u2_steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=third_user.email, role="User"
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.ui_click_organization_settings_button(
            email=third_user.email
        )

        await u3_steps.org_settings_popup.verify_ui_settings_btn_not_displayed()
        await u3_steps.org_settings_popup.verify_ui_billing_btn_not_displayed()

    @async_title("Verify Manager cannot change Manager role to Admin")
    async def test_manager_change_manager_to_admin(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Manager role via API.
        -Signup third user.
        -Invite third user to organization with Manager role via API.
        Verify that:
            - Manager cannot change user role from Manager to Admin.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        u3_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        third_user = await u3_steps.ui_get_third_user()
        await u3_steps.ui_login(third_user)
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=third_user.username,
            role="Manager",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=third_user.email)
        await u2_steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_edit_user_btn()
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_org_user_popup.ui_select_new_user_role(role="Admin")
        await u2_steps.edit_org_user_popup.ui_click_save_button()
        await u2_steps.ui_wait_for_timeout(1000)
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )
        await u2_steps.ui_reload_page()
        await u2_steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=third_user.email, role="Manager"
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.ui_click_organization_settings_button(
            email=third_user.email
        )

        await u3_steps.org_settings_popup.verify_ui_settings_btn_displayed()
        await u3_steps.org_settings_popup.verify_ui_billing_btn_displayed()

    @async_title("Verify Manager cannot change Admin role to User")
    async def test_manager_change_admin_to_user(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Manager role via API.
        -Signup third user.
        -Invite third user to organization with Admin role via API.
        Verify that:
            - Manager cannot change user role from Admin to User
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        u3_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        third_user = await u3_steps.ui_get_third_user()
        await u3_steps.ui_login(third_user)
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=third_user.username,
            role="Admin",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=third_user.email)
        await u2_steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_edit_user_btn()
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_org_user_popup.ui_select_new_user_role(role="User")
        await u2_steps.edit_org_user_popup.ui_click_save_button()
        await u2_steps.ui_wait_for_timeout(1000)
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )
        await u2_steps.ui_reload_page()
        await u2_steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=third_user.email, role="Admin"
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.ui_click_organization_settings_button(
            email=third_user.email
        )

        await u3_steps.org_settings_popup.verify_ui_settings_btn_displayed()
        await u3_steps.org_settings_popup.verify_ui_billing_btn_displayed()

    @async_title("Verify Manager cannot change Admin role to Manager")
    async def test_manager_change_admin_to_manager(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Manager role via API.
        -Signup third user.
        -Invite third user to organization with Admin role via API.
        Verify that:
            - Manager cannot change user role from Admin to Manager
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        u3_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )
        third_user = await u3_steps.ui_get_third_user()
        await u3_steps.ui_login(third_user)
        await u3_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=third_user.username,
            role="Admin",
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=third_user.email)
        await u2_steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_edit_user_btn()
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )

        await u2_steps.edit_org_user_popup.ui_select_new_user_role(role="Manager")
        await u2_steps.edit_org_user_popup.ui_click_save_button()
        await u2_steps.ui_wait_for_timeout(1000)
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=third_user.username
        )
        await u2_steps.ui_reload_page()
        await u2_steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=third_user.email, role="Admin"
        )

        await u3_steps.ui_reload_page()
        await u3_steps.main_page.ui_click_organization_settings_button(
            email=third_user.email
        )

        await u3_steps.org_settings_popup.verify_ui_settings_btn_displayed()
        await u3_steps.org_settings_popup.verify_ui_billing_btn_displayed()

    @async_title("Verify Manager cannot demote himself to User")
    async def test_manager_demote_himself_to_user(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Manager role via API.
        Verify that:
            - Manager cannot demote himself to User.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.ui_click_organization_settings_button(
            second_user.email
        )
        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.ui_click_three_dots_btn(email=second_user.email)
        await u2_steps.org_people_page.verify_ui_edit_user_btn_enabled()

        await u2_steps.org_people_page.ui_click_edit_user_btn()
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )

        await u2_steps.edit_org_user_popup.ui_select_new_user_role(role="User")
        await u2_steps.edit_org_user_popup.ui_click_save_button()
        await u2_steps.ui_wait_for_timeout(1000)
        await u2_steps.edit_org_user_popup.verify_ui_popup_displayed(
            username=second_user.username
        )
        await u2_steps.ui_reload_page()
        await u2_steps.org_people_page.verify_ui_valid_user_role_displayed(
            email=second_user.email, role="Manager"
        )
