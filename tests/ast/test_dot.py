from pydbml.core.engine import Engine


def test_dot_assignment():
    engine = Engine()

    engine.execute("!x = object ARRAY()")
    engine.execute("!x.name = 'Tommy'")

    result = engine.execute("!x.name")

    assert result.value == "Tommy"


def test_dot_on_index():
    engine = Engine()

    engine.execute("!x = object ARRAY()")
    engine.execute("!x[1] = object ARRAY()")
    engine.execute("!x[1].name = 'Nested'")

    result = engine.execute("!x[1].name")

    assert result.value == "Nested"