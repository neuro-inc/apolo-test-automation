from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class NoProjectPopup(BasePage):
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
            await self._get_no_proj_text_field().expect_to_be_loaded()
            and await self._create_proj_button().expect_to_be_loaded()
        )

    def _get_no_proj_text_field(self) -> BaseElement:
        return BaseElement(
            self.page, "p.text-h6", has_text="You don't have any projects"
        )

    def _create_proj_text_field(self, org_name: str) -> BaseElement:
        return BaseElement(
            self.page,
            "p.text-center",
            has_text=f"Create a new project for {org_name} organization",
        )

    def _create_proj_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Create new project")

    async def click_create_proj_button(self) -> None:
        self.log("Click create project button")
        await self._create_proj_button().click()
