from pydbml.types.base import PyDBMLType
from pydbml.utils.debug import debug

class Array(PyDBMLType):
    def __init__(self):
        super().__init__({})  # use dict for sparse array

    def validate(self):
        if not isinstance(self.value, dict):
            raise TypeError("Array must be dict-based")

    def set(self, index: int, item: PyDBMLType):
        if not isinstance(index, int):
            raise TypeError("Array index must be integer")

        if index < 1:
            raise ValueError("Array index starts from 1")

        if not isinstance(item, PyDBMLType):
            raise TypeError("Array value must be PyDBMLType")
        
        debug("ARRAY SET", f"index={index}, value={item}")
        debug("ARRAY STATE", self.value)

        self.value[index] = item

    def get(self, index: int):
        if index not in self.value:
            raise KeyError(f"Index {index} not set")
        debug("ARRAY GET", f"index={index}, value={self.value.get(index)}")
        return self.value.get(index)


    def __str__(self):
        if not self.value:
            return "<ARRAY>"

        lines = ["<ARRAY>"]

        for idx in sorted(self.value.keys()):
            item = self.value[idx]
            lines.append(f"   [{idx}] {item}")

        return "\n".join(lines)
