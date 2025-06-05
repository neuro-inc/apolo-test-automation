import traceback
import logging
import os

from tests.utils.exception_handling.playwright_formatter import (
    PlaywrightExceptionFormatter,
)
from tests.utils.exception_handling.schema_formatter import JsonSchemaFormatter


class ExceptionManager:
    def __init__(
        self, logger: logging.Logger = None, log_file: str = "test_errors.log"
    ):
        self.logger = logger or self._create_default_logger(log_file)
        self.formatters = [
            PlaywrightExceptionFormatter(),
            JsonSchemaFormatter(),
        ]

    def handle(self, exception: Exception, context: str = "", **kwargs) -> str:
        debug = self.logger.isEnabledFor(logging.DEBUG)

        for formatter in self.formatters:
            if formatter.can_handle(exception):
                message = formatter.format(exception, context, **kwargs)
                return self._output(message, exception, debug)

        fallback = f"[{type(exception).__name__}] during step: {context}\nMessage: {str(exception)}"
        return self._output(fallback, exception, debug)

    def _output(self, message: str, exception: Exception, debug: bool) -> str:
        if debug:
            tb = "".join(
                traceback.format_exception(
                    type(exception), exception, exception.__traceback__
                )
            )
            message += "\n\nTraceback:\n" + tb

        return message

    def _create_default_logger(self, log_file: str) -> logging.Logger:
        logger = logging.getLogger("exception_manager")
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)

            os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            )

            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

        return logger
