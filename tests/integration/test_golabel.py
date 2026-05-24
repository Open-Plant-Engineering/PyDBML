from pydbml.core.engine import Engine
from pydbml.runtime.exceptions import PyDBMLError

# ✅ 1. Basic forward jump
def test_basic_golabel():
    e = Engine()

    code = """
    !x = 1

    golabel /end

    !x = 2

    label /end
    return !x
    """

    r = e.execute(code)
    assert r.value == 1


# ✅ 2. Inside loop → outside jump (YOUR MAIN USE CASE)
def test_golabel_exit_loop():
    e = Engine()

    code = """
    !x = object array()
    !x[1] = 5
    !x[3] = 6
    !x[4] = 8

    do !i indices !x
        if (!i.eq(3)) then
            golabel /end
        endif
    enddo

    label /end
    return 10
    """

    r = e.execute(code)
    assert r.value == 10


# ✅ 3. Backward jump (loop using golabel)
def test_golabel_backward_loop():
    e = Engine()

    code = """
    !x = 0

    label /start

    !x = !x + 1

    if (!x.lt(5)) then
        golabel /start
    endif

    return !x
    """

    r = e.execute(code)
    assert r.value == 5


# ❌ 4. Invalid: jumping INTO inner block
def test_golabel_invalid_into_block():
    e = Engine()

    code = """
    if (true) then
        label /inner
    endif

    golabel /inner
    """

    try:
        e.execute(code)
    except Exception:
        assert True
    else:
        assert False  # must fail


# ❌ 5. Duplicate labels
def test_duplicate_label():
    e = Engine()

    code = """
    label /A
    label /A
    """

    try:
        e.execute(code)
    except Exception:
        assert True
    else:
        assert False


# ❌ 6. Missing label
def test_missing_label():
    e = Engine()

    code = """
    golabel /doesnotexist
    """

    try:
        e.execute(code)
    except Exception:
        assert True
    else:
        assert False


# ✅ 7. Golabel inside IF block
def test_golabel_inside_if():
    e = Engine()

    code = """
    !x = 1

    if (true) then
        golabel /end
    endif

    !x = 2

    label /end
    return !x
    """

    r = e.execute(code)
    assert r.value == 1


# ✅ 8. Golabel inside HANDLE block
def test_golabel_inside_handle():
    e = Engine()

    code = """
    !x = 0

    handle (41, 8)
        golabel /end
    elsehandle any
        !x = 100
    endhandle

    label /end
    return 50
    """

    r = e.execute(code)
    assert r.value == 50

def test_golabel_keyword_name_not_allowed():
    e = Engine()

    code = """
    golabel /skip
    """

    try:
        e.execute(code)
    except SyntaxError:
        assert True
    else:
        assert False  # should fail

def test_label_keyword_name_not_allowed():
    e = Engine()

    code = """
    label /if
    """

    try:
        e.execute(code)
    except PyDBMLError as err:
        assert "Invalid label name" in str(err)
        return

    assert False, "Expected error"

import pytest

@pytest.mark.parametrize("kw", ["skip", "if", "then", "return", "handle", "do"])
def test_all_keywords_invalid(kw):
    e = Engine()

    code = f"""
    golabel /{kw}
    """

    try:
        e.execute(code)
    except SyntaxError:
        assert True
    else:
        assert False