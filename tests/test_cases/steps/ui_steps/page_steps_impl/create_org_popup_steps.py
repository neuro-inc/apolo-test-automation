from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class CreateOrgPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify Create organization popup displayed")
    async def verify_ui_popup_displayed(self) -> None:
        assert await self._pm.create_org_popup.is_loaded(), (
            "Create organization popup should be displayed!"
        )

    @async_step("Enter organization name")
    async def ui_enter_org_name(self, org_name: str) -> None:
        await self._pm.create_org_popup.enter_org_name(org_name=org_name)

    @async_step("Click Create button")
    async def ui_click_create_button(self) -> None:
        await self._pm.create_org_popup.click_create_button()

    @async_step("Wait for Create organization popup disappear")
    async def ui_wait_to_disappear(self) -> None:
        await self._pm.create_org_popup.wait_to_disappear()
