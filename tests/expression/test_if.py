from pydbml.core.engine import Engine


def test_if_true():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("IF !x > 5 THEN 1 ELSE 0")

    assert result.value == 1

def test_if_false():
    engine = Engine()

    engine.execute("!x = 2")
    result = engine.execute("IF !x > 5 THEN 1 ELSE 0")

    assert result.value == 0

def test_nested_if():
    engine = Engine()

    engine.execute("!x = 10")

    result = engine.execute(
        "IF !x > 5 THEN IF !x > 8 THEN 2 ELSE 1 ELSE 0"
    )

    assert result.value == 2

def test_if_assignment():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = IF !x > 5 THEN 100 ELSE 0")

    result = engine.execute("!y")

    assert result.value == 100