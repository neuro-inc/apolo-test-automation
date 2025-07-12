from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class AuthPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Click signup button")
    async def ui_click_signup_button(self) -> None:
        await self._pm.auth_page.click_sign_up_button()

    @async_step("Verify that Auth page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.auth_page.is_loaded(), "Auth page should be displayed!"

    @async_step("Click login button")
    async def ui_click_login_button(self) -> None:
        await self._pm.auth_page.click_log_in_button()
