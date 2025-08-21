from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class NewFolderPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")

        return (
            await self._get_new_folder_title().expect_to_be_loaded()
            and await self._get_folder_name_input().expect_to_be_loaded()
            and await self._get_create_btn().expect_to_be_loaded()
        )

    def _get_new_folder_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="New folder")

    def _get_folder_name_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="folderName"]')

    async def enter_folder_name(self, name: str) -> None:
        self.log(f"Enter {name} folder name")
        await self._get_folder_name_input().fill(name)

    def _get_create_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Create")

    async def click_create_btn(self) -> None:
        self.log("Click Create button")
        await self._get_create_btn().click()

    async def wait_to_disappear(self) -> None:
        """
        Waits until key elements of the page disappear (popup is closed).
        """
        self.log("Wait for New Folder popup to disappear")

        await self._get_new_folder_title().locator.wait_for(state="detached")
        await self._get_folder_name_input().locator.wait_for(state="detached")
        await self._get_create_btn().locator.wait_for(state="detached")
