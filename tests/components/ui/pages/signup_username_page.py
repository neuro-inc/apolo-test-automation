from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class SignupUsernamePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._username_input = BaseElement(self.page, "#input")
        self._signup_button = BaseElement(self.page, "button", has_text="Sign up")

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page is loaded")
        await self.page.wait_for_timeout(1000)
        return (
            await self._username_input.expect_to_be_loaded()
            and await self._signup_button.expect_to_be_loaded()
        )

    async def enter_username(self, text: str) -> None:
        self.log(f"Enter {text} username")
        await self._username_input.fill(text)
        await self.page.wait_for_timeout(500)
        self.log("Wait for network idle")
        await self.page.wait_for_load_state("networkidle", timeout=10000)
        self.log("Network idle done")

    async def click_signup_button(self) -> None:
        self.log("Click signup button")
        await self._signup_button.click()
        await self.page.wait_for_timeout(1000)
        await self.page.reload()
        await self.page.wait_for_timeout(500)
