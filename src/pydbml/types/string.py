from pydbml.plugins import pydbml_class, pydbml_method, pydbml_operator
from .base import PyDBMLType

@pydbml_class
class String(PyDBMLType):

    def __init__(self, value):
        self.value = value

    @pydbml_method("LENGTH")
    def length(self):
        return len(self.value)

    def validate(self):
        if not isinstance(self.value, str):
            raise TypeError("Invalid string")
        
    @pydbml_operator("&")
    @pydbml_operator("+")
    def concat(self, other):
        return self.value + str(other)
