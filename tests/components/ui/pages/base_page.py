import logging
from abc import ABC, abstractmethod

class PageLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        class_name = self.extra.get("class_name", "UnknownPage")
        return f"{class_name}: {msg}", kwargs

class BasePage(ABC):
    def __init__(self, page):
        self.page = page
        self.logger = logging.getLogger("[🎭 Playwright]")

    def log(self, message: str, level=logging.INFO):
        class_name = self.__class__.__name__
        full_message = f"<{class_name}>: {message}"
        self.logger.log(level, full_message)

    @abstractmethod
    async def is_loaded(self, **kwargs) -> bool:
        """
        Must be implemented by all page classes.
        Returns True if the page is considered loaded (key elements are visible).
        """
        pass
