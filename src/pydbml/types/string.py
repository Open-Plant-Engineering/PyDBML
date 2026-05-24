from pydbml.plugins import pydbml_class, pydbml_method, pydbml_operator
from .base import PyDBMLType


@pydbml_class
class String(PyDBMLType):

    def __init__(self, value):
        self.value = value

    def validate(self):
        if not isinstance(self.value, str):
            raise TypeError("Invalid string")

    # --------------------------
    # ✅ OPERATORS
    # --------------------------

    @pydbml_operator("+", "&")
    def concat(self, other):
        def fmt(v):
            if isinstance(v, float) and v.is_integer():
                return str(int(v))
            return str(v)

        return self.value + fmt(other)

    @pydbml_method("EQ")
    @pydbml_operator("==")
    def eq(self, other):
        return self.value == str(other)

    @pydbml_method("NEQ")
    @pydbml_operator("!=")
    def ne(self, other):
        return self.value != str(other)

    @pydbml_operator(">")
    @pydbml_method("GT")
    def gt(self, other):
        return self.value > str(other)

    @pydbml_operator("<")
    @pydbml_method("LT")
    def lt(self, other):
        return self.value < str(other)

    @pydbml_operator(">=")
    @pydbml_method("GEQ")
    def ge(self, other):
        return self.value >= str(other)

    @pydbml_operator("<=")
    @pydbml_method("LEQ")
    def le(self, other):
        return self.value <= str(other)

    # --------------------------
    # ✅ BASIC METHODS
    # --------------------------

    @pydbml_method("UPPER")
    def upper(self):
        return self.value.upper()

    @pydbml_method("LOWER")
    def lower(self):
        return self.value.lower()

    @pydbml_method("LENGTH")
    def length(self):
        return len(self.value)

    # --------------------------
    # ✅ USEFUL STRING METHODS
    # --------------------------

    @pydbml_method("STRIP")
    def strip(self):
        return self.value.strip()

    @pydbml_method("LTRIM")
    def lstrip(self):
        return self.value.lstrip()

    @pydbml_method("RTRIM")
    def rstrip(self):
        return self.value.rstrip()

    @pydbml_method("STARTSWITH")
    def startswith(self, prefix):
        return self.value.startswith(str(prefix))

    @pydbml_method("ENDSWITH")
    def endswith(self, suffix):
        return self.value.endswith(str(suffix))

    @pydbml_method("CONTAINS")
    def contains(self, substring):
        return str(substring) in self.value

    @pydbml_method("REPLACE")
    def replace(self, old, new):
        return self.value.replace(str(old), str(new))

    @pydbml_method("SPLIT")
    def split(self, sep):
        return self.value.split(str(sep))

    @pydbml_method("INDEXOF")
    def indexof(self, sub):
        return self.value.find(str(sub))  # -1 if not found

    @pydbml_method("SUBSTRING")
    def substring(self, start, end=None):
        start = int(start)
        if end is None:
            return self.value[start:]
        return self.value[start:int(end)]

    # --------------------------
    # ✅ CONVERSION
    # --------------------------

    @pydbml_method("TOREAL")
    def toreal(self):
        try:
            return float(self.value)
        except:
            raise TypeError("Cannot convert string to real")

    @pydbml_method("TOBOOLEAN")
    def toboolean(self):
        val = self.value.lower()
        if val in ("true", "1"):
            return True
        if val in ("false", "0"):
            return False
        raise TypeError("Cannot convert string to boolean")

