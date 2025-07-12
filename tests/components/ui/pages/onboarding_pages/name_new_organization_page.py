from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class NameNewOrganizationPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._name_your_organization_title = BaseElement(
            self.page, "h5", has_text="Name your Organization:"
        )
        self._organization_name_input = BaseElement(self.page, 'input[name="name"]')
        self._next_button = BaseElement(
            self.page, 'button[type="submit"]', has_text="Next"
        )

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        await self.page.wait_for_timeout(1000)
        return (
            await self._name_your_organization_title.expect_to_be_loaded()
            and await self._organization_name_input.expect_to_be_loaded()
            and await self._next_button.expect_to_be_loaded()
        )

    async def enter_organization_name(self, value: str) -> None:
        self.log(f"Enter {value} organization name")
        await self._organization_name_input.fill(value)

    async def click_next_button(self) -> None:
        self.log("Click next button")
        btn = self._next_button
        await self.page.wait_for_timeout(500)
        await btn.hover()
        await btn.click()
        await self.page.wait_for_timeout(1000)
