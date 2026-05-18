from pydbml.plugins import pydbml_class, pydbml_method, pydbml_operator
from .base import PyDBMLType

@pydbml_class
class Number(PyDBMLType):

    def __init__(self, value):
        self.value = value

    @pydbml_operator("+")
    @pydbml_method("ADD")
    def add(self, other):
        return self.value + other

    @pydbml_operator("-")
    @pydbml_method("SUB")
    def sub(self, other):
        return self.value - other

    @pydbml_operator("*")
    @pydbml_method("MUL")
    def mul(self, other):
        return self.value * other

    @pydbml_operator("/")
    @pydbml_method("DIV")
    def div(self, other):
        return self.value / other

    @pydbml_operator("==")
    @pydbml_method("EQ")
    def eq(self, other):
        return self.value == other

    @pydbml_operator("!=")
    @pydbml_method("NEQ")
    def neq(self, other):
        return self.value != other

    @pydbml_operator(">")
    @pydbml_method("GT")
    def gt(self, other):
        return self.value > other

    @pydbml_operator("<")
    @pydbml_method("LT")
    def lt(self, other):
        return self.value < other

    @pydbml_operator(">=")
    @pydbml_method("GEQ")
    def geq(self, other):
        return self.value >= other

    @pydbml_operator("<=")
    @pydbml_method("LEQ")
    def leq(self, other):
        return self.value <= other

    @pydbml_operator("&")
    def concat(self, other):
        def fmt(v):
            if isinstance(v, float) and v.is_integer():
                return str(int(v))
            return str(v)
    
        return fmt(self.value) + str(other)
    
    def validate(self):
        if not isinstance(self.value, (int, float)):
            raise TypeError("Invalid number")
