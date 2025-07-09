import re
from typing import Any, cast
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class InviteProjMemberPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        org_name = kwargs.get("org_name")
        if not isinstance(org_name, str):
            raise ValueError("Expected 'org_name' to be a non-empty string in kwargs")
        proj_name = kwargs.get("proj_name")
        if not isinstance(proj_name, str):
            raise ValueError("Expected 'proj_name' to be a non-empty string in kwargs")
        return (
            await self._get_invite_member_title().expect_to_be_loaded()
            and await self._get_invite_user_text_field(
                org_name=org_name, proj_name=proj_name
            ).expect_to_be_loaded()
            and await self._get_user_data_input().expect_to_be_loaded()
        )

    def _get_invite_member_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Invite Member")

    def _get_invite_user_text_field(self, org_name: str, proj_name: str) -> BaseElement:
        return BaseElement(
            self.page,
            "p.text-footnote.text-neural-04",
            has_text=re.compile(
                rf"Invite user to\s*{proj_name}\s*project in\s*{org_name}\s*organization"
            ),
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

    def _get_role_selector(self) -> BaseElement:
        return BaseElement(
            self.page,
            'select:has(option:has-text("Reader"))'
            ':has(option:has-text("Writer"))'
            ':has(option:has-text("Manager"))'
            ':has(option:has-text("Admin"))',
        )

    async def select_user_role(self, role: str) -> None:
        roles = ("reader", "writer", "manager", "admin")
        if role.lower() not in roles:
            raise ValueError(f"Expected role {role} to be in {roles}")
        self.log(f"Select user role {role}")
        await self._get_role_selector().select_option(role.lower())

    def _get_invite_user_btn(self, email: str) -> BaseElement:
        return BaseElement(self.page, "button", has_text=re.compile(re.escape(email)))

    async def is_invite_user_btn_displayed(self, email: str) -> bool:
        self.log(f"Check if invite user {email} button displayed")
        return await self._get_invite_user_btn(email).is_visible()

    async def click_invite_user_btn(self, email: str) -> None:
        self.log(f"Click invite user {email} button")
        await self._get_invite_user_btn(email).click()

    def _get_cancel_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Cancel")

    async def click_cancel_btn(self) -> None:
        self.log("Click Cancel button")
        await self._get_cancel_btn().click()

    def _get_invite_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text=re.compile(r"^Invite$"))

    async def is_invite_btn_enabled(self) -> bool:
        return await self._get_invite_btn().is_enabled()

    async def click_invite_btn(self) -> None:
        self.log("Click Invite button")
        await self._get_invite_btn().click()
        await self.page.wait_for_timeout(500)

    async def wait_to_disappear(self, org_name: str, proj_name: str) -> None:
        """
        Waits until key elements of the page disappear (popup is closed).
        """
        self.log("Wait for Remove organization user popup to disappear")

        await self._get_invite_member_title().locator.wait_for(state="detached")
        await self._get_invite_user_text_field(
            org_name=org_name, proj_name=proj_name
        ).locator.wait_for(state="detached")
        await self._get_cancel_btn().locator.wait_for(state="detached")
        await self._get_user_data_input().locator.wait_for(state="detached")
