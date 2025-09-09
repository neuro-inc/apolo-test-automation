from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class CreateSecretPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the popup is considered loaded (key elements are visible).
        """
        self.log("Check if popup loaded")
        return (
            await self._get_create_new_secret_title().is_visible()
            and await self._get_secret_name_input().is_visible()
            and await self._get_secret_value_input().is_visible()
            and await self._get_create_secret_btn().is_visible()
        )

    def _get_create_new_secret_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Create New Secret")

    def _get_secret_name_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="key"]')

    async def enter_secret_name(self, secret_name: str) -> None:
        self.log(f"Enter secret name {secret_name}")
        await self._get_secret_name_input().fill(secret_name)

    def _get_secret_value_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[name="value"]')

    async def enter_secret_value(self, secret_value: str) -> None:
        self.log(f"Enter secret value {secret_value}")
        await self._get_secret_value_input().fill(secret_value)

    def _get_create_secret_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Create secret")

    async def click_create_secret_button(self) -> None:
        self.log("Click Create secret button")
        await self._get_create_secret_btn().click()

    async def wait_to_disappear(self) -> None:
        """
        Waits until key elements of the popup disappear (popup is closed).
        """
        self.log("Wait for Create New Secret popup to disappear")

        await self._get_create_new_secret_title().locator.wait_for(state="detached")
        await self._get_secret_name_input().locator.wait_for(state="detached")
        await self._get_secret_value_input().locator.wait_for(state="detached")
        await self._get_create_secret_btn().locator.wait_for(state="detached")
