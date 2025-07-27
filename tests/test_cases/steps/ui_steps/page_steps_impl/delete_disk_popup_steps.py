from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class DeleteDiskPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Delete Disk popup displayed")
    async def verify_ui_popup_displayed(self, disk_name: str) -> None:
        assert await self._pm.delete_disk_popup.is_loaded(disk_name=disk_name), (
            "Delete Disk popup should be displayed!"
        )

    @async_step("Click Cancel button")
    async def ui_click_cancel_btn(self) -> None:
        await self._pm.delete_disk_popup.click_cancel_btn()

    @async_step("Click Delete button")
    async def ui_click_delete_btn(self) -> None:
        await self._pm.delete_disk_popup.click_delete_btn()

    @async_step("Wait for Delete Disk popup to disappear")
    async def ui_wait_to_disappear(self, disk_name: str) -> None:
        await self._pm.delete_disk_popup.wait_to_disappear(disk_name)
