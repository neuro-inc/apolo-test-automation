from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class InviteProjMemberPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify Invite project member popup displayed")
    async def verify_ui_popup_displayed(self, org_name: str, proj_name: str) -> None:
        assert await self._pm.invite_proj_member_popup.is_loaded(
            org_name=org_name, proj_name=proj_name
        ), "Invite project member popup should be displayed!"

    @async_step("Enter user email/username")
    async def ui_enter_user_data(self, email: str) -> None:
        await self._pm.invite_proj_member_popup.enter_user_data(email)

    @async_step("Select user role")
    async def ui_select_user_role(self, role: str) -> None:
        await self._pm.invite_proj_member_popup.select_user_role(role=role)

    @async_step("Verify Invite user button displayed")
    async def verify_ui_invite_user_btn_displayed(self, email: str) -> None:
        assert await self._pm.invite_proj_member_popup.is_invite_user_btn_displayed(
            email=email
        ), f"Invite user {email} button should be displayed!"

    @async_step("Verify Invite user button not displayed")
    async def verify_ui_invite_user_btn_not_displayed(self, email: str) -> None:
        assert not await self._pm.invite_proj_member_popup.is_invite_user_btn_displayed(
            email=email
        ), f"Invite user {email} button should not be displayed!"

    @async_step("Verify Invite button disabled")
    async def verify_ui_invite_bth_disabled(self) -> None:
        assert not await self._pm.invite_proj_member_popup.is_invite_btn_enabled(), (
            "Invite button should be disabled!"
        )

    @async_step("Click invite user button")
    async def ui_click_invite_user_btn(self, email: str) -> None:
        await self._pm.invite_proj_member_popup.click_invite_user_btn(email=email)

    @async_step("Verify Invite button enabled")
    async def verify_ui_invite_bth_enabled(self) -> None:
        assert await self._pm.invite_proj_member_popup.is_invite_btn_enabled(), (
            "Invite button should be enabled!"
        )

    @async_step("Click Invite button")
    async def ui_click_invite_btn(self) -> None:
        await self._pm.invite_proj_member_popup.click_invite_btn()
