from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class ChooseSecretPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Choose New Secret popup displayed")
    async def verify_ui_popup_displayed(self) -> None:
        assert await self._pm.choose_secret_popup.is_loaded(), (
            "Create New Secret popup should be displayed!"
        )

    @async_step("Select Secret")
    async def ui_select_secret(self, secret_name: str) -> None:
        await self._pm.choose_secret_popup.select_secret(secret_name=secret_name)

    @async_step("Click Create New Secret checkbox")
    async def ui_click_create_new_secret_checkbox(self) -> None:
        await self._pm.choose_secret_popup.click_new_secret_checkbox()

    @async_step("Click Apply button")
    async def ui_click_apply_button(self) -> None:
        await self._pm.choose_secret_popup.click_apply_btn()

    @async_step("Wait for Choose New Secret popup to disappear")
    async def ui_wait_to_disappear(self) -> None:
        await self._pm.choose_secret_popup.wait_to_disappear()
