import re
from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class CreateDiskPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the popup is considered loaded (key elements are visible).
        """
        self.log("Check if popup loaded")
        return (
            await self._get_create_new_disk_title().is_visible()
            and await self._get_disk_storage_input().is_visible()
            and await self._get_storage_units_dropdown().is_visible()
            and await self._get_disk_name_input().is_visible()
            and await self._get_disk_lifespan_input().is_visible()
            and await self._get_create_disk_btn().is_visible()
        )

    def _get_create_new_disk_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Create New Disk")

    def _get_disk_storage_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="storage"]')

    async def enter_storage_value(self, storage_value: str) -> None:
        self.log(f"Enter storage value: {storage_value}")
        await self._get_disk_storage_input().fill(storage_value)

    def _get_storage_units_dropdown(self) -> BaseElement:
        return BaseElement(
            self.page, 'select:has(option[value="GB"]):has(option[value="TB"])'
        )

    async def select_storage_units(self, storage_units: str) -> None:
        units = ("GB", "TB")
        if storage_units not in units:
            raise ValueError(f"Expected {storage_units} to be in {units}")
        self.log(f"Select storage units: {storage_units}")
        await self._get_storage_units_dropdown().select_option(storage_units)

    def _get_disk_name_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="name"]')

    async def enter_disk_name(self, disk_name: str) -> None:
        self.log(f"Enter disk name: {disk_name}")
        await self._get_disk_name_input().fill(disk_name)

    def _get_disk_lifespan_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="lifeSpan"]')

    async def enter_disk_lifespan(self, lifespan_value: str) -> None:
        self.log(f"Enter disk lifespan: {lifespan_value}")
        await self._get_disk_lifespan_input().fill(lifespan_value)

    def _get_create_disk_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text=re.compile(r"^Create$"))

    async def click_create_disk_btn(self) -> None:
        self.log("Click Create button")
        await self._get_create_disk_btn().click()

    async def wait_to_disappear(self) -> None:
        """
        Waits until key elements of the popup disappear (popup is closed).
        """
        self.log("Wait for Create New Secret popup to disappear")

        await self._get_create_new_disk_title().locator.wait_for(state="detached")
        await self._get_disk_storage_input().locator.wait_for(state="detached")
        await self._get_storage_units_dropdown().locator.wait_for(state="detached")
        await self._get_disk_name_input().locator.wait_for(state="detached")
        await self._get_disk_lifespan_input().locator.wait_for(state="detached")
        await self._get_create_disk_btn().locator.wait_for(state="detached")
