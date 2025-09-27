from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class SecretsPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Secrets page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.secrets_page.is_loaded(), (
            "Secrets page should be displayed!"
        )

    @async_step("Verify that Secrets page is not displayed")
    async def verify_ui_page_not_displayed(self) -> None:
        assert not await self._pm.secrets_page.is_loaded(), (
            "Secrets page should not be displayed!"
        )

    @async_step("Verify that no secrets message displayed")
    async def verify_ui_no_secrets_message_displayed(self) -> None:
        assert await self._pm.secrets_page.is_no_secrets_message_displayed(), (
            "No secrets message should be displayed!"
        )

    @async_step("Verify that no secrets message is not displayed")
    async def verify_ui_no_secrets_message_not_displayed(self) -> None:
        assert not await self._pm.secrets_page.is_no_secrets_message_displayed(), (
            "No secrets message should not be displayed!"
        )

    @async_step("Click Create New Secret button")
    async def ui_click_create_new_secret_btn(self) -> None:
        await self._pm.secrets_page.click_create_new_secret_btn()

    @async_step("Enter Secret name into Search input")
    async def ui_enter_secret_name_into_search_input(self, secret_name: str) -> None:
        await self._pm.secrets_page.enter_search_secret_name(secret_name)

    @async_step("Verify Secret row displayed")
    async def verify_ui_secret_row_displayed(self, secret_name: str) -> None:
        assert await self._pm.secrets_page.is_secret_row_displayed(secret_name), (
            f"Secret {secret_name} row should be displayed!"
        )

    @async_step("Verify Secret row not displayed")
    async def verify_ui_secret_row_not_displayed(self, secret_name: str) -> None:
        assert not await self._pm.secrets_page.is_secret_row_displayed(secret_name), (
            f"Secret {secret_name} row should not be displayed!"
        )

    @async_step("Click Delete Secret button")
    async def ui_click_delete_secret_btn(self, secret_name: str) -> None:
        await self._pm.secrets_page.click_delete_secret_btn(secret_name)
