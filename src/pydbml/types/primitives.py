from .base import PyDBMLType


class String(PyDBMLType):
    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Expected string value")

    def __str__(self):
        return f"<STRING> '{self.value}'"


class Number(PyDBMLType):
    def validate(self) -> None:
        if not isinstance(self.value, (int, float)):
            raise TypeError("Expected number value")

    def __str__(self):
        return f"<REAL> {self.value}"


class Boolean(PyDBMLType):
    def validate(self) -> None:
        if not isinstance(self.value, bool):
            raise TypeError("Expected boolean value")

    def __str__(self):
        return f"<BOOLEAN> {'TRUE' if self.value else 'FALSE'}"
