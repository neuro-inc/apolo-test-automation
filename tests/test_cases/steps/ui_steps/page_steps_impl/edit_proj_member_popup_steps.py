from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class EditProjMemberPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Edit project member popup displayed")
    async def verify_ui_popup_displayed(self, username: str) -> None:
        assert await self._pm.edit_proj_member_popup.is_loaded(username=username), (
            "Edit organization user popup should be displayed!"
        )

    @async_step("Select new role for project member")
    async def ui_select_new_user_role(self, role: str) -> None:
        await self._pm.edit_proj_member_popup.select_new_role(role)

    @async_step("Click Save button")
    async def ui_click_save_button(self) -> None:
        await self._pm.edit_proj_member_popup.click_save_btn()

    @async_step("Wait for Edit project member popup to disappear")
    async def ui_wait_to_disappear(self, username: str) -> None:
        await self._pm.edit_proj_member_popup.wait_to_disappear(username=username)
