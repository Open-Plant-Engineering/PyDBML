from pydbml.core.engine import Engine


def test_concat_operator():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("$!x & ' world'")

    assert result.value == "10 world"


def test_pipe_and_concat():
    engine = Engine()

    engine.execute("!x = 5")
    result = engine.execute("|Value: $!x| & ' units'")

    assert result.value == "Value: 5 units"


def test_plus_not_string_concat():
    engine = Engine()

    try:
        engine.execute("'Hello' + 'World'")
        assert False
    except Exception:
        assert True


def test_complex_mix():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("($!x + 5) & | total|")

    assert result.value == "15 total"