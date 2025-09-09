from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class PaymentPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Payment page displayed")
    async def verify_ui_page_displayed(self, email: str) -> None:
        assert await self._pm.payment_page.is_loaded(email=email), (
            "Payment page should be displayed!"
        )

    @async_step("Fill test payment data")
    async def ui_enter_test_payment_data(self) -> None:
        await self._pm.payment_page.enter_card_number()
        await self._pm.payment_page.enter_card_expiry()
        await self._pm.payment_page.enter_card_cvv()
        await self._pm.payment_page.enter_card_name()

    @async_step("Click Pay button")
    async def ui_click_pay_button(self) -> None:
        await self._pm.payment_page.click_pay_btn()

    @async_step("Wait for Payment page disappear")
    async def ui_wait_to_disappear(self) -> None:
        await self._pm.payment_page.wait_to_disappear()
