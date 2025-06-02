class ExceptionFormatter:
    def __init__(self):
        if self.__class__.can_handle == ExceptionFormatter.can_handle:
            raise NotImplementedError("All formatters must implement 'can_handle()' method!")

        if self.__class__.format == ExceptionFormatter.format:
            raise NotImplementedError("All formatters must implement 'format()' method!")

    def can_handle(self, exception: Exception) -> bool:
        """Returns True if this formatter is responsible for the given exception type."""
        raise NotImplementedError

    def format(self, exception: Exception, context: str, **kwargs) -> str:
        """Returns a human-readable formatted message for Allure/logs."""
        raise NotImplementedError
