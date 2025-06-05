from playwright.async_api import expect


class BaseElement:
    def __init__(self, page, selector, **kwargs):
        self.page = page
        self.selector = selector
        self.locator = self.page.locator(selector, **kwargs)

    async def expect_to_be_loaded(self, timeout=5000):
        try:
            await expect(self.locator).to_be_visible(timeout=timeout)
            return True
        except TimeoutError:
            return False

    async def click(self):
        await self.locator.click()

    async def fill(self, value):
        await self.locator.fill(value)

    async def is_visible(self):
        try:
            return await self.locator.is_visible()
        except TimeoutError:
            return False

    async def text_content(self):
        return await self.locator.text_content()

    async def wait_for_selector(self, timeout=None):
        await self.page.wait_for_selector(self.selector, timeout=timeout)
