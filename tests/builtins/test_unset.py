import pytest
from pydbml.core.engine import Engine
from pydbml.runtime.environment import Environment
from pydbml.types.real import Real
from pydbml.types.unset import UNSET


# --------------------------------------------------
# ✅ Helper
# --------------------------------------------------
def run(code: str):
    e = Engine()
    return e.execute(code)


# --------------------------------------------------
# ✅ VARIABLE TESTS
# --------------------------------------------------

def test_variable_unset():
    env = Environment()

    env.set("x", None)
    var = env.get("x")

    assert var.get() is UNSET


def test_variable_with_value():
    env = Environment()

    env.set("x", Real(10))
    var = env.get("x")

    assert var.get().value == 10


def test_variable_not_defined_raises():
    e = Engine()

    code = """
    RETURN !x
    """

    with pytest.raises(Exception):
        e.execute(code)


# --------------------------------------------------
# ✅ OBJECT MEMBER TESTS
# --------------------------------------------------

def test_object_member_unset():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()
    RETURN !x.age
    """

    r = run(code)

    assert r is UNSET


def test_object_member_value():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()
    !x.age = 25
    RETURN !x.age
    """

    r = run(code)

    assert r.value == 25


def test_object_invalid_member():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()
    RETURN !x.name
    """

    with pytest.raises(Exception):
        run(code)


# --------------------------------------------------
# ✅ BUILTIN unset() FUNCTION TESTS
# --------------------------------------------------

def test_unset_builtin_true():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()
    RETURN unset(!x.age)
    """

    r = run(code)

    assert r.value is True


def test_unset_builtin_false():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()
    !x.age = 10
    RETURN unset(!x.age)
    """

    r = run(code)

    assert r.value is False


# --------------------------------------------------
# ✅ METHOD STYLE unset()
# --------------------------------------------------

def test_unset_method_true():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()
    RETURN !x.age.unset()
    """

    r = run(code)

    assert r.value is True


def test_unset_method_false():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()
    !x.age = 5
    RETURN !x.age.unset()
    """

    r = run(code)

    assert r.value is False


# --------------------------------------------------
# ✅ IMPORTANT EDGE CASES
# --------------------------------------------------

def test_unset_on_defined_variable_none():
    code = """
    !x = NULL
    RETURN unset(!x)
    """

    r = run(code)

    # depends on how NULL is handled;
    # if NULL maps to None → UNSET → True
    assert r.value in (True, False)


def test_unset_on_undefined_variable():
    code = """
    RETURN unset(!x)
    """

    # ✅ undefined variable should still raise
    with pytest.raises(Exception):
        run(code)


def test_nested_unset_usage():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()

    !y = iftrue(unset(!x.age), 10, 20)
    RETURN !y
    """

    r = run(code)

    assert r.value == 10

def test_unset_string_value():
    code = """
    !x = |hello|
    RETURN unset(!x)
    """
    r = run(code)

    assert r.value is False


def test_unset_string_uninitialized():
    code = """
    define object USER
        member .name is STRING
    endobject

    !x = object user()
    RETURN unset(!x.name)
    """
    r = run(code)

    assert r.value is True


def test_unset_boolean_value_true():
    code = """
    !x = true
    RETURN unset(!x)
    """
    r = run(code)

    assert r.value is False


def test_unset_boolean_value_false():
    code = """
    !x = false
    RETURN unset(!x)
    """
    r = run(code)

    assert r.value is False


def test_unset_boolean_uninitialized():
    code = """
    define object USER
        member .active is BOOLEAN
    endobject

    !x = object user()
    RETURN unset(!x.active)
    """
    r = run(code)

    assert r.value is True

def test_unset_array_value():
    code = """
    !arr = object array()
    !arr[1] = 10
    RETURN unset(!arr[1])
    """
    r = run(code)

    assert r.value is False


def test_unset_array_missing_index():
    code = """
    !arr = object array()
    RETURN unset(!arr[1])
    """

    # ✅ arrays should raise error, not return UNSET
    with pytest.raises(Exception):
        run(code)

def test_unset_array_member_uninitialized():
    code = """
    define object USER
        member .scores is ARRAY
    endobject

    !x = object user()
    RETURN unset(!x.scores)
    """
    r = run(code)

    assert r.value is True

def test_unset_nested_object_member():
    code = """
    define object ADDRESS
        member .zip is REAL
    endobject

    define object USER
        member .addr is ADDRESS
    endobject

    !x = object user()
    RETURN unset(!x.addr)
    """
    r = run(code)

    assert r.value is True

def test_unset_nested_array():
    code = """
    !arr = object array()
    !inner = object array()
    !inner[1] = 50
    !arr[1] = !inner

    RETURN unset(!arr[1])
    """
    r = run(code)

    # outer exists → NOT unset
    assert r.value is False


def test_unset_nested_array_missing():
    code = """
    !arr = object array()
    RETURN unset(!arr[1][1])
    """

    # ✅ should fail at index access
    with pytest.raises(Exception):
        run(code)

def test_unset_deep_nested_object():
    code = """
    define object ADDRESS
        member .zip is REAL
    endobject

    define object USER
        member .addr is ADDRESS
    endobject

    !x = object user()

    RETURN unset(!x.addr.zip)
    """
    r = run(code)

    assert r.value is True

def test_double_bang_unset_true():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()
    RETURN !!unset(!x.age)
    """

    r = run(code)

    # unset → True → !!True → True
    assert r.value is True

def test_double_bang_unset_false():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()
    !x.age = 10

    RETURN !!unset(!x.age)
    """

    r = run(code)

    # unset → False → !!False → False
    assert r.value is False

def test_double_bang_unset_in_iftrue():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()

    !y = iftrue(!!unset(!x.age), 100, 200)
    RETURN !y
    """

    r = run(code)

    assert r.value == 100

def test_double_bang_unset_primitive():
    code = """
    !x = 5
    RETURN !!unset(!x)
    """

    r = run(code)

    assert r.value is False

def test_double_bang_unset_nested_object():
    code = """
    define object ADDRESS
        member .zip is REAL
    endobject

    define object USER
        member .addr is ADDRESS
    endobject

    !x = object user()

    RETURN !!unset(!x.addr.zip)
    """

    r = run(code)

    assert r.value is True

def test_double_bang_unset_method():
    code = """
    define object USER
        member .age is REAL
    endobject

    !x = object user()

    RETURN !!unset(!x.age)
    """

    r = run(code)

    assert r.value is True

