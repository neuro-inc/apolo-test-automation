from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class AppsPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify Apps page displayed")
    async def verify_ui_apps_page_displayed(self) -> None:
        assert await self._pm.apps_page.is_loaded(), (
            "Create project popup should be displayed!"
        )
