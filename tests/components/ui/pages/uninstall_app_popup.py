import re
from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class UninstallAppPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def _get_popup_container(self) -> BaseElement:
        """Get the popup container that holds all popup elements."""
        return BaseElement(
            self.page,
            'div[role="dialog"]',
            has=self.page.locator("h2", has_text="Uninstall App"),
        )

    async def is_loaded(self, **kwargs: Any) -> bool:
        self.log("Check if popup loaded")
        try:
            await self._get_popup_container().locator.wait_for(
                state="visible", timeout=5000
            )
        except Exception:
            return False
        return (
            await self._get_uninstall_title().is_visible()
            and await self._get_cancel_btn().is_visible()
            and await self._get_uninstall_btn().is_visible()
        )

    def _get_uninstall_title(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Uninstall App")

    def _get_cancel_btn(self) -> BaseElement:
        """Get Cancel button scoped to popup container."""
        container = self._get_popup_container().locator
        return BaseElement(
            self.page, locator=container.locator("button", has_text="Cancel")
        )

    async def click_cancel_btn(self) -> None:
        self.log("Click cancel button")
        await self._get_cancel_btn().click()

    def _get_uninstall_btn(self) -> BaseElement:
        """Get Uninstall button scoped to popup container."""
        container = self._get_popup_container().locator
        return BaseElement(
            self.page,
            locator=container.locator("button", has_text=re.compile(r"^Uninstall$")),
        )

    async def click_uninstall_btn(self) -> None:
        self.log("Click Uninstall button")
        await self._get_uninstall_btn().click()

    async def wait_to_disappear(self) -> None:
        self.log("Wait for Uninstall popup to disappear")
        await self._get_popup_container().locator.wait_for(state="detached")
