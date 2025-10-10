from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class DisksPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Disks page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.disks_page.is_loaded(), "Disks page should be displayed!"

    @async_step("Verify that Disks page is not displayed")
    async def verify_ui_page_not_displayed(self) -> None:
        assert not await self._pm.disks_page.is_loaded(), (
            "Disks page should not be displayed!"
        )

    @async_step("Verify that no disks message displayed")
    async def verify_ui_no_disks_message_displayed(self) -> None:
        assert await self._pm.disks_page.is_no_disks_message_displayed(), (
            "No disks message should be displayed!"
        )

    @async_step("Verify that no disks message is not displayed")
    async def verify_ui_no_disks_message_not_displayed(self) -> None:
        assert not await self._pm.disks_page.is_no_disks_message_displayed(), (
            "No disks message should not be displayed!"
        )

    @async_step("Click Create New Disk button")
    async def ui_click_create_new_disk_btn(self) -> None:
        await self._pm.disks_page.click_create_new_disk_btn()

    @async_step("Enter Disk name into Search input")
    async def ui_enter_disk_name_into_search_input(self, disk_name: str) -> None:
        await self._pm.disks_page.enter_search_disk_name(disk_name)

    @async_step("Verify Disk row displayed")
    async def verify_ui_disk_row_displayed(self, disk_name: str) -> None:
        assert await self._pm.disks_page.is_disk_btn_displayed(disk_name), (
            f"Disk {disk_name} button should be displayed!"
        )

    @async_step("Verify Disk row not displayed")
    async def verify_ui_disk_row_not_displayed(self, disk_name: str) -> None:
        assert not await self._pm.disks_page.is_disk_btn_displayed(disk_name), (
            f"Disk {disk_name} button should not be displayed!"
        )

    @async_step("Verify valid Disk info displayed")
    async def verify_ui_valid_disk_info_displayed(
        self, disk_name: str, owner: str, storage_value: str
    ) -> None:
        result, error_message = await self._pm.disks_page.is_valid_disk_row_displayed(
            disk_name, owner, storage_value
        )
        assert result, error_message

    @async_step("Click Delete Disk button")
    async def ui_click_delete_disk_btn(self, disk_name: str) -> None:
        await self._pm.disks_page.click_delete_disk_btn(disk_name)
