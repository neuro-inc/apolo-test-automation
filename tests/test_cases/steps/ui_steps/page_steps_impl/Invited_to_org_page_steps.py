from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class InvitedToOrgPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Invited to organization page displayed")
    async def verify_ui_invite_to_org_page_displayed(
        self, org_name: str, user_role: str
    ) -> None:
        assert await self._pm.invited_to_org_page.is_loaded(
            org_name=org_name, user_role=user_role
        ), "Invited to organization page should be displayed!"

    @async_step("Click Accept and Go button")
    async def ui_click_accept_and_go_button(self) -> None:
        await self._pm.invited_to_org_page.click_accept_and_go_button()
