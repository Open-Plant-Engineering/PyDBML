from pydbml.core.engine import Engine

def test_python_numeric_return():
    e = Engine()

    e.execute("import |test_plugin|")

    result = e.execute("!!multiply(3,4)")

    assert result.value == 12

def test_plugin_method_numeric():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!x = object MyClass()")
    e.execute("!x.add(10)")

    result = e.execute("!x.get()")

    assert result.value == 10

def test_python_dict_to_array():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!x = !!get_dict()")

    result = e.execute("!x[1]")

    assert result.value == 100

def test_python_list_to_array():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!x = !!get_list()")

    result = e.execute("!x[2]")

    assert result.value == 20

def test_nested_conversion():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!x = !!get_nested()")

    result = e.execute("!x[2][1]")

    assert result.value == 3

def test_boolean_conversion():
    e = Engine()

    e.execute("import |test_plugin|")

    result = e.execute("!!check()")

    assert result.value is True

