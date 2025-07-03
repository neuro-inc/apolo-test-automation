from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class OrgPeoplePageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Organization people page displayed")
    async def verify_ui_org_people_page_displayed(self) -> None:
        assert await self._pm.organization_people_page.is_loaded(), (
            "Organization people page should be displayed!"
        )

    @async_step("Click Invite people button")
    async def ui_click_invite_people_button(self) -> None:
        await self._pm.organization_people_page.click_invite_people_button()

    @async_step("Verify that invited user displayed in users list")
    async def verify_ui_user_displayed_in_users_list(self, email: str) -> None:
        assert await self._pm.organization_people_page.is_org_user_row_displayed(
            email
        ), "Invited user should be displayed in organization users list!"

    @async_step("Verify that invited user role is valid")
    async def verify_ui_valid_user_role_displayed(self, email: str, role: str) -> None:
        user_role = await self._pm.organization_people_page.get_org_user_role(email)
        assert user_role.lower() == role.lower(), f"Invited user role should be {role}!"

    @async_step("Verify that invited user status is valid")
    async def verify_ui_valid_user_status_displayed(
        self, email: str, status: str
    ) -> None:
        user_status = await self._pm.organization_people_page.get_org_user_status(email)
        assert status.lower() in user_status.lower(), (
            f"Invited user status should be {user_status}!"
        )
