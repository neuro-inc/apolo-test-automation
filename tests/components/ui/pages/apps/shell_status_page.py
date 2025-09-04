from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class ShellDetailsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return (
            await self._get_app_status_field().is_visible()
            and await self._get_id_field().is_visible()
            and await self._get_display_name_field().is_visible()
            and await self._get_proj_field().is_visible()
            and await self._get_org_field().is_visible()
            and await self._get_refresh_button().is_visible()
            and await self._get_uninstall_btn().is_visible()
            and await self._get_input_section_header().is_visible()
            and await self._get_input_download_btn().is_visible()
        )

    def _get_app_status_field(self) -> BaseElement:
        return BaseElement(
            self.page, 'div[slot="trigger"]:has(p.text-caption-3) p.capitalize'
        )

    async def get_app_status(self) -> str:
        element = self._get_app_status_field()
        return (await element.text_content()).strip()

    def _get_refresh_button(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Refresh")

    async def click_refresh_button(self) -> None:
        await self._get_refresh_button().click()

    def _get_uninstall_btn(self) -> BaseElement:
        return BaseElement(self.page, "button", has_text="Uninstall")

    async def click_uninstall_btn(self) -> None:
        await self._get_uninstall_btn().click()

    def _get_owner_field(self) -> BaseElement:
        locator = (
            "div.flex.flex-col.gap-1.5"
            ":has(p.text-footnote.capitalize.text-neural-04:has-text('Owner')) "
            "p.text-rebecca"
        )
        return BaseElement(self.page, locator)

    async def get_owner_value(self) -> str:
        return await self._get_owner_field().text_content()

    def _get_id_field(self) -> BaseElement:
        # 2 means "third ID field"
        return BaseElement(
            self.page, 'div:has(h6:text("ID")) p[slot="trigger"] >> nth=0'
        )

    async def get_uuid_value(self) -> str:
        element = self._get_id_field()
        raw_text = await element.text_content()
        return raw_text.strip().split()[0]

    def _get_display_name_field(self) -> BaseElement:
        return BaseElement(
            self.page, 'div:has(h6:text("Display Name")) p[slot="trigger"] >> nth=2'
        )

    async def get_display_name_value(self) -> str:
        element = self._get_display_name_field()
        raw_text = await element.text_content()
        return raw_text.strip().split()[0]

    def _get_proj_field(self) -> BaseElement:
        return BaseElement(self.page, 'div:has(h6:text("Project")) p.w-fit >> nth=1')

    async def get_proj_name(self) -> str:
        element = self._get_proj_field()
        return (await element.text_content()).strip()

    def _get_org_field(self) -> BaseElement:
        return BaseElement(
            self.page, 'div:has(h6:text("Organization")) p.w-fit >> nth=5'
        )

    async def get_org_name(self) -> str:
        element = self._get_org_field()
        return (await element.text_content()).strip()

    def _get_input_section_header(self) -> BaseElement:
        return BaseElement(self.page, "h3.text-h5.capitalize", has_text="input")

    def _get_input_download_btn(self) -> BaseElement:
        return BaseElement(
            self.page, 'h3:has-text("input") button[aria-label="Download parameters"]'
        )

    def _get_http_auth_field(self) -> BaseElement:
        locator = (
            "div.overflow-auto:has(h4:has-text('HTTP Authentication')) "
            "p span.text-pink-800"
        )
        return BaseElement(self.page, locator)

    async def get_http_auth_value(self) -> bool:
        raw_value = await self._get_http_auth_field().text_content()
        return raw_value.strip().lower() == "true"

    def _get_resource_preset_field(self) -> BaseElement:
        locator = (
            "div.overflow-auto:has(h4:has-text('Resource Preset')) p span.text-lime-800"
        )
        return BaseElement(self.page, locator)

    async def get_resource_preset_value(self) -> str:
        return (await self._get_resource_preset_field().text_content()).strip()

    async def verify_app_details_info(
        self, owner: str, app_id: str, app_name: str, proj_name: str, org_name: str
    ) -> tuple[bool, str]:
        mismatches: list[str] = []

        # collect actual values
        actual_owner = (await self.get_owner_value()).strip()
        actual_app_id = (await self.get_uuid_value()).strip()
        actual_app_name = (await self.get_display_name_value()).strip()
        actual_proj_name = (await self.get_proj_name()).strip()
        actual_org_name = (await self.get_org_name()).strip()

        # compare one by one
        if actual_owner != owner:
            mismatches.append(f"Owner expected '{owner}', got '{actual_owner}'")
        if actual_app_id != app_id:
            mismatches.append(f"ID expected '{app_id}', got '{actual_app_id}'")
        if actual_app_name != app_name:
            mismatches.append(
                f"Display Name expected '{app_name}', got '{actual_app_name}'"
            )
        if actual_proj_name != proj_name:
            mismatches.append(
                f"Project expected '{proj_name}', got '{actual_proj_name}'"
            )
        if actual_org_name != org_name:
            mismatches.append(
                f"Organization expected '{org_name}', got '{actual_org_name}'"
            )

        if mismatches:
            return False, "; ".join(mismatches)
        return True, ""
