import logging
from abc import ABC, abstractmethod
from typing import Any
from playwright.async_api import Page


class BasePage(ABC):
    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.logger: logging.Logger = logging.getLogger("[🎭 Playwright]")

    def log(self, message: str, level: int = logging.INFO) -> None:
        class_name = self.__class__.__name__
        full_message = f"<{class_name}>: {message}"
        self.logger.log(level, full_message)

    @abstractmethod
    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Must be implemented by all page classes.
        Returns True if the page is considered loaded (key elements are visible).
        """
        ...
