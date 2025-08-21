from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class CreateDiskPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Create New Disk popup displayed")
    async def verify_ui_popup_displayed(self) -> None:
        assert await self._pm.create_disk_popup.is_loaded(), (
            "Create New Disk popup should be displayed!"
        )

    @async_step("Enter Disk storage value")
    async def ui_enter_disk_storage_value(self, storage_value: str) -> None:
        await self._pm.create_disk_popup.enter_storage_value(storage_value)

    @async_step("Select Disk storage units")
    async def ui_select_disk_storage_units(self, storage_units: str) -> None:
        await self._pm.create_disk_popup.select_storage_units(storage_units)

    @async_step("Enter Disk name")
    async def ui_enter_disk_name(self, disk_name: str) -> None:
        await self._pm.create_disk_popup.enter_disk_name(disk_name)

    @async_step("Enter Disk lifespan value")
    async def ui_enter_disk_lifespan_value(self, lifespan_value: str) -> None:
        await self._pm.create_disk_popup.enter_disk_lifespan(lifespan_value)

    @async_step("Click Create button")
    async def ui_click_create_disk_btn(self) -> None:
        await self._pm.create_disk_popup.click_create_disk_btn()

    @async_step("Wait for Create New Disk popup to disappear")
    async def ui_wait_to_disappear(self) -> None:
        await self._pm.create_disk_popup.wait_to_disappear()
