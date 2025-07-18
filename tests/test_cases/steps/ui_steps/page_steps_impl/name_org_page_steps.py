from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager
from tests.utils.test_data_management.test_data import DataManager


class NameOrgPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
        data_manager: DataManager,
    ) -> None:
        self._pm = page_manager
        self._data_manager = data_manager

    @async_step("Verify Name organization page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.name_your_organization_page.is_loaded(), (
            "Name organization page should be displayed!"
        )

    @async_step("Enter organization name")
    async def ui_enter_organization_name(self, org_name: str) -> None:
        page = self._pm.name_your_organization_page
        await page.enter_organization_name(org_name)

    @async_step("Click next button")
    async def ui_click_next_button(self) -> None:
        await self._pm.name_your_organization_page.click_next_button()
