from pydbml.core.engine import Engine


def test_precedence_multiplication_first():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 5")

    engine.execute("!z = !x + !y * 2")
    result = engine.execute("!z")

    assert result.value == 20  # 10 + (5 * 2)


def test_precedence_division():
    engine = Engine()

    engine.execute("!x = 20")
    engine.execute("!y = 2")

    engine.execute("!z = !x / !y + 5")
    result = engine.execute("!z")

    assert result.value == 15  # (20 / 2) + 5


def test_parentheses():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 5")

    engine.execute("!z = (!x + !y) * 2")
    result = engine.execute("!z")

    assert result.value == 30


def test_nested_expression():
    engine = Engine()

    engine.execute("!x = 2")
    engine.execute("!y = 3")

    engine.execute("!z = (!x + !y) * (!x + 1)")
    result = engine.execute("!z")

    assert result.value == 15