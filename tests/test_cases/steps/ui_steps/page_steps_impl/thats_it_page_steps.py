from tests.reporting_hooks.reporting import async_step
from tests.components.ui.page_manager import PageManager


class ThatsItPageSteps:
    def __init__(
        self,
        page_manager: PageManager,
    ) -> None:
        self._pm = page_manager

    @async_step("Verify That's it page displayed")
    async def verify_ui_page_displayed(self) -> None:
        assert await self._pm.thats_it_page.is_loaded(), (
            "That's it page should be loaded!"
        )

    @async_step("Click lets do it button on That's it page")
    async def ui_click_lets_do_it_button(self) -> None:
        await self._pm.thats_it_page.click_lets_do_it_button()
