from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class DisksPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_disks_title().is_visible()
            and await self._get_create_new_disk_btn().is_visible()
        )

    def _get_disks_title(self) -> BaseElement:
        return BaseElement(self.page, "h4.text-h4", has_text="Disks")

    def _get_create_new_disk_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Create new disk")

    def _get_search_disk_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[placeholder=" "]')

    def _get_no_disks_message(self) -> BaseElement:
        return BaseElement(self.page, "p", has_text="No disks found")

    def _get_disk_btn(self, disk_name: str) -> BaseElement:
        return BaseElement(self.page, "button", has_text=disk_name)

    def _get_disk_info_view_title(self, disk_name: str) -> BaseElement:
        return BaseElement(self.page, "p.truncate.text-h5", has_text=disk_name)

    def _get_disk_info_owner_label(self) -> BaseElement:
        return BaseElement(self.page, "p.text-h6", has_text="Owner")

    def _get_disk_info_owner_value(self, owner: str) -> BaseElement:
        return BaseElement(self.page, "p.text-neural-04", has_text=owner)

    def _get_disk_info_storage_label(self) -> BaseElement:
        return BaseElement(self.page, "p.text-h6", has_text="Storage")

    def _get_disk_info_storage_value(self, storage_value: str) -> BaseElement:
        return BaseElement(self.page, "p.text-neural-04", has_text=storage_value)

    def _get_disk_info_lifespan_label(self) -> BaseElement:
        return BaseElement(self.page, "p.text-h6", has_text="Lifespan")

    def _get_disk_info_lifespan_value(self, lifespan_value: str) -> BaseElement:
        return BaseElement(self.page, "p.text-neural-04", has_text=lifespan_value)

    def _get_disk_info_delete_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Delete disk")

    async def is_no_disks_message_displayed(self) -> bool:
        self.log("Check if No disks message displayed")
        return await self._get_no_disks_message().is_visible()

    async def click_create_new_disk_btn(self) -> None:
        self.log("Click Create new disk button")
        await self._get_create_new_disk_btn().click()

    async def enter_search_disk_name(self, disk_name: str) -> None:
        self.log("Enter disk name into Search input")
        await self._get_search_disk_input().fill(disk_name)

    async def is_disk_btn_displayed(self, disk_name: str) -> bool:
        self.log(f"Check if Disk {disk_name} row displayed")
        return await self._get_disk_btn(disk_name).is_visible()

    async def click_disk_btn(self, disk_name: str) -> None:
        self.log(f"Click Disk {disk_name} button")
        await self._get_disk_btn(disk_name).click()

    async def is_disk_info_view_displayed(
        self, disk_name: str, owner: str, storage_value: str, lifespan_value: str
    ) -> bool:
        self.log(f"Check if Disk {disk_name} info view displayed")
        return (
            await self._get_disk_info_view_title(disk_name).is_visible()
            and await self._get_disk_info_owner_label().is_visible()
            and await self._get_disk_info_owner_value(owner).is_visible()
            and await self._get_disk_info_storage_label().is_visible()
            and await self._get_disk_info_storage_value(storage_value).is_visible()
            and await self._get_disk_info_lifespan_label().is_visible()
            and await self._get_disk_info_lifespan_value(lifespan_value).is_visible()
            and await self._get_disk_info_delete_btn().is_visible()
        )

    async def click_delete_disk_btn(self) -> None:
        self.log("Click Delete Disk button")
        await self._get_disk_info_delete_btn().click()
