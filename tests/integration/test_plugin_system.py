from pydbml.core.engine import Engine

def test_plugin_basic():
    engine = Engine()

    engine.execute("import |test_plugin|")

    engine.execute("!x = object MyClass()")
    engine.execute("!x.add(10)")
    engine.execute("!x.add(5)")

    result = engine.execute("!x.get()")

    assert result.value == 15


def test_plugin_function():
    engine = Engine()

    engine.execute("import |test_plugin|")

    result = engine.execute("!!multiply(3,4)")

    assert result.value == 12