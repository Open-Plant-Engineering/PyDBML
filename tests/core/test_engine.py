from pydbml.core.engine import Engine


def test_number_assignment():
    engine = Engine()

    result = engine.execute("!x = 10")
    assert result == "x set"


def test_number_lookup():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("!x")

    assert result.value == 10


def test_string_assignment():
    engine = Engine()

    engine.execute("!name = 'Tommy'")
    result = engine.execute("!name")

    assert result.value == "Tommy"


def test_boolean_assignment():
    engine = Engine()

    engine.execute("!flag = true")
    result = engine.execute("!flag")

    assert result.value is True

def test_variable_reference():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = !x")

    result = engine.execute("!y")

    assert result.value == 10