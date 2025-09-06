from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class DeleteFilePopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        name = kwargs.get("name")
        if not isinstance(name, str):
            raise ValueError("Expected 'name' to be a non-empty string in kwargs")
        return (
            await self._get_delete_file_title().is_visible()
            and await self._get_delete_file_message(name).is_visible()
            and await self._get_delete_btn().is_visible()
        )

    def _get_delete_file_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Delete Storage Object")

    def _get_delete_file_message(self, name: str) -> BaseElement:
        selector = (
            f"p:has-text('Are you sure you want to delete'):has(span:text('{name}'))"
        )
        return BaseElement(self.page, selector)

    def _get_delete_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Delete")

    async def click_delete_btn(self) -> None:
        self.log("Click Delete button")
        await self._get_delete_btn().click()

    async def wait_to_disappear(self, name: str) -> None:
        """
        Waits until key elements of the page disappear (popup is closed).
        """
        self.log("Wait for Delete File popup to disappear")

        await self._get_delete_file_title().locator.wait_for(state="detached")
        await self._get_delete_file_message(name).locator.wait_for(state="detached")
        await self._get_delete_btn().locator.wait_for(state="detached")
