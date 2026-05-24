from pydbml.core.engine import Engine


def test_command_var_array_index():
    engine = Engine()

    engine.execute("!arr = object ARRAY()")
    engine.execute("!arr[1] = 100")
    engine.execute("!i = 1")

    result = engine.execute("!arr[$!i]")

    assert result.value == 100