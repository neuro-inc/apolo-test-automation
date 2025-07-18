from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class FilesPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

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

    @async_step("Verify Folder is displayed")
    async def verify_ui_folder_displayed(self, name: str) -> None:
        assert await self._pm.files_page.is_folder_btn_displayed(name=name), (
            f"Folder {name} button should be displayed!"
        )
