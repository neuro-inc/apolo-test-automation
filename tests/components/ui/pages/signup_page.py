from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class SignupPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._signup_message = BaseElement(
            self.page, "p", has_text="Sign Up to Apolo to continue to Console."
        )
        self._email_input = BaseElement(self.page, "#email")
        self._password_input = BaseElement(self.page, "#password")
        self._continue_button = BaseElement(
            self.page, "button[type='submit'][name='action'][value='default']"
        )

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page is loaded")
        return (
            await self._signup_message.expect_to_be_loaded()
            and await self._email_input.expect_to_be_loaded()
            and await self._password_input.expect_to_be_loaded()
            and await self._continue_button.expect_to_be_loaded()
        )

    async def enter_email(self, text: str) -> None:
        self.log(f"Enter {text} email")
        await self._email_input.fill(text)

    async def enter_password(self, text: str) -> None:
        self.log("Enter ********* password")
        await self._password_input.fill(text)

    async def click_continue_button(self) -> None:
        self.log("Click continue button")
        await self._continue_button.click()
