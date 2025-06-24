from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class OrganizationSettingsPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        email = kwargs.get("email")
        if not isinstance(email, str):
            raise ValueError("Expected 'email' to be a non-empty string in kwargs")
        username = kwargs.get("username")
        if not isinstance(username, str):
            raise ValueError("Expected 'username' to be a non-empty string in kwargs")
        return await self._get_log_out_button().expect_to_be_loaded()

    def _get_select_org_button(self, org_name: str) -> BaseElement:
        return BaseElement(self.page, f"button:has(p[title={org_name}])")

    async def is_select_org_button_displayed(self, org_name: str) -> bool:
        self.log(f"Check if select organization {org_name} button displayed")
        return await self._get_select_org_button(org_name).is_visible()

    async def click_select_organization_button(self, org_name: str) -> None:
        self.log(f"Select {org_name} organization")
        await self._get_select_org_button(org_name).click()

    def _get_settings_button(self) -> BaseElement:
        return BaseElement(self.page, "a", has_text="Settings")

    async def click_settings_button(self) -> None:
        self.log("Click settings button")
        await self._get_settings_button().click()

    def _get_people_button(self) -> BaseElement:
        return BaseElement(self.page, "a", has_text="People")

    async def click_people_button(self) -> None:
        self.log("Click People button")
        await self.page.wait_for_timeout(300)
        await self._get_people_button().click()

    def _get_billing_button(self) -> BaseElement:
        return BaseElement(self.page, "a", has_text="Billing")

    async def click_billing_button(self) -> None:
        self.log("Click Billing button")
        await self._get_billing_button().click()

    def _get_create_new_organization_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Create new organization")

    async def click_create_new_organization_button(self) -> None:
        self.log("Click Create new organization button")
        await self._get_create_new_organization_button().click()

    def _get_user_email_label(self, email: str) -> BaseElement:
        return BaseElement(self.page, f'p.truncate[title="{email}"]')

    async def is_user_email_label_displayed(self, email: str) -> bool:
        self.log(f"Check if {email} email label displayed")
        return await self._get_user_email_label(email).is_visible()

    def _get_user_username_label(self, username: str) -> BaseElement:
        return BaseElement(self.page, "p.truncate", has_text=username)

    async def is_user_username_label_displayed(self, username: str) -> bool:
        self.log(f"Check if {username} username label displayed")
        return await self._get_user_username_label(username).is_visible()

    def _get_log_out_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Log out")

    async def is_log_out_button_displayed(self) -> bool:
        self.log("Check if log out button displayed")
        return await self._get_log_out_button().is_visible()

    async def click_log_out_button(self) -> None:
        self.log("Click Log out button")
        await self._get_log_out_button().click()
