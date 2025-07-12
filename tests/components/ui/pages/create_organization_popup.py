import re
from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class CreateOrganizationPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_create_org_title().expect_to_be_loaded()
            and await self._get_org_name_input().expect_to_be_loaded()
            and await self._get_cancel_button().expect_to_be_loaded()
            and await self._get_create_button().expect_to_be_loaded()
        )

    def _get_create_org_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Create Organization")

    def _get_org_name_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="name"]')

    async def enter_org_name(self, org_name: str) -> None:
        self.log(f"Enter new organization name {org_name}")
        await self._get_org_name_input().fill(org_name)

    def _get_cancel_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Cancel")

    async def click_cancel_button(self) -> None:
        self.log("Click Cancel button")
        await self._get_cancel_button().click()

    def _get_create_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text=re.compile(r"^Create$"))

    async def click_create_button(self) -> None:
        self.log("Click Create button")
        await self._get_create_button().click()
        await self.page.wait_for_timeout(300)

    async def wait_to_disappear(self) -> None:
        """
        Waits until key elements of the page disappear (popup is closed).
        """
        self.log("Wait for Create organization popup to disappear")

        await self._get_create_org_title().locator.wait_for(state="detached")
        await self._get_org_name_input().locator.wait_for(state="detached")
        await self._get_cancel_button().locator.wait_for(state="detached")
        await self._get_create_button().locator.wait_for(state="detached")
