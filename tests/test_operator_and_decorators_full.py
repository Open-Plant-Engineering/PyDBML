import pytest
from pydbml.core.engine import Engine
from pydbml.plugins import pydbml_class, pydbml_operator, pydbml_method

# =========================================================
# ✅ BASIC NUMBER OPERATOR TESTS
# =========================================================

def test_number_basic_ops():
    e = Engine()

    e.execute("!x = 10")
    e.execute("!y = !x + 5")

    assert e.env.get("y").get().value == 15


def test_number_comparisons():
    e = Engine()

    e.execute("!x = 10")
    e.execute("!y = !x > 5")

    assert e.env.get("y").get().value is True


# =========================================================
# ✅ STRING OPERATOR TESTS
# =========================================================

def test_string_concat_plus():
    e = Engine()

    e.execute("!a = 'Hello'")
    e.execute("!b = 'World'")
    e.execute("!c = !a + !b")

    assert e.env.get("c").get().value == "HelloWorld"


def test_string_concat_amp():
    e = Engine()

    e.execute("!a = 'Hi'")
    e.execute("!b = 'There'")
    e.execute("!c = !a & !b")

    assert e.env.get("c").get().value == "HiThere"


# =========================================================
# ✅ MULTI-ARG OPERATOR TEST
# =========================================================

def test_operator_alias_same_method():
    e = Engine()

    e.execute("!a = 'A'")
    e.execute("!b = 'B'")

    e.execute("!x = !a + !b")
    e.execute("!y = !a & !b")

    assert e.env.get("x").get().value == "AB"
    assert e.env.get("y").get().value == "AB"


# =========================================================
# ✅ METHOD ALIAS TEST
# =========================================================

def test_method_alias():
    e = Engine()

    e.execute("!x = 10")
    e.execute("!a = !x.add(5)")
    e.execute("!b = !x.ADD(5)")
    e.execute("!c = !x.plus(5)")

    assert e.env.get("a").get().value == 15
    assert e.env.get("b").get().value == 15
    assert e.env.get("c").get().value == 15


# =========================================================
# ✅ CLASS MULTI-NAME TEST
# =========================================================

def test_class_alias_names():

    @pydbml_class("vec", "vector")
    class Vec:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        @pydbml_operator("+")
        def add(self, other):
            return Vec(self.x + other.x, self.y + other.y)

    e = Engine()

    e.evaluator.registry.classes["vec"] = Vec
    e.evaluator.registry.classes["vector"] = Vec
    
    # ✅ both should work if registry updated
    e.execute("!a = object vec()")
    e.execute("!b = object vector()")

    assert e.env.get("a").get() is not None
    assert e.env.get("b").get() is not None


# =========================================================
# ✅ PYTHON OBJECT OPERATOR TESTS
# =========================================================
def test_python_object_add():

    @pydbml_class("vec", "vector")
    class Vec:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        @pydbml_operator("+")
        def add(self, other):
            return Vec(self.x + other.x, self.y + other.y)

    e = Engine()
    
    # ✅ CRITICAL: register class directly
    e.evaluator.registry.classes["vec"] = Vec
    e.evaluator.registry.classes["vector"] = Vec

    e.execute("!a = object vec(1,2)")
    e.execute("!b = object vec(3,4)")
    e.execute("!c = !a + !b")

    result = e.env.get("c").get()

    assert result.x == 4
    assert result.y == 6

def test_python_object_comparison():
    
    @pydbml_class("vec", "vector")
    class Vec:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        @pydbml_operator("+")
        def add(self, other):
            return Vec(self.x + other.x, self.y + other.y)
        
        @pydbml_method("MAG", "LENGTH")
        def magnitude(self):
            return (self.x**2 + self.y**2) ** 0.5

        @pydbml_operator(">")
        def gt(self, other):
            return (self.x + self.y) > (other.x + other.y)
        
    e = Engine()

    e.evaluator.registry.classes["vec"] = Vec
    e.evaluator.registry.classes["vector"] = Vec

    e.execute("!a = object vec(5,5)")
    e.execute("!b = object vec(1,1)")
    e.execute("!c = !a > !b")

    assert e.env.get("c").get().value is True


# =========================================================
# ✅ PYTHON OBJECT METHOD ALIAS
# =========================================================

def test_python_method_alias():
    
    @pydbml_class("vec", "vector")
    class Vec:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        @pydbml_operator("+")
        def add(self, other):
            return Vec(self.x + other.x, self.y + other.y)

        @pydbml_method("MAG", "LENGTH")
        def magnitude(self):
            return (self.x**2 + self.y**2) ** 0.5

        @pydbml_operator(">")
        def gt(self, other):
            return (self.x + self.y) > (other.x + other.y)

    e = Engine()

    e.evaluator.registry.classes["vec"] = Vec
    e.evaluator.registry.classes["vector"] = Vec

    e.execute("!a = object vec(3,4)")
    e.execute("!x = !a.mag()")
    e.execute("!y = !a.length()")

    assert int(e.env.get("x").get().value) == 5
    assert int(e.env.get("y").get().value) == 5


# =========================================================
# ✅ OPERATOR CHAINING TEST
# =========================================================

def test_operator_chain():
    e = Engine()

    e.execute("!x = 10")
    e.execute("!y = !x + 5 + 2")

    assert e.env.get("y").get().value == 17


# =========================================================
# ✅ MIXED TYPE OPERATOR TEST
# =========================================================

def test_string_number_mix():
    e = Engine()

    e.execute("!x = 10")
    e.execute("!y = 'Value='")
    e.execute("!z = !y + !x")

    assert e.env.get("z").get().value == "Value=10"


# =========================================================
# ✅ ERROR CASE TEST (OPERATOR NOT FOUND)
# =========================================================

def test_invalid_operator():
    e = Engine()

    e.execute("!x = object array()")   # array has no operators

    with pytest.raises(Exception):
        e.execute("!y = !x + 5")

    e.execute("!x = 'hello'")

    with pytest.raises(Exception):
        e.execute("!y = !x > 5")

    e.execute("!x = 10")

    with pytest.raises(Exception):
        e.execute("!y = !x === 2")   # not defined


# =========================================================
# ✅ MULTI-ALIAS STABILITY
# =========================================================

def test_multiple_alias_consistency():
    e = Engine()

    e.execute("!x = 20")

    e.execute("!a = !x.add(5)")
    e.execute("!b = !x.plus(5)")
    e.execute("!c = !x.sum(5)")

    assert e.env.get("a").get().value == 25
    assert e.env.get("b").get().value == 25
    assert e.env.get("c").get().value == 25