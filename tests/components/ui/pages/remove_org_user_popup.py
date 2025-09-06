import re
from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class RemoveOrgUserPopup(BasePage):
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
            await self._get_remove_user_title().is_visible()
            and await self._get_remove_user_description(username).is_visible()
            and await self._get_cancel_btn().is_visible()
            and await self._get_remove_btn().is_visible()
        )

    def _get_remove_user_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Remove User")

    def _get_remove_user_description(self, username: str) -> BaseElement:
        return BaseElement(
            self.page,
            "p",
            has_text=f"The user {username} will no longer have access to the organization",
        )

    def _get_cancel_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Cancel")

    def _get_remove_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text=re.compile(r"^Remove$"))

    async def click_remove_btn(self) -> None:
        self.log("Click Remove button")
        await self._get_remove_btn().click()

    async def wait_to_disappear(self, username: str) -> None:
        """
        Waits until key elements of the page disappear (popup is closed).
        """
        self.log("Wait for Remove organization user popup to disappear")

        await self._get_remove_user_title().locator.wait_for(state="detached")
        await self._get_remove_user_description(username).locator.wait_for(
            state="detached"
        )
        await self._get_cancel_btn().locator.wait_for(state="detached")
        await self._get_remove_btn().locator.wait_for(state="detached")
