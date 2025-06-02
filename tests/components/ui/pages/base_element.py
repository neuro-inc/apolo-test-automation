from playwright.sync_api import expect


class BaseElement:
    def __init__(self, page, selector, **kwargs):
        self.page = page
        self.selector = selector
        self.locator = self.page.locator(selector, **kwargs)

    def expect_to_be_loaded(self, timeout=5000):
        try:
            expect(self.locator).to_be_visible(timeout=timeout)
            return True
        except TimeoutError:
            return False

    def click(self):
        self.locator.click()

    def fill(self, value):
        self.locator.fill(value)

    def is_visible(self):
        try:
            return self.locator.is_visible()
        except TimeoutError:
            return False

    def text_content(self):
        return self.locator.text_content()

    def wait_for_selector(self, timeout=None):
        self.page.wait_for_selector(self.selector, timeout=timeout)