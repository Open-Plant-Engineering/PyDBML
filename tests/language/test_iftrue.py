import pytest
from pydbml.core.engine import Engine
from pydbml.runtime.exceptions import PyDBMLError


# --------------------------
# ✅ BASIC TRUE CASE
# --------------------------
def test_iftrue_true_branch():
    e = Engine()

    code = """
    !x = iftrue(3 == 3, 3, 5)
    """

    e.execute(code)

    result = e.env.get("x").get()
    assert result.value == 3


# --------------------------
# ✅ BASIC FALSE CASE
# --------------------------
def test_iftrue_false_branch():
    e = Engine()

    code = """
    !x = iftrue(3 == 2, 3, 5)
    """

    e.execute(code)

    result = e.env.get("x").get()
    assert result.value == 5


# --------------------------
# ✅ NESTED IFTRUE
# --------------------------
def test_iftrue_nested():
    e = Engine()

    code = """
    !x = iftrue(3 == 3, iftrue(2 == 2, 10, 20), 5)
    """

    e.execute(code)

    result = e.env.get("x").get()
    assert result.value == 10


# --------------------------
# ✅ TYPE ERROR (condition not boolean)
# --------------------------
def test_iftrue_condition_type_error():
    e = Engine()

    code = """
    !x = iftrue(5, 3, 4)
    """

    with pytest.raises(PyDBMLError) as err:
        e.execute(code)

    assert "BOOLEAN" in str(err.value)


# --------------------------
# ✅ ARG COUNT ERROR
# --------------------------
def test_iftrue_arg_count_error():
    e = Engine()

    code = """
    !x = iftrue(3 == 3, 3)
    """

    with pytest.raises(PyDBMLError) as err:
        e.execute(code)

    assert "expects 3 arguments" in str(err.value)