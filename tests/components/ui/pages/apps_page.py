from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class AppsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._log_in_button = BaseElement(self.page, "button:text('Log in')")
        self._sign_up_button = BaseElement(self.page, "button:text('Sign up')")

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return await self._get_all_apps_btn().is_visible()

    def _get_all_apps_btn(self) -> BaseElement:
        return BaseElement(self.page, "a", has_text="All apps")

    async def click_all_apps_btn(self) -> None:
        self.log("Click All Apps button")
        await self._get_all_apps_btn().click()
