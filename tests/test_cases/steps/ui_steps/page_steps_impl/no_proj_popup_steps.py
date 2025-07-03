from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class NoProjPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify No project popup displayed")
    async def verify_ui_no_proj_popup_displayed(self, org_name: str) -> None:
        assert await self._pm.no_proj_popup.is_loaded(org_name=org_name), (
            "No project popup should be displayed!"
        )

    @async_step("Click Create new project button")
    async def ui_click_create_new_proj_button(self) -> None:
        await self._pm.no_proj_popup.click_create_proj_button()
