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
