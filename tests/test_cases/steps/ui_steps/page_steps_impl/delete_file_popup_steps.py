from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class DeleteFilePopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Delete File popup displayed")
    async def verify_ui_popup_displayed(self, name: str) -> None:
        assert await self._pm.delete_file_popup.is_loaded(name=name), (
            "Delete File popup should be displayed!"
        )

    @async_step("Click Delete button")
    async def ui_click_delete_button(self) -> None:
        await self._pm.delete_file_popup.click_delete_btn()

    @async_step("Wait for Delete File popup to disappear")
    async def ui_wait_to_disappear(self, name: str) -> None:
        await self._pm.delete_file_popup.wait_to_disappear(name=name)
