from pydbml.core.engine import Engine


def test_local_variable():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("!x")

    assert result.value == 10


def test_global_variable():
    engine = Engine()

    engine.execute("!!x = 20")
    result = engine.execute("!!x")

    assert result.value == 20


def test_local_overrides_global():
    engine = Engine()

    engine.execute("!!x = 20")
    engine.execute("!x = 10")

    result = engine.execute("!x")

    assert result.value == 10


def test_fallback_to_global():
    engine = Engine()

    engine.execute("!!x = 20")

    result = engine.execute("!x")

    assert result.value == 20