from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class LoginPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Login page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.login_page.is_loaded(), "Login page should be displayed!"

    @async_step("Enter email")
    async def ui_enter_email(self, email: str) -> None:
        await self._pm.login_page.enter_email(text=email)

    @async_step("Enter password")
    async def ui_enter_password(self, password: str) -> None:
        await self._pm.login_page.enter_password(text=password)

    @async_step("Click Continue button")
    async def ui_click_continue_button(self) -> None:
        await self._pm.login_page.click_continue_button()
