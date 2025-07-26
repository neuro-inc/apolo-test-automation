from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class PaymentPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        email = kwargs.get("email")
        if not isinstance(email, str):
            raise ValueError("Expected 'email' to be a non-empty string in kwargs")

        try:
            return (
                await self._get_email_field(email).is_visible()
                and await self._get_card_number_input().is_visible()
                and await self._get_card_expiry_input().is_visible()
                and await self._get_card_cvv_input().is_visible()
                and await self._get_card_name_input().is_visible()
                and await self._get_pay_btn().is_visible()
            )
        except Exception:
            html = await self.page.content()
            self.log(f"[PAYMENT page HTML]\n{html}")
            return False

    def _get_email_field(self, email: str) -> BaseElement:
        return BaseElement(self.page, "div.ReadOnlyFormField-title", has_text=email)

    def _get_card_number_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="cardNumber"]')

    def _get_card_expiry_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="cardExpiry"]')

    def _get_card_cvv_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="cardCvc"]')

    def _get_card_name_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="billingName"]')

    def _get_pay_btn(self) -> BaseElement:
        return BaseElement(self.page, '[data-testid="hosted-payment-submit-button"]')

    async def enter_card_number(self) -> None:
        await self._get_card_number_input().fill("4242424242424242")

    async def enter_card_expiry(self) -> None:
        await self._get_card_expiry_input().fill("0930")

    async def enter_card_cvv(self) -> None:
        await self._get_card_cvv_input().fill("098")

    async def enter_card_name(self) -> None:
        await self._get_card_name_input().fill("AQA Team")

    async def click_pay_btn(self) -> None:
        await self._get_pay_btn().click()

    async def wait_to_disappear(self) -> None:
        """
        Waits until key elements of the page disappear (popup is closed).
        """
        self.log("Wait for Payment page to process payment")

        await self._get_card_number_input().locator.wait_for(state="detached")
        await self._get_card_expiry_input().locator.wait_for(state="detached")
        await self._get_card_cvv_input().locator.wait_for(state="detached")
        await self._get_card_name_input().locator.wait_for(state="detached")
