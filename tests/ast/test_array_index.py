from pydbml.core.engine import Engine


def test_array_index_assignment():
    engine = Engine()

    engine.execute("!x = object ARRAY()")
    engine.execute("!x[1] = 5")

    result = engine.execute("!x[1]")

    assert result.value == 5

def test_array_multiple_types():
    engine = Engine()

    engine.execute("!x = object ARRAY()")
    engine.execute("!x[1] = 5")
    engine.execute("!x[2] = 'Tommy'")

    result1 = engine.execute("!x[1]")
    result2 = engine.execute("!x[2]")

    assert result1.value == 5
    assert result2.value == "Tommy"

def test_index_expression():
    engine = Engine()

    engine.execute("!x = object ARRAY()")
    engine.execute("!i = 1")

    engine.execute("!x[!i] = 100")

    result = engine.execute("!x[1]")

    assert result.value == 100