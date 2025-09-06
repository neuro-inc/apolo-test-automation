from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class ResourcePresetPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify Resource Preset popup displayed")
    async def verify_ui_popup_displayed(self) -> None:
        assert await self._pm.resource_preset_popup.is_loaded(), (
            "Resource Preset popup should be displayed!"
        )

    @async_step("Select cpu-large preset")
    async def ui_select_cpu_large_preset(self) -> None:
        await self._pm.resource_preset_popup.click_cpu_large_preset()

    @async_step("Select cpu-medium preset")
    async def ui_select_cpu_medium_preset(self) -> None:
        await self._pm.resource_preset_popup.click_cpu_medium_preset()

    @async_step("Click Apply button")
    async def ui_click_apply_button(self) -> None:
        await self._pm.resource_preset_popup.click_apply_button()

    @async_step("Wait for Resource Preset popup disappear")
    async def ui_wait_to_disappear(self) -> None:
        await self._pm.resource_preset_popup.wait_to_disappear()
