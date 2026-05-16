from pydbml.core.engine import Engine


def test_command_var_basic():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("$!x")

    assert result.value == 10


def test_command_var_type_preserved():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("$!x")

    from pydbml.types.primitives import Number
    assert isinstance(result, Number)


def test_command_var_expression():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("$!x + 5")

    assert result.value == 15


def test_command_var_concat():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("$!x & 'abc'")

    assert result.value == "10abc"