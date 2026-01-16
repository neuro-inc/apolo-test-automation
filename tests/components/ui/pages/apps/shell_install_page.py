from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class ShellInstallPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_page_heading().is_visible()
            and await self._get_page_title().is_visible()
            and await self._get_resource_preset_label().is_visible()
            and await self._get_resource_preset_btn().is_visible()
            and await self._get_networking_settings_label().is_visible()
            and await self._get_auth_dropdown().is_visible()
            and await self._get_metadata_label().is_visible()
            and await self._get_display_name_input().is_visible()
            and await self._get_install_btn().is_visible()
            and await self._get_export_config_btn().is_visible()
            and await self._get_import_config_btn().is_visible()
        )

    def _get_page_heading(self) -> BaseElement:
        return BaseElement(self.page, "h4", has_text="Shell App")

    def _get_page_title(self) -> BaseElement:
        return BaseElement(self.page, "h3", has_text="Shell")

    def _get_resource_preset_label(self) -> BaseElement:
        return BaseElement(self.page, "p.text-h4", has_text="Resource Preset")

    def _get_resource_preset_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Resource Preset")

    async def click_resource_preset_btn(self) -> None:
        self.log("Click resource Preset button")
        await self._get_resource_preset_btn().click()

    async def get_resource_preset_value(self) -> str:
        btn = self._get_resource_preset_btn()
        text = await btn.text_content()
        return text.splitlines()[-1].strip()

    def _get_networking_settings_label(self) -> BaseElement:
        return BaseElement(self.page, "p", has_text="Networking Settings")

    def _get_auth_dropdown(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector='select:has(option:text("Apolo Platform Authentication"))',
        )

    async def select_auth_type(self, value: str) -> None:
        self.log(f"Select Auth type: {value}")
        await self._get_auth_dropdown().select_option(value)

    async def get_auth_type_value(self) -> str:
        dropdown = self._get_auth_dropdown()
        selected_option = dropdown.locator.locator("option:checked")
        return (await selected_option.text_content() or "").strip()

    def _get_metadata_label(self) -> BaseElement:
        return BaseElement(self.page, "p", has_text="Metadata")

    def _get_display_name_input(self) -> BaseElement:
        return BaseElement(self.page, '[name="displayName"]')

    async def enter_app_name(self, app_name: str) -> None:
        self.log(f"Entering {app_name} app name")
        await self._get_display_name_input().fill(app_name)

    async def get_display_name_value(self) -> str:
        element = self._get_display_name_input()
        return await element.locator.input_value()

    def _get_install_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Install")

    async def click_install_btn(self) -> None:
        self.log("Click Install button")
        await self._get_install_btn().click()
        spinner_selector = "button:has-text('Install') div.chase-spinner"
        await self.wait_for_spinner(spinner_selector=spinner_selector, timeout=30000)

    def _get_export_config_btn(self) -> BaseElement:
        return BaseElement(self.page, by_role="button", name="Download parameters")

    async def is_export_config_btn_enabled(self) -> bool:
        return await self._get_export_config_btn().is_enabled()

    async def click_export_config_btn(self) -> None:
        self.log("Click Export config button")
        await self._get_export_config_btn().click()

    def _get_import_config_btn(self) -> BaseElement:
        return BaseElement(self.page, by_role="button", name="Import App Configuration")

    async def is_import_config_btn_enabled(self) -> bool:
        return await self._get_import_config_btn().is_enabled()

    async def click_import_config_btn(self) -> None:
        self.log("Click Import config button")
        await self._get_import_config_btn().click()

    def _get_version_text(self) -> BaseElement:
        return BaseElement(self.page, "p.text-neural-04", has_text="Version:")

    async def get_template_version(self) -> str:
        """Get template version from UI (e.g., 'v26.1.2')"""
        self.log("Get template version from UI")
        text = await self._get_version_text().locator.inner_text()
        # Parse "Version: v26.1.2" -> "v26.1.2"
        return text.replace("Version:", "").strip()
