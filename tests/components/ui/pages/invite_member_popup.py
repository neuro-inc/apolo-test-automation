import re
from typing import Any, cast
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class InviteMemberPopup(BasePage):
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

    async def is_user_data_input_displayed(self) -> bool:
        self.log("Check if email/username input displayed")
        return await self._get_user_data_input().is_visible()

    async def enter_user_data(
        self,
        email: str | None = None,  # 👈 explicit Optional
        username: str | None = None,  # 👈 explicit Optional
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

    async def select_user_role(self) -> None:
        self.log("Select user role")
        await self._get_user_role_dropdown().select_option("user")

    async def select_manager_role(self) -> None:
        self.log("Select manager role")
        await self._get_user_role_dropdown().select_option("manager")

    async def select_admin_role(self) -> None:
        self.log("Select admin role")
        await self._get_user_role_dropdown().select_option("admin")

    def _get_invite_user_button(self, email: str) -> BaseElement:
        return BaseElement(
            self.page, by_role="button", name=re.compile(rf"Invite user.*{email}")
        )

    async def is_invite_user_displayed(self, email: str) -> bool:
        self.log(f"Check if Invite user {email} button displayed")
        return await self._get_invite_user_button(email).is_visible()

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
