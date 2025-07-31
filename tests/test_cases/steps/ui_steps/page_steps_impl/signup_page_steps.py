from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class SignupPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Enter email")
    async def ui_enter_email(self, email: str) -> None:
        await self._pm.signup_page.enter_email(email)

    @async_step("Enter password")
    async def ui_enter_password(self, password: str) -> None:
        await self._pm.signup_page.enter_password(password)

    @async_step("Click continue button")
    async def ui_click_continue_button(self) -> None:
        await self._pm.signup_page.click_continue_button()
