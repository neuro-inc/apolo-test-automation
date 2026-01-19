from __future__ import annotations

from typing import Any

from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager
from tests.utils.test_data_management.test_data import DataManager


class DeepSeekDetailsPageSteps:
    def __init__(self, page_manager: PageManager, data_manager: DataManager) -> None:
        self._pm = page_manager
        self._data_manager = data_manager
        self.required_APIs = [
            ("OpenAI Compatible Chat API", "http"),
            ("OpenAI Compatible Chat API", "https"),
            ("OpenAI Compatible Embeddings API", "http"),
            ("OpenAI Compatible Embeddings API", "https"),
        ]

    @async_step("Verify that DeepSeek app Details page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.deep_seek_details_page.is_loaded(), (
            "DeepSeek app Details page should be displayed!"
        )

    @async_step("Verify that app status is valid")
    async def verify_ui_app_status_is_valid(self, expected_status: str) -> None:
        actual_status = await self._pm.deep_seek_details_page.get_app_status()
        assert actual_status.lower() == expected_status.lower(), (
            f"Expected {expected_status} but got {actual_status}!"
        )

    @async_step("Get DeepSeek app UUID")
    async def ui_get_deep_seek_app_uuid(self) -> str:
        return await self._pm.deep_seek_details_page.get_uuid_value()

    @async_step("Validate DeepSeek app details info")
    async def verify_ui_app_details_info(
        self, owner: str, app_id: str, app_name: str, proj_name: str, org_name: str
    ) -> None:
        (
            result,
            error_message,
        ) = await self._pm.deep_seek_details_page.verify_app_details_info(
            owner=owner,
            app_id=app_id,
            app_name=app_name,
            proj_name=proj_name,
            org_name=org_name,
        )
        assert result, error_message

    @async_step("Verify App output section displayed")
    async def verify_ui_app_output_displayed(self) -> None:
        assert await self._pm.deep_seek_details_page.is_output_container_displayed(), (
            "Output container should be displayed!"
        )

    @async_step("Verify App output contains required endpoints")
    async def verify_ui_app_output_apis(self) -> None:
        api_sections = await self._pm.deep_seek_details_page.parse_output_sections()
        for name, protocol in self.required_APIs:
            assert self._has_object_with_title_and_protocol(
                api_sections, name, protocol
            ), f"No {name} API with {protocol} protocol!"

    @async_step("Verify App endpoints sections contains valid data format")
    async def verify_ui_app_output_apis_data_format(self) -> None:
        api_sections = await self._pm.deep_seek_details_page.parse_output_sections()
        await self._data_manager.app_data.load_output_ui_schema("deep_seek")
        result, error_message = self._data_manager.app_data.validate_api_section_schema(
            api_sections
        )
        assert result, error_message

    @async_step("Click Uninstall button")
    async def ui_click_uninstall_btn(self) -> None:
        await self._pm.deep_seek_details_page.click_uninstall_btn()

    @async_step("Click Uninstall button and confirm")
    async def ui_click_uninstall_and_confirm(self) -> None:
        await self._pm.deep_seek_details_page.click_uninstall_btn()
        assert await self._pm.uninstall_app_popup.is_loaded(), (
            "Uninstall confirmation popup should appear!"
        )
        await self._pm.uninstall_app_popup.click_uninstall_btn()
        await self._pm.uninstall_app_popup.wait_to_disappear()

    def _has_object_with_title_and_protocol(
        self, data: list[dict[str, Any]], title: str, protocol: str
    ) -> bool:
        """
        Check if there is at least one object in the list
        with the given title and protocol.
        """
        return any(
            obj.get("title") == title and obj.get("Protocol") == protocol
            for obj in data
        )
