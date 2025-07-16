from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class NewFolderPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify New Folder popup displayed")
    async def verify_ui_popup_displayed(self) -> None:
        assert await self._pm.new_folder_popup.is_loaded(), (
            "New Folder popup should be displayed!"
        )

    @async_step("Wait New Folder popup to disappear")
    async def ui_wait_to_disappear(self) -> None:
        await self._pm.new_folder_popup.wait_to_disappear()

    @async_step("Enter folder name")
    async def ui_enter_folder_name(self, name: str) -> None:
        await self._pm.new_folder_popup.enter_folder_name(name=name)

    @async_step("Click Create button")
    async def ui_click_create_btn(self) -> None:
        await self._pm.new_folder_popup.click_create_btn()
