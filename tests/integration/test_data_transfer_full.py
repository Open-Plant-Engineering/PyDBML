from pydbml.core.engine import Engine
from pydbml.plugins import pydbml_function


# =====================================================
# ✅ TEST PLUGIN FUNCTIONS (used by tests)
# =====================================================

@pydbml_function
def receive_array(a):
    # expects dict-like {1:10,2:20}
    return len(a)


@pydbml_function
def check_bool(x):
    return not x


@pydbml_function
def return_none():
    return None


@pydbml_function
def make_vec():
    from test_plugin import Vec
    return Vec(99)


@pydbml_function
def make_vec_list():
    from test_plugin import Vec
    return [Vec(1), Vec(2)]


@pydbml_function
def mixed_return():
    from test_plugin import Vec
    return {1: Vec(10), 2: 20}


@pydbml_function
def echo_value(x):
    # returns exactly what it receives (useful for direction tests)
    return x


# =====================================================
# ✅ TESTS START HERE
# =====================================================


# -----------------------------------------------------
# ✅ 1. Array → Python
# -----------------------------------------------------
def test_pydbml_array_to_python():
    e = Engine()
    e.execute("import |test_plugin|")
    e.execute("import |tests.integration.test_data_transfer_full|")

    e.execute("!arr = object array()")
    e.execute("!arr[1] = 10")
    e.execute("!arr[2] = 20")

    r = e.execute("!!receive_array(!arr)")

    assert r.value == 2


# -----------------------------------------------------
# ✅ 2. Boolean → Python
# -----------------------------------------------------
def test_boolean_transfer():
    e = Engine()
    e.execute("import |test_plugin|")
    e.execute("import |tests.integration.test_data_transfer_full|")

    r = e.execute("!!check_bool(true)")

    assert r.value is False


# -----------------------------------------------------
# ✅ 3. Python None → PyDBML
# -----------------------------------------------------
def test_none_return():
    e = Engine()
    e.execute("import |test_plugin|")
    e.execute("import |tests.integration.test_data_transfer_full|")

    r = e.execute("!!return_none()")

    assert r is None


# -----------------------------------------------------
# ✅ 4. Python → Plugin Object Return
# -----------------------------------------------------
def test_plugin_object_return():
    e = Engine()
    e.execute("import |test_plugin|")
    e.execute("import |tests.integration.test_data_transfer_full|")

    e.execute("!x = !!make_vec()")

    r = e.execute("!x.x")

    assert r.value == 99


# -----------------------------------------------------
# ✅ 5. Nested Plugin Objects inside list
# -----------------------------------------------------
def test_vec_list_return():
    e = Engine()
    e.execute("import |test_plugin|")
    e.execute("import |tests.integration.test_data_transfer_full|")

    e.execute("!x = !!make_vec_list()")

    r = e.execute("!x[2].x")

    assert r.value == 2


# -----------------------------------------------------
# ✅ 6. Mixed Types (plugin + primitive)
# -----------------------------------------------------
def test_mixed_types():
    e = Engine()
    e.execute("import |test_plugin|")
    e.execute("import |tests.integration.test_data_transfer_full|")

    e.execute("!x = !!mixed_return()")

    r1 = e.execute("!x[1].x")
    r2 = e.execute("!x[2]")

    assert r1.value == 10
    assert r2.value == 20


# -----------------------------------------------------
# ✅ 7. PyDBML → Python Primitive Echo
# -----------------------------------------------------
def test_pydbml_to_python_number():
    e = Engine()
    e.execute("import |test_plugin|")
    e.execute("import |tests.integration.test_data_transfer_full|")

    r = e.execute("!!echo_value(10)")

    assert r.value == 10


# -----------------------------------------------------
# ✅ 8. Python → PyDBML List
# -----------------------------------------------------
@pydbml_function
def get_list():
    return [10, 20, 30]

def test_list_conversion():
    e = Engine()
    e.execute("import |test_plugin|")
    e.execute("import |tests.integration.test_data_transfer_full|")

    e.execute("!x = !!get_list()")

    r = e.execute("!x[2]")

    assert r.value == 20


# -----------------------------------------------------
# ✅ 9. Python → PyDBML Tuple
# -----------------------------------------------------
@pydbml_function
def get_tuple():
    return (10, 20, 30)

def test_tuple_conversion():
    e = Engine()
    e.execute("import |test_plugin|")
    e.execute("import |tests.integration.test_data_transfer_full|")

    e.execute("!x = !!get_tuple()")

    r = e.execute("!x[3]")

    assert r.value == 30


# -----------------------------------------------------
# ✅ 10. Python → PyDBML Set
# -----------------------------------------------------
@pydbml_function
def get_set():
    return {10, 20, 30}

def test_set_conversion():
    e = Engine()
    e.execute("import |test_plugin|")
    e.execute("import |tests.integration.test_data_transfer_full|")

    e.execute("!x = !!get_set()")

    # set is unordered → compare values
    v1 = e.execute("!x[1]").value
    v2 = e.execute("!x[2]").value
    v3 = e.execute("!x[3]").value

    assert {v1, v2, v3} == {10, 20, 30}


# -----------------------------------------------------
# ✅ 11. Nested Structures (list + dict + tuple)
# -----------------------------------------------------
@pydbml_function
def get_nested():
    return {1: [1, 2], 2: (3, 4)}

def test_nested_conversion():
    e = Engine()
    e.execute("import |test_plugin|")
    e.execute("import |tests.integration.test_data_transfer_full|")

    e.execute("!x = !!get_nested()")

    r = e.execute("!x[2][1]")

    assert r.value == 3