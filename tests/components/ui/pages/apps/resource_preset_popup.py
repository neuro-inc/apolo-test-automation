from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class ResourcePresetPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the popup is considered loaded (key elements are visible).
        """
        self.log("Check if popup loaded")
        return (
            await self._get_popup_header().is_visible()
            and await self._get_preset_row("cpu-large").is_visible()
            and await self._get_apply_button().is_visible()
        )

    def _get_popup_header(self) -> BaseElement:
        return BaseElement(self.page, "h2", has_text="Choose Resource Preset")

    def _get_preset_row(self, name: str) -> BaseElement:
        return BaseElement(self.page, f'tr:has(td span:has-text("{name}"))')

    async def click_cpu_large_preset(self) -> None:
        self.log("Click cpu-large preset")
        await self._get_preset_row("cpu-large").click()

    async def click_cpu_medium_preset(self) -> None:
        self.log("Click cpu-medium preset")
        await self._get_preset_row("cpu-medium").click()
        await self.page.wait_for_timeout(2000)

    def _get_apply_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Apply")

    async def click_apply_button(self) -> None:
        self.log("Click Apply button")
        await self._get_apply_button().click()

    async def wait_to_disappear(self) -> None:
        """
        Waits until key elements of the popup disappear (popup is closed).
        """
        self.log("Wait for Create New Secret popup to disappear")

        await self._get_popup_header().locator.wait_for(state="detached")
        await self._get_preset_row("cpu-large").locator.wait_for(state="detached")
        await self._get_apply_button().locator.wait_for(state="detached")
