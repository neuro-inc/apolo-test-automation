import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.base_test_class import BaseTestClass


@async_suite("UI Organization Roles Access", parent="UI Tests")
class TestUIOrganizationRolesAccess(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_ui_test_steps()
        self._steps: UISteps = steps

    @async_title("Verify invited User access")
    async def test_invited_user_access(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with User role via API.
        Verify that User:
            - Cannot access organization Settings
            - Cannot access organization Billing
            - Cannot invite member to organization
            - Cannot edit organization members
            - Cannot delete members from organization
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
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.verify_ui_settings_btn_not_displayed()
        await u2_steps.org_settings_popup.verify_ui_billing_btn_not_displayed()

        await u2_steps.org_settings_popup.ui_click_people_button()
        await u2_steps.org_people_page.verify_ui_page_displayed()
        await u2_steps.org_people_page.verify_ui_invite_ppl_btn_disabled()

        await u2_steps.org_people_page.ui_click_three_dots_btn(email=user.email)
        await u2_steps.org_people_page.verify_ui_edit_user_btn_disabled()
        await u2_steps.org_people_page.verify_ui_remove_user_btn_disabled()

    @async_title("Verify invited Manager can access organization settings")
    async def test_invited_manager_org_settings(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Manager role via API.
        Verify that Manager:
            - Can access organization Settings.
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

        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.verify_ui_settings_btn_displayed()

        await u2_steps.org_settings_popup.ui_click_settings_btn()
        await u2_steps.org_settings_page.verify_ui_page_displayed()

    @async_title("Verify invited Manager can access organization billing")
    async def test_invited_manager_org_billing(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Manager role via API.
        Verify that Manager:
            - Can access organization Billing.
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

        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.verify_ui_billing_btn_displayed()

        await u2_steps.org_settings_popup.ui_click_billing_btn()
        await u2_steps.org_billing_page.verify_ui_page_displayed()

    @async_title("Verify invited Admin can access organization settings")
    async def test_invited_admin_org_settings(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Admin role via API.
        Verify that Admin:
            - Can access organization Settings.
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

        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.verify_ui_settings_btn_displayed()

        await u2_steps.org_settings_popup.ui_click_settings_btn()
        await u2_steps.org_settings_page.verify_ui_page_displayed()

    @async_title("Verify invited Admin can access organization billing")
    async def test_invited_admin_org_billing(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Signup second user.
        -Invite second user to organization with Admin role via API.
        Verify that Admin:
            - Can access organization Billing.
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

        await u2_steps.main_page.ui_click_organization_settings_button(
            email=second_user.email
        )
        await u2_steps.org_settings_popup.verify_ui_billing_btn_displayed()

        await u2_steps.org_settings_popup.ui_click_billing_btn()
        await u2_steps.org_billing_page.verify_ui_page_displayed()
