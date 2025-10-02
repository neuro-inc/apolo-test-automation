from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class ImportAppConfigPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify Import app config popup displayed")
    async def verify_ui_popup_displayed(self) -> None:
        assert await self._pm.import_app_config_popup.is_loaded(), (
            "Import app config popup should be displayed!"
        )

    @async_step("Import yaml config")
    async def ui_import_yaml_config(self, config_path: str) -> None:
        await self._pm.import_app_config_popup.import_config_file(
            config_file=config_path
        )

    @async_step("Click Apply config button")
    async def ui_click_apply_config_btn(self) -> None:
        await self._pm.import_app_config_popup.click_apply_config_btn()

    @async_step("Wait for Import app config popup disappear")
    async def ui_wait_to_disappear(self) -> None:
        await self._pm.import_app_config_popup.wait_to_disappear()
