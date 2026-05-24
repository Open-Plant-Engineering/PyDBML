import pytest
from pydbml.core.engine import Engine
from pydbml.plugins import pydbml_extend, pydbml_method, pydbml_operator

# =========================================================
# ✅ BASIC METHOD EXTENSION
# =========================================================
def test_extend_number_method():

    @pydbml_extend("real")
    class NumberExt:

        @pydbml_method("DOUBLE")
        def double(self):
            return self.value * 2


    e = Engine()

    # ✅ register extension manually
    
    module = type("TempModule", (), {})()
    module.NumberExt = NumberExt
    e.evaluator.registry.register_module(module)

    e.execute("!x = 5")
    e.execute("!y = !x.double()")

    assert e.env.get("y").get().value == 10

# =========================================================
# ✅ OPERATOR EXTENSION
# =========================================================
def test_operator_extension():

    @pydbml_extend("string")
    class NumberExt:

        @pydbml_operator("/")
        def mod(self, other):
            return self.value + other


    e = Engine()
    
    module = type("TempModule", (), {})()
    module.NumberExt = NumberExt
    e.evaluator.registry.register_module(module)

    e.execute("!x = |a|")
    e.execute("!y = !x / !x")

    assert e.env.get("y").get().value == "aa"


# =========================================================
# ✅ STRING EXTENSION
# =========================================================
def test_string_extension():

    @pydbml_extend("string")
    class StringExt:

        @pydbml_method("REV")
        def reverse(self):
            return self.value[::-1]


    e = Engine()
    
    module = type("TempModule", (), {})()
    module.StringExt = StringExt
    e.evaluator.registry.register_module(module)

    e.execute("!x = 'abc'")
    e.execute("!y = !x.rev()")

    assert e.env.get("y").get().value == "cba"

# =========================================================
# ✅ CACHE REFRESH TEST (IMPORTANT)
# =========================================================
def test_cache_refresh():

    @pydbml_extend("real")
    class NumberExt:

        @pydbml_method("INC")
        def inc(self):
            return self.value + 1


    e = Engine()
    
    module = type("TempModule", (), {})()
    module.NumberExt = NumberExt
    e.evaluator.registry.register_module(module)

    # ✅ call multiple times to ensure cache consistency
    e.execute("!x = 1")
    e.execute("!x = !x.inc()")
    e.execute("!x = !x.inc()")

    assert e.env.get("x").get().value == 3

# =========================================================
# ✅ MULTIPLE METHODS
# =========================================================
def test_multiple_methods():

    @pydbml_extend("real")
    class NumberExt:

        @pydbml_method("DOUBLE")
        def double(self):
            return self.value * 2

        @pydbml_method("TRIPLE")
        def triple(self):
            return self.value * 3

    e = Engine()
    
    module = type("TempModule", (), {})()
    module.NumberExt = NumberExt
    e.evaluator.registry.register_module(module)

    e.execute("!x = 4")
    e.execute("!a = !x.double()")
    e.execute("!b = !x.triple()")

    assert e.env.get("a").get().value == 8
    assert e.env.get("b").get().value == 12


# =========================================================
# ✅ MULTI-TYPE EXTENSION
# =========================================================
def test_multi_type_extension():

    @pydbml_extend("real", "string")
    class CommonExt:

        @pydbml_method("TYPE")
        def type_of(self):
            return type(self).__name__

    e = Engine()
    
    module = type("TempModule", (), {})()
    module.CommonExt = CommonExt
    e.evaluator.registry.register_module(module)

    e.execute("!x = 10")
    e.execute("!y = 'abc'")

    e.execute("!a = !x.type()")
    e.execute("!b = !y.type()")

    assert e.env.get("a").get().value == "Real"
    assert e.env.get("b").get().value == "String"


# =========================================================
# ✅ ERROR CASE
# =========================================================
def test_extend_invalid_type():

    @pydbml_extend("unknown")
    class BadExt:

        @pydbml_method("X")
        def x(self):
            return 1

    e = Engine()

    with pytest.raises(Exception):
        module = type("TempModule", (), {})()
        module.BadExt = BadExt
        e.evaluator.registry.register_module(module)

