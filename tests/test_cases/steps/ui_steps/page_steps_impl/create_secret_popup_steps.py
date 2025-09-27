from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class CreateSecretPopupSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Create New Secret popup displayed")
    async def verify_ui_popup_displayed(self) -> None:
        assert await self._pm.create_secret_popup.is_loaded(), (
            "Create New Secret popup should be displayed!"
        )

    @async_step("Enter Secret name")
    async def ui_enter_secret_name(self, secret_name: str) -> None:
        await self._pm.create_secret_popup.enter_secret_name(secret_name)

    @async_step("Enter Secret value")
    async def ui_enter_secret_value(self, secret_value: str) -> None:
        await self._pm.create_secret_popup.enter_secret_value(secret_value)

    @async_step("Click Create Secret button")
    async def ui_click_create_secret_btn(self) -> None:
        await self._pm.create_secret_popup.click_create_secret_button()

    @async_step("Wait for Create New Secret popup to disappear")
    async def ui_wait_to_disappear(self) -> None:
        await self._pm.create_secret_popup.wait_to_disappear()
