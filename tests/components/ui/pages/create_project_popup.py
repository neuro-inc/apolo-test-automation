from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class CreateProjectPopup(BasePage):
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

        return (
            await self._get_create_proj_title().expect_to_be_loaded()
            and await self._get_create_proj_text_field(org_name).expect_to_be_loaded()
            and await self._get_proj_name_input().expect_to_be_loaded()
            and await self._get_is_proj_default_checkbox().expect_to_be_loaded()
            and await self._get_default_role_dropdown().expect_to_be_loaded()
            and await self._get_cancel_button().expect_to_be_loaded()
            and await self._get_create_button().expect_to_be_loaded()
        )

    def _get_create_proj_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Create Project")

    def _get_create_proj_text_field(self, org_name: str) -> BaseElement:
        return BaseElement(
            self.page, "p", has_text=f"Create new project for {org_name} organization"
        )

    def _get_proj_name_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="name"]')

    async def enter_proj_name(self, proj_name: str) -> None:
        self.log(f"Enter new project name {proj_name}")
        await self._get_proj_name_input().fill(proj_name)

    def _get_is_proj_default_checkbox(self) -> BaseElement:
        return BaseElement(self.page, "label", has_text="Make project as default")

    async def click_proj_default_checkbox(self) -> None:
        self.log("Click project default checkbox")
        await self._get_is_proj_default_checkbox().click()

    def _get_default_role_dropdown(self) -> BaseElement:
        return BaseElement(self.page, 'select[name="defaultRole"]')

    async def select_default_role(self, role: str) -> None:
        roles = ("reader", "writer", "manager")
        if role.lower() not in roles:
            raise ValueError(f"Expected role '{role}' to be one of {roles}")
        self.log(f"Select default role {role}")
        await self._get_default_role_dropdown().select_option(role.lower())

    def _get_cancel_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Cancel")

    async def click_cancel_button(self) -> None:
        self.log("Click cancel button")
        await self._get_cancel_button().click()

    def _get_create_button(self) -> BaseElement:
        return BaseElement(self.page, 'button[type="submit"]', has_text="Create")

    async def click_create_button(self) -> None:
        self.log("Click create button")
        await self._get_create_button().click()
        await self.page.wait_for_timeout(300)
