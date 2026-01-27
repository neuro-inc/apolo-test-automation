from typing import Any
from playwright.async_api import Page, Locator
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class DeepSeekDetailsPage(BasePage):
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
            "p.text-footnote.capitalize.text-neural-04:has-text('Owner') "
            "+ p.text-rebecca"
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
        return BaseElement(self.page, 'h6:has-text("Project") + p.w-fit')

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

    def _get_output_container(self) -> BaseElement:
        return BaseElement(
            self.page,
            selector="div.mt-4.flex.flex-col.gap-4",
            has=self.page.get_by_role("heading", name="output"),
        )

    async def is_output_container_displayed(self) -> bool:
        container_area = self.page.locator(
            "div.min-h-0.min-w-0.overflow-auto.bg-gray-100"
        )
        container = self._get_output_container()

        try:
            for _ in range(3):  # limit to avoid infinite loop
                if await container.is_element_in_viewport():
                    return True

                await container.scroll_half_window(container_locator=container_area)
                await self.page.wait_for_timeout(300)

            self.log("Output section not found after scrolling")
            return False

        except Exception as e:
            self.log(f"Output section not found: {e}")
            return False

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

    async def parse_output_sections(self) -> list[dict[str, str]]:
        """
        Parse the 'Output' section and return structured API dictionaries.
        Rules:
          - <button disabled> → key/value pair
          - <button not disabled> → nested dict (collapsible)
          - Only sections ending with 'API' are kept.
          - 'Service APIs' wrapper sections are unwrapped: nested API
            subsections are extracted individually.
          - Duplicates between parent and nested dicts are safely removed.
        """
        results: list[dict[str, str]] = []

        # Locate the 'Output' section container
        output_section = self.page.locator(
            "xpath=//h3[translate(normalize-space(), 'OUTPUT', 'output')='output']/following-sibling::div"
        )

        # Top-level API sections (font-bold buttons)
        api_buttons = output_section.locator(
            "xpath=.//button[contains(@class,'font-bold') and .//h4]"
        )
        total = await api_buttons.count()

        for i in range(total):
            api_button = api_buttons.nth(i)
            title_el = api_button.locator("xpath=.//h4")
            title = (await title_el.inner_text()).strip()

            # Skip non-API sections early
            if not (title.lower().endswith("api") or title.lower() == "service apis"):
                continue

            # Handle 'Service APIs' wrapper: extract nested API subsections
            if title.lower() == "service apis":
                container = api_button.locator(
                    "xpath=following-sibling::div[contains(@class,'overflow-hidden')"
                    " or contains(@class,'contents')]"
                )
                nested_api_buttons = container.locator("xpath=.//button[h4]")
                nested_count = await nested_api_buttons.count()
                for j in range(nested_count):
                    nested_btn = nested_api_buttons.nth(j)
                    nested_title = (
                        await nested_btn.locator("xpath=.//h4").inner_text()
                    ).strip()
                    if not nested_title.lower().endswith("api"):
                        continue
                    nested_data = await self._parse_api_section(nested_btn)
                    nested_data["title"] = nested_title
                    results.append(nested_data)
                continue

            # Parse this API section recursively
            section_data = await self._parse_api_section(api_button)
            section_data["title"] = title

            # --- Deduplicate safely ---
            keys_to_delete: list[str] = []
            for k, v in list(section_data.items()):
                if isinstance(v, dict):
                    for nested_key in v.keys():
                        if nested_key in section_data and nested_key != k:
                            keys_to_delete.append(nested_key)

            # Delete outside the iteration
            for k in keys_to_delete:
                del section_data[k]

            results.append(section_data)

        return results

    async def _parse_api_section(self, button: Locator) -> dict[str, str]:
        """
        Recursively parses collapsible API sections.
        Disabled <button> → key/value pair
        Enabled <button>  → nested dict (subsection)
        Avoids duplicate fields across nested levels.
        """
        data: dict[str, str] = {}

        # The container directly following this button
        container = button.locator(
            "xpath=following-sibling::div[contains(@class,'overflow-hidden') or contains(@class,'contents')]"
        )

        # Get all nested buttons with <h4>
        sub_buttons = container.locator("xpath=.//button[h4]")
        total = await sub_buttons.count()

        for i in range(total):
            sub_button = sub_buttons.nth(i)
            key_el = sub_button.locator("xpath=.//h4")
            key = (await key_el.inner_text()).strip()
            is_disabled = await sub_button.get_attribute("disabled")

            if is_disabled is not None:
                # --- Simple key/value pair ---
                value_span = sub_button.locator(
                    "xpath=following-sibling::div[contains(@class,'overflow-hidden') or contains(@class,'contents')]"
                    "//span[contains(@class,'text-lime-800') or "
                    "contains(@class,'text-cyan-800') or "
                    "contains(@class,'text-neural-06')]"
                )
                if await value_span.count() > 0:
                    value = (await value_span.first.inner_text()).strip()
                    data[key] = value
            else:
                # --- Nested collapsible dict ---
                nested_dict = await self._parse_api_section(sub_button)
                data[key] = nested_dict  # type: ignore[assignment]

                # Dedup nested keys safely
                keys_to_delete = [
                    nk for nk in nested_dict.keys() if nk in data and nk != key
                ]
                for k_del in keys_to_delete:
                    del data[k_del]

        return data
