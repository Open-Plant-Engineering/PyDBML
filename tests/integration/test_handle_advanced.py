import pytest
from pydbml.core.engine import Engine
from pydbml.runtime.exceptions import PyDBMLError


# ✅ helper: simulate failure
def inject_fail(engine):

    original_eval = engine.evaluator.evaluate

    def fail_wrapper(node):
        if hasattr(node, "type_name") and node.type_name == "fail":
            raise PyDBMLError(41, 8)
        return original_eval(node)

    engine.evaluator.evaluate = fail_wrapper


def run(code: str, inject: bool = True):
    engine = Engine()
    if inject:
        inject_fail(engine)
    engine.execute(code)
    return engine


# --------------------------------------------------
# ✅ HANDLE ANY (fixed)
# --------------------------------------------------

def test_handle_any_basic():
    code = """
!tmp = object fail()

HANDLE ANY
    !x = 999
ENDHANDLE
"""
    engine = run(code)
    assert engine.env.get("x").get().value == 999


# --------------------------------------------------
# ✅ HANDLE ANY should not run without error
# --------------------------------------------------

def test_handle_any_no_error():
    code = """
!x = 5

HANDLE ANY
    !x = 999
ENDHANDLE
"""
    engine = run(code, inject=False)
    assert engine.env.get("x").get().value == 5


# --------------------------------------------------
# ✅ HANDLE exact match
# --------------------------------------------------

def test_handle_exact_match():
    code = """
!tmp = object fail()

HANDLE (41, 8)
    !x = 111
ENDHANDLE
"""
    engine = run(code)
    assert engine.env.get("x").get().value == 111


# --------------------------------------------------
# ✅ HANDLE partial match
# --------------------------------------------------

def test_handle_single_code():
    code = """
!tmp = object fail()

HANDLE ( 41 , )
    !x = 222
ENDHANDLE
"""
    engine = run(code)
    assert engine.env.get("x").get().value == 222


# --------------------------------------------------
# ✅ ELSEHANDLE ANY fallback
# --------------------------------------------------

def test_handle_else_any():
    code = """
!tmp = object fail()

HANDLE (99, 9)
    !x = 100
ELSEHANDLE ANY
    !x = 200
ENDHANDLE
"""
    engine = run(code)
    assert engine.env.get("x").get().value == 200


# --------------------------------------------------
# ✅ HANDLE ANY priority
# --------------------------------------------------

def test_handle_any_priority():
    code = """
!tmp = object fail()

HANDLE ANY
    !x = 300
ELSEHANDLE (41, 8)
    !x = 400
ENDHANDLE
"""
    engine = run(code)
    assert engine.env.get("x").get().value == 300


# --------------------------------------------------
# ✅ ELSEHANDLE NONE
# --------------------------------------------------

def test_handle_none_on_success():
    code = """
!x = 0

HANDLE (41, 8)
    !x = 111
ELSEHANDLE NONE
    !x = 222
ENDHANDLE
"""
    engine = run(code, inject=False)
    assert engine.env.get("x").get().value == 222


# --------------------------------------------------
# ✅ Nested HANDLE
# --------------------------------------------------

def test_nested_handle_any():
    code = """
!tmp = object fail()

HANDLE ANY
    !tmp = object fail()
    HANDLE ANY
        !x = 555
    ENDHANDLE
ENDHANDLE
"""
    engine = run(code)
    assert engine.env.get("x").get().value == 555


# --------------------------------------------------
# ✅ No handler match → should fail
# --------------------------------------------------

def test_handle_no_match_should_fail():
    code = """
!tmp = object fail()

HANDLE (99, 9)
    !x = 100
ENDHANDLE
"""
    with pytest.raises(PyDBMLError):
        run(code)


# --------------------------------------------------
# ✅ Priority order
# --------------------------------------------------

def test_handle_priority_order():
    code = """
!tmp = object fail()

HANDLE ( 41 , )
    !x = 1
ELSEHANDLE ( 41 , 8 )
    !x = 2
ELSEHANDLE ANY
    !x = 3
ENDHANDLE
"""
    engine = run(code)
    assert engine.env.get("x").get().value == 1


# --------------------------------------------------
# ✅ ELSEHANDLE chain
# --------------------------------------------------

def test_multiple_elsehandle_chain():
    code = """
!tmp = object fail()

HANDLE ( 99 , )
    !x = 10
ELSEHANDLE ( 98 , )
    !x = 20
ELSEHANDLE ANY
    !x = 30
ENDHANDLE
"""
    engine = run(code)
    assert engine.env.get("x").get().value == 30