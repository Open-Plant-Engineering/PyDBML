from typing import List
from .base import PyDBMLType


class Array(PyDBMLType):
    def __init__(self, value: List[PyDBMLType]):
        super().__init__(value)

    def validate(self) -> None:
        if not isinstance(self.value, list):
            raise TypeError("Expected list")

        for item in self.value:
            if not isinstance(item, PyDBMLType):
                raise TypeError("Array must contain PyDBMLType values")

    def to_python(self):
        return [item.to_python() for item in self.value]