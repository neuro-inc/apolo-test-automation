from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class FilesPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_files_title().is_visible()
            and await self._get_add_folder_btn().is_visible()
            and await self._get_upload_btn().is_visible()
            and await self._get_folder_up_btn().is_visible()
        )

    def _get_files_title(self) -> BaseElement:
        return BaseElement(self.page, "h4.text-h4", has_text="Files")

    def _get_add_folder_btn(self) -> BaseElement:
        return BaseElement(self.page, "button.bg-rebecca", has_text="Add folder")

    def _get_upload_btn(self) -> BaseElement:
        return BaseElement(self.page, "button.bg-rebecca", has_text="Upload")

    def _get_folder_up_btn(self) -> BaseElement:
        return BaseElement(
            self.page,
            'button:has(svg[data-icon="arrow-turn-left"])',
            has_text="Folder up",
        )

    def _get_folder_btn(self, name: str) -> BaseElement:
        return BaseElement(self.page, f'button:has(p[title="{name}"]:text("{name}"))')

    async def is_add_folder_btn_enabled(self) -> bool:
        self.log("Check if Add folder button is enabled")
        return await self._get_add_folder_btn().is_enabled()

    async def click_add_folder_btn(self) -> None:
        self.log("Click Add Folder button")
        await self._get_add_folder_btn().click()

    async def is_upload_btn_enabled(self) -> bool:
        self.log("Check if Upload button is enabled")
        return await self._get_upload_btn().is_enabled()

    async def click_upload_btn(self) -> None:
        self.log("Click Upload button")
        await self._get_upload_btn().click()

    async def is_folder_btn_displayed(self, name: str) -> bool:
        self.log(f"Check if Folder {name} button is displayed")
        return await self._get_folder_btn(name).is_visible()
