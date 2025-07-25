from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class ProjPeoplePageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify People page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.project_people_page.is_loaded(), (
            "Project people page should be displayed!"
        )

    @async_step("Click Invite people button")
    async def ui_click_invite_people_proj_people_btn(self) -> None:
        await self._pm.project_people_page.click_invite_people_btn()

    @async_step("Verify user displayed in users list")
    async def verify_ui_user_displayed_in_users_list(self, username: str) -> None:
        assert await self._pm.project_people_page.is_user_row_displayed(
            username=username
        ), f"User {username} should be displayed in the project users list!"

    @async_step("Verify user is not displayed in users list")
    async def verify_ui_user_not_displayed_in_users_list(self, username: str) -> None:
        assert not await self._pm.project_people_page.is_user_row_displayed(
            username=username
        ), f"User {username} should not be displayed in the project users list!"

    @async_step("Verify user role is valid")
    async def verify_ui_user_role(self, username: str, role: str) -> None:
        value = await self._pm.project_people_page.get_row_role(username=username)
        assert value.lower() == role.lower(), f"User role should be {role}!"

    @async_step("Verify user email is valid")
    async def verify_ui_invited_user_email(self, username: str, email: str) -> None:
        value = await self._pm.project_people_page.get_row_email(username=username)
        assert value.lower() == email.lower(), f"User email should be {email}!"

    @async_step("Click Delete member button")
    async def ui_click_delete_member_btn(self, username: str) -> None:
        await self._pm.project_people_page.click_row_delete_btn(username=username)

    @async_step("Verify delete member button disabled")
    async def verify_ui_delete_member_btn_disabled(self, username: str) -> None:
        assert not await self._pm.project_people_page.is_row_delete_btn_enabled(
            username=username
        ), f"Delete button for user {username} should be disabled!"

    @async_step("Click Edit member button")
    async def ui_click_edit_member_btn(self, username: str) -> None:
        await self._pm.project_people_page.click_row_edit_btn(username=username)

    @async_step("Verify edit member button disabled")
    async def verify_ui_edit_member_btn_disabled(self, username: str) -> None:
        assert not await self._pm.project_people_page.is_row_edit_btn_enabled(
            username=username
        ), f"Edit button for user {username} should be disabled!"
