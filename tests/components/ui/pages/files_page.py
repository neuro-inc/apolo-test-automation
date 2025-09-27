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

    def _get_file_btn(self, name: str) -> BaseElement:
        return BaseElement(self.page, f'button:has(p[title="{name}"]:text("{name}"))')

    async def is_folder_up_btn_displayed(self) -> bool:
        self.log("Check if folder up button displayed")
        return await self._get_folder_up_btn().is_visible()

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
        await self.page.wait_for_timeout(1000)

    async def is_file_btn_displayed(self, name: str) -> bool:
        self.log(f"Check if File {name} button is displayed")
        return await self._get_file_btn(name).is_visible()

    async def click_file_btn(self, name: str) -> None:
        self.log(f"Click File {name} button")
        await self._get_file_btn(name).click()

    async def double_click_file_btn(self, name: str) -> None:
        self.log(f"Double click File {name} button")
        await self._get_file_btn(name).double_click()
        await self.page.wait_for_timeout(500)

    def _get_file_info_section_title(self, name: str) -> BaseElement:
        return BaseElement(self.page, "p.truncate.text-h5", has_text=name)

    def _get_file_info_section_properties_title(self) -> BaseElement:
        return BaseElement(self.page, "p.text-h6", has_text="Properties")

    def _get_file_info_section_path(self, path: str) -> BaseElement:
        return BaseElement(self.page, "span.truncate", has_text=path)

    async def is_file_info_section_displayed(self, name: str, path: str) -> bool:
        self.log(f"Check if File {name} info section is displayed")
        return (
            await self._get_file_info_section_title(name=name).is_visible()
            and await self._get_file_info_section_properties_title().is_visible()
            and await self._get_file_info_section_path(path=path).is_visible()
        )

    def _get_file_action_bar_share_btn(self) -> BaseElement:
        return BaseElement(self.page, "svg[data-icon='user-plus']")

    async def is_file_action_bar_share_btn_enabled(self) -> bool:
        self.log("Check if Share button in File action bar is enabled")
        return (
            await self._get_file_action_bar_share_btn()
            .locator.locator("xpath=ancestor::button")
            .is_enabled()
        )

    def _get_file_action_bar_download_btn(self) -> BaseElement:
        return BaseElement(self.page, "svg[data-icon='file-arrow-down']")

    async def is_file_action_bar_download_btn_enabled(self) -> bool:
        self.log("Check if Download button in File action bar is enabled")
        return (
            await self._get_file_action_bar_download_btn()
            .locator.locator("xpath=ancestor::button")
            .is_enabled()
        )

    async def click_file_action_bar_download_btn(self) -> None:
        self.log("Click Download button on File action bar")
        await (
            self._get_file_action_bar_download_btn()
            .locator.locator("xpath=ancestor::button")
            .click()
        )

    def _get_file_action_bar_rename_btn(self) -> BaseElement:
        return BaseElement(self.page, "svg[data-icon='file-pen']")

    async def is_file_action_bar_rename_btn_enabled(self) -> bool:
        self.log("Check if Rename button in File action bar is enabled")
        return (
            await self._get_file_action_bar_rename_btn()
            .locator.locator("xpath=ancestor::button")
            .is_enabled()
        )

    async def click_file_action_bar_rename_btn(self) -> None:
        self.log("Click Rename button in File action bar")
        await (
            self._get_file_action_bar_rename_btn()
            .locator.locator("xpath=ancestor::button")
            .click()
        )

    def _get_file_action_bar_delete_btn(self) -> BaseElement:
        return BaseElement(self.page, "svg[data-icon='trash-can']")

    async def is_file_action_bar_delete_btn_enabled(self) -> bool:
        self.log("Check if Delete button in File action bar is enabled")
        return (
            await self._get_file_action_bar_delete_btn()
            .locator.locator("xpath=ancestor::button")
            .is_enabled()
        )

    async def click_file_action_bar_delete_btn(self) -> None:
        self.log("Click Delete button in File action bar")
        await (
            self._get_file_action_bar_delete_btn()
            .locator.locator("xpath=ancestor::button")
            .click()
        )

    async def is_file_action_bar_displayed(self) -> bool:
        self.log("Check if File action bar is displayed")
        return (
            await self._get_file_action_bar_share_btn().is_visible()
            and await self._get_file_action_bar_download_btn().is_visible()
            and await self._get_file_action_bar_rename_btn().is_visible()
            and await self._get_file_action_bar_delete_btn().is_visible()
        )
