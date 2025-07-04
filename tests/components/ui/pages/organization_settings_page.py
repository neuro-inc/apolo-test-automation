from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class OrganizationSettingsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_general_title().is_visible()
            and await self._get_credits_input().is_visible()
            and await self._get_save_button().is_visible()
        )

    def _get_general_title(self) -> BaseElement:
        return BaseElement(self.page, "h6.text-h6", has_text="General")

    def _get_credits_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="credits"]')

    def _get_save_button(self) -> BaseElement:
        return BaseElement(self.page, by_role="button", name="Save")
