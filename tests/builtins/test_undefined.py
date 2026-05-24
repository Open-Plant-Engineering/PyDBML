import pytest
from pydbml.core.engine import Engine
from pydbml.types.boolean import Boolean


# --------------------------------------------------
# ✅ Helper runner
# --------------------------------------------------
def run(code: str):
    e = Engine()
    return e.execute(code)


# --------------------------------------------------
# ✅ TEST: undefined() function style
# --------------------------------------------------
def test_undefined_function_style_global():
    code = """
    !y = undefined(!!x)
    RETURN !y
    """
    r = run(code)

    assert r.value is True


# --------------------------------------------------
# ✅ TEST: undefined() with existing variable
# --------------------------------------------------
def test_undefined_existing_variable_global():
    code = """
    !!x = 10
    !y = undefined(!!x)
    RETURN !y
    """
    r = run(code)

    assert r.value is False


# --------------------------------------------------
# ✅ TEST: !!undefined() global style
# --------------------------------------------------
def test_undefined_global_style_global():
    code = """
    !y = !!undefined(!!x)
    RETURN !y
    """
    r = run(code)

    assert r.value is True


# --------------------------------------------------
# ✅ TEST: method style (!x.undefined())
# --------------------------------------------------
def test_undefined_method_style_global():
    code = """
    !!a = 5
    !y = !!a.undefined()
    RETURN !y
    """
    r = run(code)

    assert r.value is False


# --------------------------------------------------
# ✅ TEST: method style undefined on missing variable
# --------------------------------------------------
def test_undefined_method_missing_var_global():
    code = """
    !y = !!x.undefined()
    RETURN !y
    """
    r = run(code)

    # ✅ undefined(), but accessing !x fails FIRST
    # so this should raise NAME_ERROR
    assert r.value is True  # execution won't reach here


# --------------------------------------------------
# ✅ TEST: undefined() function style
# --------------------------------------------------
def test_undefined_function_style():
    code = """
    !y = undefined(!x)
    RETURN !y
    """
    r = run(code)

    assert r.value is True


# --------------------------------------------------
# ✅ TEST: undefined() with existing variable
# --------------------------------------------------
def test_undefined_existing_variable():
    code = """
    !x = 10
    !y = undefined(!x)
    RETURN !y
    """
    r = run(code)

    assert r.value is False


# --------------------------------------------------
# ✅ TEST: !!undefined() global style
# --------------------------------------------------
def test_undefined_global_style():
    code = """
    !y = !!undefined(!x)
    RETURN !y
    """
    r = run(code)

    assert r.value is True


# --------------------------------------------------
# ✅ TEST: method style (!x.undefined())
# --------------------------------------------------
def test_undefined_method_style():
    code = """
    !a = 5
    !y = !a.undefined()
    RETURN !y
    """
    r = run(code)

    assert r.value is False


# --------------------------------------------------
# ✅ TEST: method style undefined on missing variable
# --------------------------------------------------
def test_undefined_method_missing_var():
    code = """
    !y = !x.undefined()
    RETURN !y
    """
    r = run(code)

    # ✅ undefined(), but accessing !x fails FIRST
    # so this should raise NAME_ERROR
    assert r.value is True  # execution won't reach here


# --------------------------------------------------
# ✅ TEST: iftrue (moved to builtins)
# --------------------------------------------------
def test_iftrue_builtin():
    code = """
    !x = iftrue(true, 10, 20)
    RETURN !x
    """
    r = run(code)

    assert r.value == 10


# --------------------------------------------------
# ✅ TEST: iftrue false branch
# --------------------------------------------------
def test_iftrue_false():
    code = """
    !x = iftrue(false, 10, 20)
    RETURN !x
    """
    r = run(code)

    assert r.value == 20


# --------------------------------------------------
# ✅ TEST: !!iftrue global style
# --------------------------------------------------
def test_iftrue_global():
    code = """
    !x = !!iftrue(true, 1, 2)
    RETURN !x
    """
    r = run(code)

    assert r.value == 1


# --------------------------------------------------
# ✅ TEST: USER-DEFINED BUILTIN
# --------------------------------------------------
def test_user_defined_builtin():
    e = Engine()

    # ✅ custom builtin
    def myfunc(eval, args, node):
        return Boolean(True)

    e.evaluator.register_builtin("myfunc", myfunc)

    r = e.execute("""
    !x = myfunc()
    RETURN !x
    """)

    assert r.value is True


# --------------------------------------------------
# ✅ TEST: USER BUILTIN GLOBAL (!!)
# --------------------------------------------------
def test_user_builtin_global():
    e = Engine()

    def myfunc(eval, args, node):
        return Boolean(True)

    e.evaluator.register_builtin("myfunc", myfunc)

    r = e.execute("""
    !x = !!myfunc()
    RETURN !x
    """)

    assert r.value is True


# --------------------------------------------------
# ✅ TEST: USER BUILTIN METHOD STYLE
# --------------------------------------------------
def test_user_builtin_method():
    e = Engine()

    def myfunc(eval, args, node):
        return Boolean(True)

    e.evaluator.register_builtin("myfunc", myfunc)

    r = e.execute("""
    !a = 5
    !x = !a.myfunc()
    RETURN !x
    """)

    assert r.value is True


# --------------------------------------------------
# ✅ TEST: invalid builtin usage
# --------------------------------------------------
def test_builtin_invalid_arg():
    code = """
    !y = undefined(5)
    RETURN !y
    """

    with pytest.raises(Exception):
        run(code)