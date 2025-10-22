import logging
from abc import ABC, abstractmethod
from typing import Any
from playwright.async_api import Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


class BasePage(ABC):
    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.logger: logging.Logger = logging.getLogger("[🎭 Playwright]")

    def log(self, message: str, level: int = logging.INFO) -> None:
        class_name = self.__class__.__name__
        full_message = f"<{class_name}>: {message}"
        self.logger.log(level, full_message)

    async def wait_for_spinner(
        self, spinner_selector: str = ".chase-spinner", timeout: int = 6000
    ) -> None:
        try:
            self.log("Waiting for spinner")
            await self.page.wait_for_selector(
                spinner_selector, state="visible", timeout=timeout
            )
            self.log("Waiting for spinner to disappear")
            await self.page.wait_for_selector(
                spinner_selector, state="hidden", timeout=timeout
            )
        except PlaywrightTimeoutError:
            self.log("Timeout error for spinner")
            pass

    async def reload(self):
        try:
            await self.page.reload(timeout=60000, wait_until="domcontentloaded")
            await self.wait_for_spinner()
        except PlaywrightTimeoutError:
            self.log("Page reload took too long — continuing anyway.", level=logging.WARNING)

    @property
    async def current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    @abstractmethod
    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Must be implemented by all page classes.
        Returns True if the page is considered loaded (key elements are visible).
        """
        ...
