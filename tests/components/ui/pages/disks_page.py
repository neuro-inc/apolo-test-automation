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

    def _get_disk_row(self, disk_name: str) -> BaseElement:
        """
        Returns the entire <tr> row for a given disk name.
        """
        return BaseElement(
            self.page,
            selector=f"tr.contents:has(td p.truncate:text-is('{disk_name}'))",
        )

    def _get_disk_name_field(self, disk_name: str) -> BaseElement:
        """
        Returns the disk name <p> element within its cell.
        """
        return BaseElement(
            self.page,
            selector=f"tr.contents:has(td p.truncate:text-is('{disk_name}')) td:nth-child(2) p.truncate",
        )

    def _get_disk_storage_field(self, disk_name: str) -> BaseElement:
        """
        Returns the 'Used / Storage' cell value.
        """
        return BaseElement(
            self.page,
            selector=f"tr.contents:has(td p.truncate:text-is('{disk_name}')) td:nth-child(3)",
        )

    async def get_disk_storage_value(self, disk_name: str) -> str:
        return await self._get_disk_storage_field(disk_name).text_content()

    def _get_disk_owner_field(self, disk_name: str) -> BaseElement:
        """
        Returns the 'Owner' cell value.
        """
        return BaseElement(
            self.page,
            selector=f"tr.contents:has(td p.truncate:text-is('{disk_name}')) td:nth-child(4)",
        )

    async def get_disk_owner_value(self, disk_name: str) -> str:
        return await self._get_disk_owner_field(disk_name).text_content()

    def _get_disk_status_field(self, disk_name: str) -> BaseElement:
        """
        Returns the 'Status' cell value.
        """
        return BaseElement(
            self.page,
            selector=f"tr.contents:has(td p.truncate:text-is('{disk_name}')) td:nth-child(5)",
        )

    def _get_disk_created_field(self, disk_name: str) -> BaseElement:
        """
        Returns the 'Created' cell value.
        """
        return BaseElement(
            self.page,
            selector=f"tr.contents:has(td p.truncate:text-is('{disk_name}')) td:nth-child(6)",
        )

    def _get_disk_delete_btn(self, disk_name: str) -> BaseElement:
        """
        Returns the delete button element (trash icon) for a given disk row.
        """
        return BaseElement(
            self.page,
            selector=f"tr.contents:has(td p.truncate:text-is('{disk_name}')) td:nth-child(7) button:has(svg[data-icon='trash-xmark'])",
        )

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
        return await self._get_disk_row(disk_name).is_visible()

    async def click_disk_btn(self, disk_name: str) -> None:
        self.log(f"Click Disk {disk_name} button")
        await self._get_disk_row(disk_name).click()

    async def is_valid_disk_row_displayed(
        self,
        disk_name: str,
        owner: str,
        storage_value: str,
    ) -> tuple[bool, str]:
        errors = []

        disk_row = self._get_disk_row(disk_name)
        if not await disk_row.is_visible():
            return False, f"Disk '{disk_name}' row not found"

        actual_storage = (await self.get_disk_storage_value(disk_name) or "").strip()
        actual_owner = (await self.get_disk_owner_value(disk_name) or "").strip()

        # --- normalize storage (split on '/')
        parts = actual_storage.split("/")
        total_storage = parts[1].strip() if len(parts) == 2 else actual_storage

        if total_storage != storage_value:
            errors.append(
                f"Storage mismatch for '{disk_name}': expected total '{storage_value}', got '{total_storage}' (raw: '{actual_storage}')"
            )

        if actual_owner != owner:
            errors.append(
                f"Owner mismatch for '{disk_name}': expected '{owner}', got '{actual_owner}'"
            )

        delete_btn = self._get_disk_delete_btn(disk_name)
        if not await delete_btn.is_visible():
            errors.append(f"Delete button not visible for '{disk_name}'")

        if errors:
            return False, "; ".join(errors)
        return True, ""

    async def click_delete_disk_btn(self, disk_name: str) -> None:
        self.log("Click Delete Disk button")
        await self._get_disk_delete_btn(disk_name).click()
