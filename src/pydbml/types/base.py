from abc import ABC, abstractmethod
from typing import Any
from pydbml.plugins import pydbml_member, pydbml_method, pydbml_operator

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

    def __repr__(self):
        return f"<{self.__class__.__name__.upper()}> {getattr(self, 'value', '')}"

    def __str__(self) -> str:
        return str(self.value)

    def to_python(self) -> Any:
        """Convert to native Python type"""
        return self.value

    @pydbml_method("OBJECTTYPE")
    def objecttype(self):
        return self.__class__.__name__.upper()