import pytest
from pydbml.core.engine import Engine


# --------------------------
# ✅ BASIC ELSEIF MATCH
# --------------------------
def test_elseif_basic():
    e = Engine()

    code = """
    !x = 0

    if (5 == 3) then
        !x = 1
    elseif (5 == 4) then
        !x = 2
    elseif (5 == 5) then
        !x = 3
    else
        !x = 4
    endif
    """

    e.execute(code)

    result = e.env.get("x").get()
    assert result.value == 3.0


# --------------------------
# ✅ FIRST IF MATCH
# --------------------------
def test_elseif_first_if():
    e = Engine()

    code = """
    !x = 0

    if (5 == 5) then
        !x = 10
    elseif (5 == 5) then
        !x = 20
    else
        !x = 30
    endif
    """

    e.execute(code)

    result = e.env.get("x").get()
    assert result.value == 10.0


# --------------------------
# ✅ ELSE FALLBACK
# --------------------------
def test_elseif_else_fallback():
    e = Engine()

    code = """
    !x = 0

    if (1 == 2) then
        !x = 10
    elseif (2 == 3) then
        !x = 20
    else
        !x = 99
    endif
    """

    e.execute(code)

    result = e.env.get("x").get()
    assert result.value == 99.0


# --------------------------
# ✅ MULTIPLE ELSEIF ORDER
# --------------------------
def test_elseif_multiple_order():
    e = Engine()

    code = """
    !x = 0

    if (false) then
        !x = 1
    elseif (false) then
        !x = 2
    elseif (true) then
        !x = 3
    elseif (true) then
        !x = 4
    endif
    """

    e.execute(code)

    result = e.env.get("x").get()
    assert result.value == 3.0


# --------------------------
# ✅ ELSEIF WITHOUT ELSE
# --------------------------
def test_elseif_without_else():
    e = Engine()

    code = """
    !x = 0

    if (false) then
        !x = 1
    elseif (true) then
        !x = 42
    endif
    """

    e.execute(code)

    result = e.env.get("x").get()
    assert result.value == 42.0


# --------------------------
# ✅ TYPE ERROR IN ELSEIF
# --------------------------
def test_elseif_type_error():
    from pydbml.runtime.exceptions import PyDBMLError

    e = Engine()

    code = """
    if (false) then
        !x = 1
    elseif (5) then
        !x = 2
    endif
    """

    with pytest.raises(PyDBMLError) as err:
        e.execute(code)

    assert "BOOLEAN" in str(err.value)


# --------------------------
# ✅ ELSEIF WITH RETURN (integration)
# --------------------------
def test_elseif_with_return():
    e = Engine()

    code = """
    define function !!test() is real

        if (false) then
            return 1
        elseif (false) then
            return 2
        elseif (true) then
            return 3
        endif

        return 0
    endfunction

    !!test()
    """

    result = e.execute(code)

    assert result.value == 3.0
