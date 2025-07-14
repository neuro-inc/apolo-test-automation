import re
from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class InvitedToOrgPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._page_title = BaseElement(
            self.page, "h3", has_text="You have been invited to organization"
        )

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        await self.page.wait_for_timeout(1000)
        org_name = kwargs.get("org_name")
        user_role = kwargs.get("user_role")
        if not isinstance(org_name, str) or not org_name:
            raise ValueError("Expected 'org_name' to be a non-empty string in kwargs")
        if not isinstance(user_role, str) or not user_role:
            raise ValueError("Expected 'user_role' to be a non-empty string in kwargs")
        return (
            await self._page_title.expect_to_be_loaded()
            and await self._get_org_name_field(org_name).expect_to_be_loaded()
            and await self._get_user_role_field(user_role.lower()).expect_to_be_loaded()
            and await self._get_accept_and_go_button().expect_to_be_loaded()
        )

    def _get_org_name_field(self, org_name: str) -> BaseElement:
        return BaseElement(
            self.page,
            "p.text-h6",
            has_text=re.compile(rf"Organization name:\s*{re.escape(org_name)}"),
        )

    def _get_user_role_field(self, user_role: str) -> BaseElement:
        return BaseElement(self.page, "p.text-h6", has_text=user_role)

    def _get_accept_and_go_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Accept and Go")

    async def click_accept_and_go_button(self) -> None:
        self.log("Click accept and Go button")
        btn = self._get_accept_and_go_button()
        await btn.hover()
        await self.page.wait_for_timeout(500)
        await btn.click()
        self.log("Wait for network idle")
        await self.page.wait_for_load_state("networkidle")
        self.log("Network idle done")
