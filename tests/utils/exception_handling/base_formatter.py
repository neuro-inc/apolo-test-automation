from abc import ABC, abstractmethod


class ExceptionFormatter(ABC):
    @abstractmethod
    def can_handle(self, exception: Exception) -> bool:
        pass

    @abstractmethod
    def format(self, exception: Exception, context: str, **kwargs) -> str:
        pass
