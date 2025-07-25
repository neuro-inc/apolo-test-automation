from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class InviteOrgMemberPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Invite member popup displayed")
    async def verify_ui_popup_displayed(self) -> None:
        assert await self._pm.invite_org_member_popup.is_loaded(), (
            "Invite member popup should be displayed!"
        )

    @async_step("Enter email")
    async def ui_enter_invite_email(self, email: str) -> None:
        await self._pm.invite_org_member_popup.enter_user_data(email=email)

    @async_step("Select User role in organization")
    async def ui_select_user_role(self, role: str) -> None:
        await self._pm.invite_org_member_popup.select_user_role(role=role)

    @async_step("Verify that Invite user button appeared")
    async def verify_ui_invite_user_button_displayed(self, email: str) -> None:
        assert await self._pm.invite_org_member_popup.is_invite_user_displayed(
            email=email
        ), "Invite user button should be displayed!"

    @async_step("Click Invite user button")
    async def ui_click_invite_user_button(self, email: str) -> None:
        await self._pm.invite_org_member_popup.click_invite_user_button(email=email)

    @async_step("Verify that Send invite button disabled")
    async def verify_ui_send_invite_button_disabled(self) -> None:
        assert (
            not await self._pm.invite_org_member_popup.is_send_invite_button_enabled()
        ), "Send invite button should be disabled!"

    @async_step("Verify that Send invite button enabled")
    async def verify_ui_send_invite_button_enabled(self) -> None:
        assert await self._pm.invite_org_member_popup.is_send_invite_button_enabled(), (
            "Send invite button should be enabled!"
        )

    @async_step("Click Send invite button")
    async def ui_click_send_invite_button(self) -> None:
        await self._pm.invite_org_member_popup.click_send_invite_button()

    @async_step("Wait for Invite organization member popup to disappear")
    async def ui_wait_to_disappear(self) -> None:
        await self._pm.invite_org_member_popup.wait_to_disappear()
