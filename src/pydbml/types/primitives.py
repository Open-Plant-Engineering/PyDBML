from .base import PyDBMLType


class String(PyDBMLType):
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Expected string value")


class Number(PyDBMLType):
    def validate(self) -> None:
        if not isinstance(self.value, (int, float)):
            raise TypeError("Expected number value")


class Boolean(PyDBMLType):
    def validate(self) -> None:
        if not isinstance(self.value, bool):
            raise TypeError("Expected boolean value")