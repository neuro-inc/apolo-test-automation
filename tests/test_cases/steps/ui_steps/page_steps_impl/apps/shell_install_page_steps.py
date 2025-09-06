from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class ShellInstallPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Shell install page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.shell_install_page.is_loaded(), (
            "Shell Install page should be displayed!"
        )

    @async_step("Click Resource preset button")
    async def ui_click_resource_preset_btn(self) -> None:
        await self._pm.shell_install_page.click_resource_preset_btn()

    @async_step("click Http Authentication checkbox")
    async def ui_click_http_auth_checkbox(self) -> None:
        await self._pm.shell_install_page.click_http_auth_checkbox()

    @async_step("Enter Shell instance display name")
    async def ui_enter_shell_app_name(self, app_name: str) -> None:
        await self._pm.shell_install_page.enter_app_name(app_name=app_name)

    @async_step("Click Install button")
    async def ui_click_install_btn(self) -> None:
        await self._pm.shell_install_page.click_install_btn()

    @async_step("Verify Export config button disabled")
    async def verify_ui_export_config_btn_disabled(self) -> None:
        assert not await self._pm.shell_install_page.is_export_config_btn_enabled(), (
            "Export Config button should be disabled!"
        )

    @async_step("Verify Export config button enabled")
    async def verify_ui_export_config_btn_enabled(self) -> None:
        assert await self._pm.shell_install_page.is_export_config_btn_enabled(), (
            "Export Config button should be enabled!"
        )

    @async_step("Click Export config button")
    async def ui_click_export_config_btn(self) -> None:
        await self._pm.shell_install_page.click_export_config_btn()

    @async_step("Verify Import config button enabled")
    async def verify_ui_import_config_btn_enabled(self) -> None:
        assert await self._pm.shell_install_page.is_import_config_btn_enabled(), (
            "Import Config button should be enabled!"
        )

    @async_step("Click Import config button")
    async def ui_click_import_config_btn(self) -> None:
        await self._pm.shell_install_page.click_import_config_btn()
