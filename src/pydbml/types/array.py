from pydbml.plugins import pydbml_class, pydbml_method
from .base import PyDBMLType

@pydbml_class
class Array(PyDBMLType):

    def __init__(self):
        self.value = {}

    def validate(self):
        if not isinstance(self.value, dict):
            raise TypeError("Invalid array")
    
    @pydbml_method("GET")
    def get(self, index):
        return self.value[int(index)]

    @pydbml_method("SET")
    def set(self, index, value):
        self.value[int(index)] = value
        return value

    @pydbml_method("LENGTH")
    def length(self):
        return len(self.value)
    
    def __str__(self):
        if not self.value:
            return "<ARRAY>"
        return f"<ARRAY> {self.value}"
