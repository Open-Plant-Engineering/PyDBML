from pydbml.types.base import PyDBMLType


class Array(PyDBMLType):
    def __init__(self):
        super().__init__({})  # use dict for sparse array

    def validate(self):
        if not isinstance(self.value, dict):
            raise TypeError("Array must be dict-based")

    def set(self, index: int, item: PyDBMLType):
        if index < 1:
            raise ValueError("Array index starts from 1")
        self.value[index] = item

    def get(self, index: int):
        return self.value.get(index)


    def __str__(self):
        if not self.value:
            return "<ARRAY>"

        lines = ["<ARRAY>"]

        for idx in sorted(self.value.keys()):
            item = self.value[idx]
            lines.append(f"   [{idx}] {item}")

        return "\n".join(lines)
