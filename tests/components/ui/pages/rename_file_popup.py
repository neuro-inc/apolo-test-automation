from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class RenameFilePopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_enter_new_name_title().is_visible()
            and await self._get_new_name_input().is_visible()
            and await self._get_rename_btn().is_visible()
        )

    def _get_enter_new_name_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Enter new name")

    def _get_new_name_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="newName"]')

    async def enter_new_name(self, name: str) -> None:
        self.log(f"Enter new name: {name}")
        await self._get_new_name_input().fill(name)

    def _get_rename_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Rename")

    async def click_rename_btn(self) -> None:
        self.log("Click Rename button")
        await self._get_rename_btn().click()

    async def wait_to_disappear(self) -> None:
        """
        Waits until key elements of the page disappear (popup is closed).
        """
        self.log("Wait for Rename File popup to disappear")

        await self._get_enter_new_name_title().locator.wait_for(state="detached")
        await self._get_new_name_input().locator.wait_for(state="detached")
        await self._get_rename_btn().locator.wait_for(state="detached")
