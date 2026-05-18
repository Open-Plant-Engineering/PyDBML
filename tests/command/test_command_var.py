from pydbml.core.engine import Engine
from pydbml.types.real import Real

def test_command_var_basic():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("$!x")

    assert result.value == 10


def test_command_var_type_preserved():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("$!x")

    assert isinstance(result, Real)


def test_command_var_expression():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("$!x + 5")

    assert result.value == 15


def test_command_var_concat():
    engine = Engine()

    engine.execute("!x = 10")
    result = engine.execute("$!x & 'abc'")

    assert result.value == "10abc"


def test_global_command_var():
    engine = Engine()

    engine.execute("!!x = 100")

    result = engine.execute("$!!x")

    assert result.value == 100

def test_pipe_global_interpolation():
    engine = Engine()

    engine.execute("!!x = 50")

    result = engine.execute("|Value is $!!x|")

    assert result.value == "Value is 50"
