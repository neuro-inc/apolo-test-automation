from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class DeepSeekInstallPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Deep Seek install page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.deep_seek_install_page.is_loaded(), (
            "DeepSeek Install page should be displayed!"
        )

    @async_step("Click Choose Secret button")
    async def ui_click_choose_secret_btn(self) -> None:
        await self._pm.deep_seek_install_page.click_choose_secret_btn()

    @async_step("Select Hugging Face model")
    async def ui_select_hugging_face_model(self, model_name: str) -> None:
        await self._pm.deep_seek_install_page.select_model(model_name=model_name)

    @async_step("Enter Deep Seek instance display name")
    async def ui_enter_display_name(self, app_name: str) -> None:
        await self._pm.deep_seek_install_page.enter_app_name(app_name=app_name)

    @async_step("Click Install button")
    async def ui_click_install_btn(self) -> None:
        await self._pm.deep_seek_install_page.click_install_btn()

    @async_step("Verify Export config button disabled")
    async def verify_ui_export_config_btn_disabled(self) -> None:
        assert (
            not await self._pm.deep_seek_install_page.is_export_config_btn_enabled()
        ), "Export Config button should be disabled!"

    @async_step("Verify Export config button enabled")
    async def verify_ui_export_config_btn_enabled(self) -> None:
        assert await self._pm.deep_seek_install_page.is_export_config_btn_enabled(), (
            "Export Config button should be enabled!"
        )

    @async_step("Click Export config button")
    async def ui_click_export_config_btn(self) -> None:
        await self._pm.deep_seek_install_page.click_export_config_btn()

    @async_step("Verify Import config button enabled")
    async def verify_ui_import_config_btn_enabled(self) -> None:
        assert await self._pm.deep_seek_install_page.is_import_config_btn_enabled(), (
            "Import Config button should be enabled!"
        )

    @async_step("Click Import config button")
    async def ui_click_import_config_btn(self) -> None:
        await self._pm.deep_seek_install_page.click_import_config_btn()
