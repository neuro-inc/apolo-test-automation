from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class RenameFilePopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Rename File popup displayed")
    async def verify_ui_popup_displayed(self) -> None:
        assert await self._pm.rename_file_popup.is_loaded(), (
            "Rename File popup should be displayed!"
        )

    @async_step("Enter new File name")
    async def ui_enter_new_file_name(self, name: str) -> None:
        await self._pm.rename_file_popup.enter_new_name(name=name)

    @async_step("Click Rename button")
    async def ui_click_rename_button(self) -> None:
        await self._pm.rename_file_popup.click_rename_btn()

    @async_step("Wait for Rename File popup to disappear")
    async def ui_wait_to_disappear(self) -> None:
        await self._pm.rename_file_popup.wait_to_disappear()
