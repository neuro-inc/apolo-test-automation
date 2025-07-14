from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class ThatsItPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._thats_it_title = BaseElement(self.page, "h3", has_text="That's it")
        self._nice_text_field = BaseElement(
            self.page,
            "p",
            has_text="Now go and change the world! And don't forget to have fun",
        )
        self._lets_do_it_button = BaseElement(
            self.page, "button", has_text="Let's do it!"
        )

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        await self.page.wait_for_timeout(1000)
        return (
            await self._thats_it_title.expect_to_be_loaded()
            and await self._nice_text_field.expect_to_be_loaded()
            and await self._lets_do_it_button.expect_to_be_loaded()
        )

    async def click_lets_do_it_button(self) -> None:
        self.log("Click let's do it button")
        await self._lets_do_it_button.click()
        await self.page.wait_for_load_state("networkidle")
        await self.page.wait_for_timeout(3000)
        await self.page.reload()
