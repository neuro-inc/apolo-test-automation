from typing import Any, cast
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class InviteOrgMemberPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_user_data_input().expect_to_be_loaded()
            and await self._get_user_role_dropdown().expect_to_be_loaded()
            and await self._get_cancel_button().expect_to_be_loaded()
            and await self._get_send_invite_button().expect_to_be_loaded()
        )

    def _get_user_data_input(self) -> BaseElement:
        return BaseElement(self.page, by_label="Username / Email")

    async def enter_user_data(
        self,
        email: str | None = None,
        username: str | None = None,
    ) -> None:
        if (email is None) == (username is None):  # both None or both non-None
            raise ValueError(
                f"Provide exactly one of email or username, got: {email}, {username}"
            )

        value = cast(str, email or username)
        self.log(f"Enter {value}")
        await self._get_user_data_input().fill(value)

    def _get_user_role_dropdown(self) -> BaseElement:
        return BaseElement(
            self.page, 'select:has-text("User"):has-text("Manager"):has-text("Admin")'
        )

    async def select_user_role(self, role: str) -> None:
        roles = ("user", "manager", "admin")
        if role.lower() not in roles:
            raise ValueError(f"Expected role {role} to be in {roles}")
        self.log(f"Select {role} role")
        await self._get_user_role_dropdown().select_option(role.lower())

    async def select_manager_role(self) -> None:
        self.log("Select manager role")
        await self._get_user_role_dropdown().select_option("manager")

    async def select_admin_role(self) -> None:
        self.log("Select admin role")
        await self._get_user_role_dropdown().select_option("admin")

    def _get_invite_user_button(self, email: str) -> BaseElement:
        return BaseElement(self.page, f'button:has(p:text("{email}"))')

    async def is_invite_user_displayed(self, email: str) -> bool:
        self.log(f"Check if Invite user {email} button displayed")
        return await self._get_invite_user_button(email).wait_until_clickable()

    async def click_invite_user_button(self, email: str) -> None:
        self.log(f"Click Invite user {email}")
        await self._get_invite_user_button(email).click()

    def _get_cancel_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Cancel")

    async def click_cancel_button(self) -> None:
        self.log("Click Cancel button")
        await self._get_cancel_button().click()

    def _get_send_invite_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Send invite")

    async def is_send_invite_button_enabled(self) -> bool:
        self.log("Check if send invite button enabled")
        return await self._get_send_invite_button().is_enabled()

    async def click_send_invite_button(self) -> None:
        self.log("Click Send invite button")
        await self._get_send_invite_button().click()
        await self.page.wait_for_timeout(500)

    async def wait_to_disappear(self) -> None:
        """
        Waits until key elements of the page disappear (popup is closed).
        """
        self.log("Wait for Invite organization member popup to disappear")

        await self._get_user_data_input().locator.wait_for(state="detached")
        await self._get_user_role_dropdown().locator.wait_for(state="detached")
        await self._get_cancel_button().locator.wait_for(state="detached")
        await self._get_send_invite_button().locator.wait_for(state="detached")
