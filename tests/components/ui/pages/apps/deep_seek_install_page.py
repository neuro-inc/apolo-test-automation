from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class DeepSeekInstallPage(BasePage):
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
            and await self._get_hf_token_label().is_visible()
            and await self._get_choose_secret_btn().is_visible()
            and await self._get_autoscaling_checkbox().is_visible()
            and await self._get_metadata_label().is_visible()
            and await self._get_display_name_input().is_visible()
            and await self._get_install_btn().is_visible()
            and await self._get_export_config_btn().is_visible()
            and await self._get_import_config_btn().is_visible()
        )

    def _get_page_heading(self) -> BaseElement:
        return BaseElement(self.page, "h4", has_text="DeepSeek App")

    def _get_page_title(self) -> BaseElement:
        return BaseElement(self.page, "h3", has_text="DeepSeek")

    def _get_hf_token_label(self) -> BaseElement:
        return BaseElement(self.page, "p.text-h4", has_text="Hugging Face Token")

    def _get_choose_secret_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Choose secret")

    async def click_choose_secret_btn(self) -> None:
        self.log("Click Choose Secret button")
        await self._get_choose_secret_btn().click()

    def _get_autoscaling_checkbox(self) -> BaseElement:
        return BaseElement(self.page, by_label="Enable Autoscaling")

    async def click_autoscaling_checkbox(self) -> None:
        self.log("Click Autoscaling checkbox")
        await self._get_autoscaling_checkbox().click()

    def _get_model_dropdown(self) -> BaseElement:
        return BaseElement(self.page, "select[name='size']")

    async def select_model(self, model_name: str) -> None:
        self.log(f"Select {model_name} model")
        await self._get_model_dropdown().select_option(model_name)

    def _get_metadata_label(self) -> BaseElement:
        return BaseElement(self.page, "p", has_text="Metadata")

    def _get_display_name_input(self) -> BaseElement:
        return BaseElement(self.page, '[name="displayName"]')

    async def enter_app_name(self, app_name: str) -> None:
        self.log(f"Entering {app_name} app name")
        await self._get_display_name_input().fill(app_name)

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
