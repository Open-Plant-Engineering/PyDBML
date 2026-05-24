import pytest
from pydbml.core.engine import Engine
from pydbml.plugins import pydbml_extend, pydbml_method, pydbml_operator
from pydbml.lexer.tokenizer import tokenize

def test_dynamic_operator_basic():

    @pydbml_extend("real")
    class Ext:
        @pydbml_operator("%")
        def mod(self, other):
            return self.value % other

    e = Engine()

    module = type("TempModule", (), {})()
    module.Ext = Ext
    e.evaluator.registry.register_module(module)

    e.execute("!x = 10")
    e.execute("!y = !x % 3")

    assert e.env.get("y").get().value == 1

def test_multiple_dynamic_operators():

    @pydbml_extend("real")
    class Ext:

        @pydbml_operator("%")
        def mod(self, other):
            return self.value % other

        @pydbml_operator("^")
        def power(self, other):
            return self.value ** other

    e = Engine()

    module = type("TempModule", (), {})()
    module.Ext = Ext
    e.evaluator.registry.register_module(module)

    e.execute("!x = 5")
    e.execute("!a = !x % 2")
    e.execute("!b = !x ^ 2")

    assert e.env.get("a").get().value == 1
    assert e.env.get("b").get().value == 25

def test_override_existing_operator():

    @pydbml_extend("real")
    class Ext:

        @pydbml_operator("+", override=True)
        def custom_add(self, other):
            return 999

    e = Engine()

    module = type("TempModule", (), {})()
    module.Ext = Ext
    e.evaluator.registry.register_module(module)

    e.execute("!x = 5")
    e.execute("!y = !x + 1")

    assert e.env.get("y").get().value == 999

def test_string_custom_operator():

    @pydbml_extend("string")
    class Ext:

        @pydbml_operator("%")
        def concat_mod(self, other):
            return self.value + str(other)

    e = Engine()

    module = type("TempModule", (), {})()
    module.Ext = Ext
    e.evaluator.registry.register_module(module)

    e.execute("!x = 'val='")
    e.execute("!y = !x % 10")

    assert e.env.get("y").get().value == "val=10"

def test_operator_chaining():

    @pydbml_extend("real")
    class Ext:

        @pydbml_operator("%")
        def mod(self, other):
            return self.value % other

    e = Engine()

    module = type("TempModule", (), {})()
    module.Ext = Ext
    e.evaluator.registry.register_module(module)

    e.execute("!x = 10")
    e.execute("!y = !x % 3 % 2")

    assert e.env.get("y").get().value == 1   # (10 % 3 = 1 → 1 % 2 = 1)


def test_mix_builtin_and_dynamic_operator():

    @pydbml_extend("real")
    class Ext:

        @pydbml_operator("%")
        def mod(self, other):
            return self.value % other

    e = Engine()

    module = type("TempModule", (), {})()
    module.Ext = Ext
    e.evaluator.registry.register_module(module)

    e.execute("!x = 10")
    e.execute("!y = (!x + 2) % 4")

    assert e.env.get("y").get().value == 0

import pytest

def test_unregistered_operator():

    e = Engine()

    e.execute("!x = 10")

    with pytest.raises(Exception):
        e.execute("!y = !x ^ 2")   # ^ not registered


def test_tokenizer_dynamic_operator():

    @pydbml_extend("real")
    class Ext:

        @pydbml_operator("%")
        def mod(self, other):
            return self.value % other

    module = type("TempModule", (), {})()
    module.Ext = Ext

    e = Engine()
    e.evaluator.registry.register_module(module)

    tokens = tokenize("!x % 3")

    token_values = [t.value for t in tokens]

    assert "%" in token_values


def test_tokenizer_dynamic_operator():

    @pydbml_extend("real")
    class Ext:

        @pydbml_operator("%")
        def mod(self, other):
            return self.value % other

    module = type("TempModule", (), {})()
    module.Ext = Ext

    e = Engine()
    e.evaluator.registry.register_module(module)

    tokens = tokenize("!x % 3")

    token_values = [t.value for t in tokens]

    assert "%" in token_values
def test_multi_type_operator_extension():

    @pydbml_extend("real", "string")
    class Ext:

        @pydbml_operator("%")
        def op(self, other):
            if hasattr(self, "value") and isinstance(self.value, str):
                return self.value + str(other)
            return self.value % other

    e = Engine()

    module = type("TempModule", (), {})()
    module.Ext = Ext
    e.evaluator.registry.register_module(module)

    e.execute("!a = 10 % 3")
    e.execute("!b = 'x=' % 5")

    assert e.env.get("a").get().value == 1
    assert e.env.get("b").get().value == "x=5"
