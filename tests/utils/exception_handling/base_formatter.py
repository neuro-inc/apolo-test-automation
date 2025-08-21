from abc import ABC, abstractmethod
from typing import Any


class ExceptionFormatter(ABC):
    @abstractmethod
    def can_handle(self, exception: Exception) -> bool:
        pass

    @abstractmethod
    def format(self, exception: Exception, context: str, **kwargs: Any) -> str:
        pass
