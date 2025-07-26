import re
from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class BuyCreditsPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_buy_credits_title().is_visible()
            and await self._get_credits_amount_input().is_visible()
            and await self._get_10_credits_btn().is_visible()
            and await self._get_100_credits_btn().is_visible()
            and await self._get_1000_credits_btn().is_visible()
            and await self._get_buy_credits_btn().is_visible()
        )

    def _get_buy_credits_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Buy Credits")

    def _get_credits_amount_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="credits"]')

    def _get_10_credits_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text=re.compile(r"^10$"))

    def _get_100_credits_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text=re.compile(r"^100$"))

    def _get_1000_credits_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text=re.compile(r"^1000$"))

    def _get_buy_credits_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Buy credits")

    async def enter_credits_amount(self, amount: int) -> None:
        self.log(f"Enter {amount} credits amount")
        await self._get_credits_amount_input().fill(str(amount))

    async def click_10_credits_btn(self) -> None:
        self.log("Click 10 credits btn")
        await self._get_10_credits_btn().click()

    async def click_100_credits_btn(self) -> None:
        self.log("Click 100 credits btn")
        await self._get_100_credits_btn().click()

    async def click_1000_credits_btn(self) -> None:
        self.log("Click 1000 credits btn")
        await self._get_1000_credits_btn().click()

    async def click_buy_credits_btn(self) -> None:
        self.log("Click Buy credits btn")
        await self._get_buy_credits_btn().click()

    async def wait_to_disappear(self) -> None:
        """
        Waits until key elements of the page disappear (popup is closed).
        """
        self.log("Wait for Buy credits popup to disappear")

        await self._get_buy_credits_title().locator.wait_for(state="detached")
        await self._get_credits_amount_input().locator.wait_for(state="detached")
        await self._get_10_credits_btn().locator.wait_for(state="detached")
        await self._get_100_credits_btn().locator.wait_for(state="detached")
        await self._get_1000_credits_btn().locator.wait_for(state="detached")
        await self._get_buy_credits_btn().locator.wait_for(state="detached")
