from pydbml.plugins import pydbml_class, pydbml_method
from .base import PyDBMLType

@pydbml_class
class Boolean(PyDBMLType):

    def __init__(self, value):
        self.value = value

    @pydbml_method("AND")
    def and_(self, other):
        return self.value and other

    @pydbml_method("OR")
    def or_(self, other):
        return self.value or other

    @pydbml_method("NOT")
    def not_(self):
        return not self.value
    
    def validate(self):
        if not isinstance(self.value, bool):
            raise TypeError("Invalid boolean")
