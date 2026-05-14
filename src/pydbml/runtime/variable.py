from pydbml.types.base import PyDBMLType


class Variable:
    """
    Represents a variable in PyDBML runtime.
    """

    def __init__(self, name: str, value: PyDBMLType | None, is_global: bool = False):
        self.name = name
        self.value = value
        self.is_global = is_global

    def set(self, value: PyDBMLType) -> None:
        self.value = value

    def get(self) -> PyDBMLType:
        if self.value is None:
            raise ValueError(f"Variable '{self.name}' is not initialized")
        return self.value

    def delete(self) -> None:
        self.value = None
