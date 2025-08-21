from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class RemoveProjMemberPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Remove project member popup displayed")
    async def verify_ui_popup_displayed(self, username: str) -> None:
        assert await self._pm.remove_proj_member_popup.is_loaded(username=username), (
            "Remove project member popup should be displayed!"
        )

    @async_step("Click Remove button")
    async def ui_click_remove_button(self) -> None:
        await self._pm.remove_proj_member_popup.click_remove_btn()

    @async_step("Wait for Remove project member popup to disappear")
    async def ui_wait_to_disappear(self, username: str) -> None:
        await self._pm.remove_proj_member_popup.wait_to_disappear(username=username)
