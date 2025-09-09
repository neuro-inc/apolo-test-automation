from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class ChooseSecretPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the popup is considered loaded (key elements are visible).
        """
        self.log("Check if popup loaded")
        return (
            await self._get_environment_secrets_title().is_visible()
            and await self._get_create_new_secret_checkbox().is_visible()
            and await self._get_apply_btn().is_visible()
        )

    def _get_environment_secrets_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Environment Secrets")

    def _get_secret_key_radio(self, secret_name: str) -> BaseElement:
        return BaseElement(
            self.page, f"label:has(input[name='secretKey'][value='{secret_name}'])"
        )

    async def select_secret(self, secret_name: str) -> None:
        self.log(f"Select {secret_name} secret")
        await self._get_secret_key_radio(secret_name).click()

    def _get_create_new_secret_checkbox(self) -> BaseElement:
        return BaseElement(self.page, by_label="Create new secret")

    async def click_new_secret_checkbox(self) -> None:
        self.log("Click Create new secret checkbox")
        await self._get_create_new_secret_checkbox().click()

    def _get_apply_btn(self) -> BaseElement:
        return BaseElement(self.page, by_role="button", name="Apply")

    async def click_apply_btn(self) -> None:
        self.log("Click Apply button")
        await self._get_apply_btn().click()

    async def wait_to_disappear(self) -> None:
        """
        Waits until key elements of the popup disappear (popup is closed).
        """
        self.log("Wait for Environment Secrets popup to disappear")

        await self._get_environment_secrets_title().locator.wait_for(state="detached")
        await self._get_create_new_secret_checkbox().locator.wait_for(state="detached")
        await self._get_apply_btn().locator.wait_for(state="detached")
