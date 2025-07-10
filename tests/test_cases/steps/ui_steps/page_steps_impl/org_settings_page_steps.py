from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class OrgSettingsPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Organization settings page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.organization_settings_page.is_loaded(), (
            "Organization settings page should be displayed!"
        )

    @async_step("Enter credits amount")
    async def ui_enter_credits_amount(self, value: str) -> None:
        await self._pm.organization_settings_page.enter_credits_amount(value=value)

    @async_step("Click Save button")
    async def ui_click_save_button(self) -> None:
        await self._pm.organization_settings_page.click_save_button()
