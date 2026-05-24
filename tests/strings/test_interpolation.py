from pydbml.core.engine import Engine


def test_pipe_interpolation_simple():
    engine = Engine()

    engine.execute("!x = 18")
    result = engine.execute("|Hello $!x|")

    assert result.value == "Hello 18"


def test_pipe_ignore_plain_variable():
    engine = Engine()

    engine.execute("!x = 18")
    result = engine.execute("|Hello !x|")

    assert result.value == "Hello !x"


def test_multiple_interpolation():
    engine = Engine()

    engine.execute("!a = 10")
    engine.execute("!b = 20")

    result = engine.execute("|$!a + $!b|")

    assert result.value == "10 + 20"


def test_boolean_interpolation():
    engine = Engine()

    engine.execute("!x = TRUE")
    result = engine.execute("|Value: $!x|")

    assert result.value == "Value: True"