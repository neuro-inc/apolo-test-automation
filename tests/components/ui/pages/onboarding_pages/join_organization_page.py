from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class JoinOrganizationPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._join_organization_title = BaseElement(
            self.page, "h5.text-h3", has_text="Join Organization"
        )
        self._pass_username_text_field = BaseElement(
            self.page,
            "p",
            has_text="Pass your username to the organization manager to join existing organization",
        )
        self._establish_new_organization_text_field = BaseElement(
            self.page, "p", has_text="Or establish a new organization"
        )
        self._create_organization_button = BaseElement(
            self.page, "button", has_text="Create organization"
        )

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        await self.page.wait_for_timeout(1000)
        username = kwargs.get("username")
        if not isinstance(username, str):
            raise ValueError("Expected 'username' to be a non-empty string in kwargs")
        return (
            await self._join_organization_title.expect_to_be_loaded()
            and await self._pass_username_text_field.expect_to_be_loaded()
            and await self._get_username_input(username).expect_to_be_loaded()
            and await self._establish_new_organization_text_field.expect_to_be_loaded()
            and await self._create_organization_button.expect_to_be_loaded()
        )

    def _get_username_input(self, username: str) -> BaseElement:
        return BaseElement(self.page, f'div:has(span:text("{username}")) > button')

    async def click_create_organization_button(self) -> None:
        self.log("Click create organization button")
        btn = self._create_organization_button
        await self.page.wait_for_timeout(500)
        await btn.hover()
        await btn.click()
        await self.page.wait_for_timeout(500)
