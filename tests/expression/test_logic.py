from pydbml.core.engine import Engine


def test_and_operator():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 3")

    result = engine.execute("!x > 5 AND !y < 5")
    assert result.value is True


def test_or_operator():
    engine = Engine()

    engine.execute("!x = 2")
    engine.execute("!y = 10")

    result = engine.execute("!x > 5 OR !y > 5")
    assert result.value is True


def test_not_operator():
    engine = Engine()

    engine.execute("!x = 2")

    result = engine.execute("NOT !x > 5")
    assert result.value is True


def test_logical_precedence():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 3")

    result = engine.execute("!x > 5 AND !y > 5 OR true")
    assert result.value is True