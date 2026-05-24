from pydbml.core.engine import Engine

def test_class_case_insensitive():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!x = object myclass()")  # lowercase class
    result = e.execute("!x.get()")

    assert result.value == 0

def test_method_case_insensitive():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!x = object MyClass()")

    e.execute("!x.ADD(10)")
    e.execute("!x.Add(5)")

    result = e.execute("!x.GET()")

    assert result.value == 15

def test_function_case_insensitive():
    e = Engine()

    e.execute("import |test_plugin|")

    r1 = e.execute("!!multiply(2,3)")
    r2 = e.execute("!!MULTIPLY(2,3)")
    r3 = e.execute("!!Multiply(2,3)")

    assert r1.value == 6
    assert r2.value == 6
    assert r3.value == 6
