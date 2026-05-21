from pydbml.plugins import pydbml_class, pydbml_method, pydbml_operator
from .base import PyDBMLType

@pydbml_class
class String(PyDBMLType):

    def __init__(self, value):
        self.value = value

    def validate(self):
        if not isinstance(self.value, str):
            raise TypeError("Invalid string")
        
    @pydbml_operator("+", "&")
    def concat(self, other):
        def fmt(v):
            if isinstance(v, float) and v.is_integer():
                return str(int(v))
            return str(v)

        return self.value + fmt(other)

    @pydbml_method("UPPER")
    def upper(self):
        return self.value.upper()

    @pydbml_method("LOWER")
    def lower(self):
        return self.value.lower()

    @pydbml_method("LENGTH")
    def length(self):
        return len(self.value)