from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class SignupUsernamePageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Signup username page displayed")
    async def verify_ui_signup_username_page_displayed(self) -> None:
        assert await self._pm.signup_username_page.is_loaded(), (
            "Signup username page should be displayed!"
        )

    @async_step("Enter username")
    async def ui_enter_username(self, username: str) -> None:
        await self._pm.signup_username_page.enter_username(username)

    @async_step("Click signup button on Signup username page")
    async def ui_click_signup_button(self) -> None:
        await self._pm.signup_username_page.click_signup_button()
