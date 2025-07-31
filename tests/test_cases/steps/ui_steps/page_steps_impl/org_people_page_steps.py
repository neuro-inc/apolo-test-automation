from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class OrgPeoplePageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Organization people page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.organization_people_page.is_loaded(), (
            "Organization people page should be displayed!"
        )

    @async_step("Verify that Invite people button is disabled")
    async def verify_ui_invite_ppl_btn_disabled(self) -> None:
        assert not await self._pm.organization_people_page.is_invite_people_button_enabled(), (
            "Invite people button should be disabled!"
        )

    @async_step("Verify that Invite people button is enabled")
    async def verify_ui_invite_ppl_btn_enabled(self) -> None:
        assert (
            await self._pm.organization_people_page.is_invite_people_button_enabled()
        ), "Invite people button should be enabled!"

    @async_step("Click Invite people button")
    async def ui_click_invite_people_button(self) -> None:
        await self._pm.organization_people_page.click_invite_people_button()

    @async_step("Verify that user displayed in users list")
    async def verify_ui_user_displayed_in_users_list(self, email: str) -> None:
        assert await self._pm.organization_people_page.is_org_user_row_displayed(
            email
        ), f"User {email} should be displayed in organization users list!"

    @async_step("Verify that user is not displayed in users list")
    async def verify_ui_user_not_displayed_in_users_list(self, email: str) -> None:
        assert not await self._pm.organization_people_page.is_org_user_row_displayed(
            email
        ), f"User {email} should not be displayed in organization users list!"

    @async_step("Verify that user role is valid")
    async def verify_ui_valid_user_role_displayed(self, email: str, role: str) -> None:
        user_role = await self._pm.organization_people_page.get_org_user_role(email)
        assert user_role.lower() == role.lower(), (
            f"User {email} role should be {role}, not {user_role}!"
        )

    @async_step("Verify that invited user status is valid")
    async def verify_ui_valid_user_status_displayed(
        self, email: str, status: str
    ) -> None:
        user_status = await self._pm.organization_people_page.get_org_user_status(email)
        assert status.lower() in user_status.lower(), (
            f"Invited user status should be {user_status}!"
        )

    @async_step("Verify that user credits amount is valid")
    async def verify_ui_valid_user_credits_displayed(
        self, email: str, credits: str
    ) -> None:
        user_credits = await self._pm.organization_people_page.get_org_user_credits(
            email
        )
        assert credits == user_credits.strip(), (
            f"User credits should be {credits}, not {user_credits}!"
        )

    @async_step("Click three dots button")
    async def ui_click_three_dots_btn(self, email: str) -> None:
        await self._pm.organization_people_page.click_three_dots_btn(email=email)

    @async_step("Verify that Edit user button is disabled")
    async def verify_ui_edit_user_btn_disabled(self) -> None:
        assert not await self._pm.organization_people_page.is_edit_user_btn_enabled(), (
            "Edit user button should be disabled!"
        )

    @async_step("Verify that Edit user button is enabled")
    async def verify_ui_edit_user_btn_enabled(self) -> None:
        assert await self._pm.organization_people_page.is_edit_user_btn_enabled(), (
            "Edit user button should be enabled!"
        )

    @async_step("Click Edit user button")
    async def ui_click_edit_user_btn(self) -> None:
        await self._pm.organization_people_page.click_edit_user_btn()

    @async_step("Verify that Remove user button is disabled")
    async def verify_ui_remove_user_btn_disabled(self) -> None:
        assert (
            not await self._pm.organization_people_page.is_remove_user_btn_enabled()
        ), "Remove user button should be disabled!"

    @async_step("Verify that Remove user button is enabled")
    async def verify_ui_remove_user_btn_enabled(self) -> None:
        assert await self._pm.organization_people_page.is_remove_user_btn_enabled(), (
            "Remove user button should be enabled!"
        )

    @async_step("Click Remove user button")
    async def ui_click_remove_user_btn(self) -> None:
        await self._pm.organization_people_page.click_remove_user_btn()

    @async_step("Enter Search input value")
    async def ui_enter_search_input_value(self, value: str) -> None:
        await self._pm.organization_people_page.enter_search_value(value)
