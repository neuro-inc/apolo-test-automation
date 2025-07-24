from urllib.parse import urlparse, unquote

from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager
from tests.utils.test_data_management.test_data import DataManager


class FilesPageSteps:
    def __init__(self, page_manager: PageManager, data_manager: DataManager) -> None:
        self._pm = page_manager
        self._data_manager = data_manager

    @async_step("Verify that Files page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.files_page.is_loaded(), "Files page should be displayed!"

    @async_step("Verify Add folder button is enabled")
    async def verify_ui_add_folder_btn_enabled(self) -> None:
        assert await self._pm.files_page.is_add_folder_btn_enabled(), (
            "Add folder button should be enabled!"
        )

    @async_step("Click Add Folder button")
    async def ui_click_add_folder_btn(self) -> None:
        await self._pm.files_page.click_add_folder_btn()

    @async_step("Verify Add folder button is disabled")
    async def verify_ui_add_folder_btn_disabled(self) -> None:
        assert not await self._pm.files_page.is_add_folder_btn_enabled(), (
            "Add folder button should be disabled!"
        )

    @async_step("Verify Upload button is enabled")
    async def verify_ui_upload_btn_enabled(self) -> None:
        assert await self._pm.files_page.is_upload_btn_enabled(), (
            "Upload button should be enabled!"
        )

    @async_step("Verify Upload button is disabled")
    async def verify_ui_upload_btn_disabled(self) -> None:
        assert not await self._pm.files_page.is_upload_btn_enabled(), (
            "Upload button should be disabled!"
        )

    @async_step("Verify Folder up button is displayed")
    async def verify_ui_folder_up_btn_displayed(self) -> None:
        assert await self._pm.files_page.is_folder_up_btn_displayed(), (
            "Folder up button should be displayed!"
        )

    @async_step("Verify File button is displayed")
    async def verify_ui_file_displayed(self, name: str) -> None:
        assert await self._pm.files_page.is_file_btn_displayed(name=name), (
            f"File {name} button should be displayed!"
        )

    @async_step("Verify File button is not displayed")
    async def verify_ui_file_not_displayed(self, name: str) -> None:
        assert not await self._pm.files_page.is_file_btn_displayed(name=name), (
            f"File {name} button should not be displayed!"
        )

    @async_step("Click File button")
    async def ui_click_file_btn(self, name: str) -> None:
        await self._pm.files_page.click_file_btn(name=name)

    @async_step("Double click File button")
    async def ui_double_click_file_btn(self, name: str) -> None:
        await self._pm.files_page.double_click_file_btn(name=name)

    @async_step("Verify File info section displayed")
    async def verify_ui_file_info_section_displayed(self, name: str, path: str) -> None:
        assert await self._pm.files_page.is_file_info_section_displayed(
            name=name, path=path
        ), f"File info section for {name} should be displayed!"

    @async_step("Verify File action bar displayed")
    async def verify_ui_file_action_bar_displayed(self, name: str) -> None:
        assert await self._pm.files_page.is_file_action_bar_displayed(), (
            f"File action bar for {name} should be displayed!"
        )

    @async_step("Verify Files page URL path is valid")
    async def verify_ui_file_url_path_is_valid(self, expected_path: str) -> None:
        """Verify that the current Files page URL path matches the expected value."""
        url = await self._pm.files_page.current_url
        actual_path = unquote(urlparse(url).path.lstrip("/"))

        assert actual_path == expected_path, (
            f"URL path mismatch:\n"
            f"- Expected: {expected_path}\n"
            f"- Actual:   {actual_path}"
        )

    @async_step("Click Rename File button")
    async def ui_click_rename_file_btn(self) -> None:
        await self._pm.files_page.click_file_action_bar_rename_btn()

    @async_step("Click Delete File button")
    async def ui_click_delete_file_btn(self) -> None:
        await self._pm.files_page.click_file_action_bar_delete_btn()

    @async_step("Generate bin file")
    async def generate_bin_file(self) -> tuple[str, str]:
        return self._data_manager.generate_dummy_bin_file()

    @async_step("Generate txt file")
    async def generate_txt_file(self) -> tuple[str, str]:
        return self._data_manager.generate_dummy_txt_file()

    @async_step("Upload file")
    async def ui_upload_file(self, file_path: str) -> None:
        async with self._pm.files_page.page.expect_file_chooser() as fc_info:
            await self._pm.files_page.click_upload_btn()
        file_chooser = await fc_info.value
        await file_chooser.set_files(file_path)
        await self._pm.main_page.page.wait_for_timeout(500)
