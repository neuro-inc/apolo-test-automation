from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class BuyCreditsPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify Buy credits popup displayed")
    async def verify_ui_popup_displayed(self) -> None:
        assert await self._pm.buy_credits_popup.is_loaded(), (
            "Buy credits popup should be displayed!"
        )

    @async_step("Enter credits amount")
    async def ui_enter_credits_amount(self, amount: int) -> None:
        await self._pm.buy_credits_popup.enter_credits_amount(amount=amount)

    @async_step("Click 10 credits button")
    async def ui_click_10_credits_button(self) -> None:
        await self._pm.buy_credits_popup.click_10_credits_btn()

    @async_step("Click 100 credits button")
    async def ui_click_100_credits_button(self) -> None:
        await self._pm.buy_credits_popup.click_100_credits_btn()

    @async_step("Click 1000 credits button")
    async def ui_click_1000_credits_button(self) -> None:
        await self._pm.buy_credits_popup.click_1000_credits_btn()

    @async_step("Click Buy credits button")
    async def ui_click_buy_credits_button(self) -> None:
        await self._pm.buy_credits_popup.click_buy_credits_btn()

    @async_step("Wait for Buy credits popup disappear")
    async def ui_wait_to_disappear(self) -> None:
        await self._pm.buy_credits_popup.wait_to_disappear()
