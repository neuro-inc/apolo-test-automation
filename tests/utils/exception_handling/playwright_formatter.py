import re
from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
    Error as PlaywrightError,
)

from tests.utils.exception_handling.base_formatter import ExceptionFormatter


class PlaywrightExceptionFormatter(ExceptionFormatter):
    def can_handle(self, exception: Exception) -> bool:
        return isinstance(exception, (PlaywrightTimeoutError, PlaywrightError))

    def format(self, exception: Exception, context: str, **kwargs) -> str:
        message = f"[{type(exception).__name__}] during step: {context}\nMessage: {str(exception)}"

        page = kwargs.get("page")
        if page:
            try:
                message += f"\nURL at error: {page.url}"
            except Exception:
                message += "\nURL at error: (unavailable)"

        if isinstance(exception, PlaywrightTimeoutError):
            message += (
                "\nNote: Playwright Timeout. Element not found or action took too long."
            )
            match = re.search(r'waiting for selector "([^"]+)"', str(exception))
            if match:
                message += f"\nFailed Selector: `{match.group(1)}`"
        return message
