from abc import ABC, abstractmethod
from typing import Any


class PyDBMLType(ABC):
    """
    Base class for all PyDBML data types.
    """

    def __init__(self, value: Any):
        self.value = value

    @abstractmethod
    def validate(self) -> None:
        """Validate type constraints"""
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    def __str__(self) -> str:
        return str(self.value)

    def to_python(self) -> Any:
        """Convert to native Python type"""
        return self.value
