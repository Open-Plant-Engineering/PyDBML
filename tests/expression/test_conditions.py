from pydbml.core.engine import Engine


def test_greater_than():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("!x > 5")

    assert result.value is True


def test_less_than():
    engine = Engine()

    engine.execute("!x = 2")
    result = engine.execute("!x < 5")

    assert result.value is True


def test_equal():
    engine = Engine()

    engine.execute("!x = 5")
    result = engine.execute("!x == 5")

    assert result.value is True