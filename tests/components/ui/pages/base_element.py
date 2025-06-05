from typing import Optional, Any
from playwright.async_api import Page, Locator, expect


class BaseElement:
    def __init__(self, page: Page, selector: str, **kwargs: Any) -> None:
        self.page: Page = page
        self.selector: str = selector
        self.locator: Locator = self.page.locator(selector, **kwargs)

    async def expect_to_be_loaded(self, timeout: int = 5000) -> bool:
        try:
            await expect(self.locator).to_be_visible(timeout=timeout)
            return True
        except TimeoutError:
            return False

    async def click(self) -> None:
        await self.locator.click()

    async def check(self) -> None:
        await self.locator.check()

    async def fill(self, value: str) -> None:
        await self.locator.fill(value)

    async def is_visible(self) -> bool:
        try:
            return await self.locator.is_visible()
        except TimeoutError:
            return False

    async def text_content(self) -> Optional[str]:
        return await self.locator.text_content()

    async def wait_for_selector(self, timeout: Optional[int] = None) -> None:
        await self.page.wait_for_selector(self.selector, timeout=timeout)
