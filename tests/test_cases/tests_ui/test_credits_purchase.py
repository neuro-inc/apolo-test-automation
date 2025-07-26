import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Credits Purchase", parent="UI Tests")
class TestUICreditsPurchase(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps

    @async_title("Verify User cannot purchase credits via top pane")
    async def test_user_purchase_credits(self) -> None:
        """
        Invite member with User role.
        Verify that:
            - User cannot purchase credits via top pane.
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        add_steps = await self.init_test_steps()
        add_user = await add_steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        await add_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=add_user.email,
            role="User",
        )

        await add_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await add_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "User"
        )
        await add_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await add_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await add_steps.main_page.verify_ui_credits_button_disabled()

    @async_title(
        "Verify Manager can purchase organization credits with predefined value"
    )
    async def test_manager_purchase_credits(self) -> None:
        """
        Invite member with Manager role.
        Verify that:
            - Manager can purchase credits using predefined value(10, 100, 1000).
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()
        add_steps = await self.init_test_steps()
        add_user = await add_steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )
        await add_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        await steps.ui_invite_user_to_org(
            email=user.email,
            username=user.username,
            add_user_email=add_user.email,
            role="Manager",
        )

        await add_steps.ui_reload_page()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await add_steps.invited_to_org_page.verify_ui_page_displayed(
            org.org_name, "Manager"
        )
        await add_steps.invited_to_org_page.ui_click_accept_and_go_button()
        await add_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        await add_steps.main_page.verify_ui_credits_button_enabled()
        current_amount = await add_steps.main_page.ui_get_current_credits_amount()

        await add_steps.main_page.ui_click_credits_btn()
        await add_steps.buy_credits_popup.verify_ui_popup_displayed()

        await add_steps.buy_credits_popup.ui_click_10_credits_button()
        await add_steps.buy_credits_popup.ui_click_buy_credits_button()
        await add_steps.payment_page.verify_ui_page_displayed(email=add_user.email)

        await add_steps.payment_page.ui_enter_test_payment_data()
        await add_steps.payment_page.ui_click_pay_button()
        await add_steps.payment_page.ui_wait_to_disappear()
        await add_steps.main_page.verify_ui_page_displayed()

        expected_amount = current_amount + 10
        await add_steps.main_page.verify_ui_current_credits_amount_is_valid(
            expected_amount
        )

    @async_title("Verify Admin can purchase organization credits with custom amount")
    async def test_admin_purchase_credits(self) -> None:
        """
        Verify that:
            - Admin can purchase credits by input custom amount.
        """

        steps = self._steps
        user = await steps.ui_signup_new_user_ver_link()

        await steps.ui_pass_new_user_onboarding(
            email=user.email,
            username=user.username,
            gherkin_name="Default-organization",
        )

        await steps.main_page.verify_ui_credits_button_enabled()
        current_amount = await steps.main_page.ui_get_current_credits_amount()

        await steps.main_page.ui_click_credits_btn()
        await steps.buy_credits_popup.verify_ui_popup_displayed()

        await steps.buy_credits_popup.ui_enter_credits_amount(250)
        await steps.buy_credits_popup.ui_click_buy_credits_button()
        await steps.payment_page.verify_ui_page_displayed(email=user.email)

        await steps.payment_page.ui_enter_test_payment_data()
        await steps.payment_page.ui_click_pay_button()
        await steps.payment_page.ui_wait_to_disappear()
        await steps.main_page.verify_ui_page_displayed()

        expected_amount = current_amount + 250
        await steps.main_page.verify_ui_current_credits_amount_is_valid(expected_amount)
