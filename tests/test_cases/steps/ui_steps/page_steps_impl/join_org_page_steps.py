from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class JoinOrgPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify Join organization page displayed")
    async def verify_ui_page_displayed(self, username: str) -> None:
        assert await self._pm.join_organization_page.is_loaded(username=username), (
            "Join organization page should be displayed!"
        )

    @async_step("Click create organization button")
    async def ui_click_create_organization_button(self) -> None:
        await self._pm.join_organization_page.click_create_organization_button()
