from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class EditOrgUserPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        username = kwargs.get("username")
        if not isinstance(username, str):
            raise ValueError("Expected 'username' to be a non-empty string in kwargs")
        return (
            await self._get_edit_user_title(username).is_visible()
            and await self._get_role_dropdown().is_visible()
            and await self._get_credits_input().is_visible()
            and await self._get_save_btn().is_visible()
        )

    def _get_edit_user_title(self, username: str) -> BaseElement:
        return BaseElement(self.page, "h2", has_text=f"Edit User {username}")

    def _get_role_dropdown(self) -> BaseElement:
        return BaseElement(self.page, 'select[name="role"]')

    async def select_new_role(self, role: str) -> None:
        roles = ("user", "manager", "admin")
        if role.lower() not in roles:
            raise ValueError(f"Expected role {role} to be in {roles}")
        self.log(f"Select {role} role")
        await self._get_role_dropdown().select_option(role.lower())

    def _get_credits_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="credits"]')

    def _get_save_btn(self) -> BaseElement:
        return BaseElement(self.page, by_role="button", name="Save")

    async def click_save_btn(self) -> None:
        self.log("Click Save button")
        await self._get_save_btn().click()

    async def wait_to_disappear(self, username: str) -> None:
        """
        Waits until key elements of the page disappear (popup is closed).
        """
        self.log("Wait for Edit organization user popup to disappear")

        await self._get_edit_user_title(username).locator.wait_for(state="detached")
        await self._get_role_dropdown().locator.wait_for(state="detached")
        await self._get_credits_input().locator.wait_for(state="detached")
        await self._get_save_btn().locator.wait_for(state="detached")
