from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class DeleteSecretPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the popup is considered loaded (key elements are visible).
        """
        self.log("Check if popup loaded")
        secret_name = kwargs.get("secret_name")
        if not isinstance(secret_name, str):
            raise ValueError(
                "Expected 'secret_name' to be a non-empty string in kwargs"
            )
        return (
            await self._get_delete_secret_title().is_visible()
            and await self._get_delete_secret_message(secret_name).is_visible()
            and await self._get_cancel_btn().is_visible()
            and await self._get_delete_btn().is_visible()
        )

    def _get_delete_secret_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Delete Secret")

    def _get_delete_secret_message(self, secret_name: str) -> BaseElement:
        return BaseElement(
            self.page,
            'p:has-text("Are you sure you want to delete")',
            has_text=secret_name,
        )

    def _get_cancel_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Cancel")

    async def click_cancel_btn(self) -> None:
        self.log("Click cancel button")
        await self._get_cancel_btn().click()

    def _get_delete_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Delete")

    async def click_delete_btn(self) -> None:
        self.log("Click Delete button")
        await self._get_delete_btn().click()

    async def wait_to_disappear(self, secret_name: str) -> None:
        """
        Waits until key elements of the popup disappear (popup is closed).
        """
        self.log("Wait for Delete Secret popup to disappear")

        await self._get_delete_secret_title().locator.wait_for(state="detached")
        await self._get_delete_secret_message(secret_name).locator.wait_for(
            state="detached"
        )
        await self._get_cancel_btn().locator.wait_for(state="detached")
        await self._get_delete_btn().locator.wait_for(state="detached")
