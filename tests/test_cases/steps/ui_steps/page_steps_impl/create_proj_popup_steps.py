from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class CreateProjPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify Create project popup displayed")
    async def verify_ui_create_proj_popup_displayed(self, org_name: str) -> None:
        assert await self._pm.create_proj_popup.is_loaded(org_name=org_name), (
            "Create project popup should be displayed!"
        )

    @async_step("Enter project name")
    async def ui_enter_proj_name(self, proj_name: str) -> None:
        await self._pm.create_proj_popup.enter_proj_name(proj_name=proj_name)

    @async_step("Select user role")
    async def ui_select_role(self, role: str) -> None:
        await self._pm.create_proj_popup.select_default_role(role=role)

    @async_step("Click Create button")
    async def ui_click_create_button(self) -> None:
        await self._pm.create_proj_popup.click_create_button()

    @async_step("Click project default checkbox")
    async def ui_click_make_default_checkbox(self) -> None:
        await self._pm.create_proj_popup.click_proj_default_checkbox()
