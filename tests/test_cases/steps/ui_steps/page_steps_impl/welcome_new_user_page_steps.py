from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class WelcomeNewUserPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify that Welcome new user page displayed")
    async def verify_ui_page_displayed(self, email: str) -> None:
        assert await self._pm.welcome_new_user_page.is_loaded(email=email), (
            "Welcome new user page should be displayed!"
        )

    @async_step("Click the let's do it button on Welcome page")
    async def ui_click_lets_do_it_button(self) -> None:
        await self._pm.welcome_new_user_page.click_lets_do_it_button()
