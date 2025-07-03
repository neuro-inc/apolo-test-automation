from typing import Optional, Any, cast
from playwright.async_api import Page, Locator, expect


class BaseElement:
    def __init__(
        self,
        page: Page,
        selector: Optional[str] = None,
        *,
        by_label: Optional[str] = None,
        by_role: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.page: Page = page
        self.selector: str
        self.locator: Locator

        if by_label:
            self.selector = f'get_by_label("{by_label}")'
            self.locator = page.get_by_label(by_label, **kwargs)

        elif by_role:
            self.selector = f'get_by_role("{by_role}", kwargs={kwargs})'
            self.locator = page.get_by_role(cast("Any", by_role), **kwargs)

        elif selector:
            self.selector = selector
            self.locator = page.locator(selector, **kwargs)

        else:
            raise ValueError("Provide one of: 'selector', 'by_label', or 'by_role'.")

    async def expect_to_be_loaded(self, timeout: int = 5000) -> bool:
        try:
            await expect(self.locator).to_be_visible(timeout=timeout)
            return True
        except TimeoutError:
            return False

    async def click(self) -> None:
        timeout = 5000
        await self.locator.wait_for(state="attached", timeout=timeout)
        await expect(self.locator).to_be_visible(timeout=timeout)
        await expect(self.locator).to_be_enabled(timeout=timeout)
        await self.page.wait_for_timeout(200)
        try:
            await self.locator.click()
        except TimeoutError:
            # Fallback in case of overlays
            await self.locator.click(force=True)

    async def check(self) -> None:
        await self.locator.check()

    async def fill(self, value: str) -> None:
        await self.locator.fill(value)

    async def select_option(self, option_name: str) -> None:
        await self.locator.select_option(option_name)

    async def is_visible(self) -> bool:
        try:
            await expect(self.locator).to_be_visible(timeout=3000)
            return True
        except AssertionError:
            return False

    async def is_enabled(self) -> bool:
        return await self.locator.is_enabled()

    async def text_content(self) -> str:
        return await self.locator.inner_text()

    async def wait_for_selector(self, timeout: Optional[int] = None) -> None:
        await self.page.wait_for_selector(self.selector, timeout=timeout)
