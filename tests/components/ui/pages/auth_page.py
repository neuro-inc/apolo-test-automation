from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class AuthPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._log_in_button = BaseElement(self.page, "button:text('Log in')")
        self._sign_up_button = BaseElement(self.page, "button:text('Sign up')")

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._log_in_button.expect_to_be_loaded()
            and await self._sign_up_button.expect_to_be_loaded()
        )

    async def click_log_in_button(self) -> None:
        self.log("Click log in button")
        await self._log_in_button.click()

    async def click_sign_up_button(self) -> None:
        self.log("Click sign up button")
        await self._sign_up_button.click()
