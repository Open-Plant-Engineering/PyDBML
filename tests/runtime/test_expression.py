from pydbml.core.engine import Engine


def test_addition():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 5")

    result = engine.execute("!z = !x + !y")
    assert result == "z set"

    value = engine.execute("!z")
    assert value.value == 15


def test_subtraction():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 3")

    engine.execute("!z = !x - !y")
    value = engine.execute("!z")

    assert value.value == 7


def test_multiplication():
    engine = Engine()

    engine.execute("!x = 4")
    engine.execute("!y = 5")

    engine.execute("!z = !x * !y")
    value = engine.execute("!z")

    assert value.value == 20


def test_division():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 2")

    engine.execute("!z = !x / !y")
    value = engine.execute("!z")

    assert value.value == 5


def test_string_concat():
    engine = Engine()

    engine.execute("!a = 'Hello'")
    engine.execute("!b = 'World'")

    engine.execute("!c = !a + !b")
    value = engine.execute("!c")

    assert value.value == "HelloWorld"