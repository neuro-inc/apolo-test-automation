from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class ProjInfoPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify Projects info popup displayed")
    async def verify_ui_projects_info_popup_displayed(self, proj_name: str) -> None:
        assert await self._pm.projects_info_popup.is_loaded(proj_name=proj_name), (
            "Projects info popup should be displayed!"
        )

    @async_step("Verify select project button in Projects info popup displayed")
    async def verify_ui_other_proj_displayed_in_info(self, proj_name: str) -> None:
        assert await self._pm.projects_info_popup.is_select_proj_button_displayed(
            proj_name=proj_name
        ), f"Select {proj_name} button should be displayed!"

    @async_step("Click People button on the Projects info popup")
    async def ui_click_people_btn_proj_info_popup(self) -> None:
        await self._pm.projects_info_popup.click_people_btn()

    @async_step("Click Create new project button")
    async def ui_click_create_new_proj_button(self) -> None:
        await self._pm.projects_info_popup.click_create_new_proj_btn()
