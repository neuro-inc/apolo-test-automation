import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.base_test_class import BaseTestClass


@async_suite("UI Credits Purchase", parent="UI Tests")
class TestUICreditsPurchase(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_ui_test_steps()
        self._steps: UISteps = steps

    @async_title("Verify User cannot purchase credits via top pane")
    async def test_user_purchase_credits(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Signup `second user`.
        - Invite `second user` to organization with `User` role.

        ### Verify that:

        - `User` **cannot** purchase credits via top pane.
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

        await u2_steps.main_page.verify_ui_credits_button_disabled()

    @async_title(
        "Verify Manager can purchase organization credits with predefined value"
    )
    async def test_manager_purchase_credits(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.
        - Signup `second user`.
        - Invite `second user` to organization with `Manager` role.

        ### Verify that:

        - `Manager` can purchase credits using predefined value(10, 100, 1000).
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

        await u2_steps.main_page.verify_ui_credits_button_enabled()
        current_amount = await u2_steps.main_page.ui_get_current_credits_amount()

        await u2_steps.main_page.ui_click_credits_btn()
        await u2_steps.buy_credits_popup.verify_ui_popup_displayed()

        await u2_steps.buy_credits_popup.ui_click_10_credits_button()
        await u2_steps.buy_credits_popup.ui_click_buy_credits_button()
        await u2_steps.payment_page.verify_ui_page_displayed(email=second_user.email)

        await u2_steps.payment_page.ui_enter_test_payment_data()
        await u2_steps.payment_page.ui_click_pay_button()
        await u2_steps.payment_page.ui_wait_to_disappear()
        await u2_steps.main_page.verify_ui_page_displayed()

        expected_amount = current_amount + 10
        await u2_steps.main_page.verify_ui_current_credits_amount_is_valid(
            expected_amount
        )

    @async_title("Verify Admin can purchase organization credits with custom amount")
    async def test_admin_purchase_credits(self) -> None:
        """
        - Login with valid credentials.
        - Create new organization via **API**.

        ### Verify that:

        - Admin can purchase credits by input custom amount.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
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
