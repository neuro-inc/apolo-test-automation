from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class SecretsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_secrets_title().is_visible()
            and await self._get_create_new_secret_btn().is_visible()
        )

    def _get_secrets_title(self) -> BaseElement:
        return BaseElement(self.page, "h4.text-h4", has_text="Secrets")

    def _get_create_new_secret_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Create new secret")

    def _get_search_secret_input(self) -> BaseElement:
        return BaseElement(self.page, 'input[placeholder=" "]')

    def _get_no_secrets_message(self) -> BaseElement:
        return BaseElement(self.page, "p", has_text="No secrets found")

    def _get_secret_row(self, secret_name: str) -> BaseElement:
        return BaseElement(self.page, "tr", has_text=secret_name)

    def _get_secret_delete_btn(self, secret_name: str) -> BaseElement:
        return BaseElement(self.page, f'tr:has-text("{secret_name}") button')

    async def is_no_secrets_message_displayed(self) -> bool:
        self.log("Check if No secrets message displayed")
        return await self._get_no_secrets_message().is_visible()

    async def click_create_new_secret_btn(self) -> None:
        self.log("Click Create new secret button")
        await self._get_create_new_secret_btn().click()

    async def enter_search_secret_name(self, secret_name: str) -> None:
        self.log("Enter secret name into Search input")
        await self._get_search_secret_input().fill(secret_name)

    async def is_secret_row_displayed(self, secret_name: str) -> bool:
        self.log(f"Check if Secret {secret_name} row displayed")
        return await self._get_secret_row(secret_name).is_visible()

    async def click_delete_secret_btn(self, secret_name: str) -> None:
        self.log(f"Click Delete Secret {secret_name} button")
        await self._get_secret_delete_btn(secret_name).click()
