from pydbml.core.engine import Engine


def test_pipe_string_basic():
    engine = Engine()

    result = engine.execute("|Hello|")
    assert result.value == "Hello"


def test_pipe_equals_normal_string():
    engine = Engine()

    r1 = engine.execute("|Hello|")
    r2 = engine.execute("'Hello'")

    assert r1.value == r2.value


def test_empty_pipe():
    engine = Engine()

    result = engine.execute("||")
    assert result.value == ""


def test_pipe_multiline():
    engine = Engine()

    result = engine.execute("""|Hello
World|""")

    assert result.value == "Hello\nWorld"


def test_pipe_newline_operator():
    engine = Engine()

    result = engine.execute("|Hello$$World|")

    assert result.value == "Hello\nWorld"