from pydbml.core.engine import Engine

def test_python_set_to_array():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!x = !!get_set()")

    # sets are unordered → just check values exist
    v1 = e.execute("!x[1]")
    v2 = e.execute("!x[2]")
    v3 = e.execute("!x[3]")

    values = {v1.value, v2.value, v3.value}

    assert values == {10, 20, 30}

def test_nested_set_conversion():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!x = !!get_nested_set()")

    # Validate inner sets (order independent)
    inner1_a = e.execute("!x[1][1]")
    inner1_b = e.execute("!x[1][2]")

    inner2_a = e.execute("!x[2][1]")
    inner2_b = e.execute("!x[2][2]")

    set1 = {inner1_a.value, inner1_b.value}
    set2 = {inner2_a.value, inner2_b.value}

    assert set1 == {1, 2}
    assert set2 == {3, 4}

def test_mixed_conversion():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!x = !!get_mixed()")

    val1 = e.execute("!x[1]")
    val2_a = e.execute("!x[2][1]")
    val2_b = e.execute("!x[2][2]")
    val3_1 = e.execute("!x[3][1]")
    val3_2 = e.execute("!x[3][2]")

    assert val1.value == 1

    # set (unordered)
    assert {val2_a.value, val2_b.value} == {10, 20}

    # tuple (ordered)
    assert val3_1.value == 30
    assert val3_2.value == 40