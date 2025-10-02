import pathlib
from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class ImportAppConfigPopup(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if popup loaded")
        return (
            await self._get_import_config_heading().expect_to_be_loaded()
            and await self._get_apply_config_btn().expect_to_be_loaded()
        )

    def _get_import_config_heading(self) -> BaseElement:
        return BaseElement(
            self.page,
            by_role="heading",
            name="Import App Configuration",
        )

    async def import_config_file(self, config_file: str) -> None:
        config_path = pathlib.Path(config_file).resolve()
        file_bytes = config_path.read_bytes()

        # Convert file bytes to a Latin-1 string so it can be passed into JS safely
        file_content = file_bytes.decode("latin-1")

        await self.page.evaluate(
            """({ selector, fileName, fileType, fileContent }) => {
                const dt = new DataTransfer();
                const blob = new Blob([fileContent], { type: fileType });
                const file = new File([blob], fileName, { type: fileType });
                dt.items.add(file);

                const dropEvent = new DragEvent("drop", {
                    dataTransfer: dt,
                    bubbles: true,
                    cancelable: true,
                });

                document.querySelector(selector).dispatchEvent(dropEvent);
            }""",
            {
                "selector": "[role='presentation']",
                "fileName": config_path.name,
                "fileType": "application/x-yaml",
                "fileContent": file_content,
            },
        )
        await self.page.wait_for_timeout(1000)

    def _get_apply_config_btn(self) -> BaseElement:
        return BaseElement(
            self.page,
            by_role="button",
            name="Apply config",
        )

    async def is_apply_config_btn_enabled(self) -> bool:
        self.log("Check if Apply config button is enabled")
        return await self._get_apply_config_btn().is_enabled()

    async def click_apply_config_btn(self) -> None:
        self.log("Click Apply config button")
        await self._get_apply_config_btn().click()
        await self.page.wait_for_timeout(1000)

    async def wait_to_disappear(self) -> None:
        """
        Waits until key elements of the page disappear (popup is closed).
        """
        self.log("Wait for Import App Configuration popup to disappear")

        await self._get_import_config_heading().locator.wait_for(state="detached")
        await self._get_apply_config_btn().locator.wait_for(state="detached")
