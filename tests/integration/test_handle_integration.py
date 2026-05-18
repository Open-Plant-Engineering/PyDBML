import os
from pydbml.core.engine import Engine
from pydbml.execution.ast_evaluator import PyDBMLError


# ✅ helper: simulate failure by monkey patch
def inject_fail(engine):

    original_eval = engine.evaluator.evaluate

    def fail_wrapper(node):
        # simulate failure when object fail is used
        if hasattr(node, "type_name") and node.type_name == "fail":
            raise PyDBMLError(41, 8)
        return original_eval(node)

    engine.evaluator.evaluate = fail_wrapper


# ✅ 1. HANDLE with specific condition
def test_handle_specific_condition():
    e = Engine()
    inject_fail(e)

    code = """
    !x = object fail()

    HANDLE (41, 8)
        RETURN 100
    ELSEHANDLE ANY
        RETURN 200
    ENDHANDLE
    """

    r = e.execute(code)

    assert r.value == 100


# ✅ 2. HANDLE fallback ANY
def test_handle_any_fallback():
    e = Engine()
    inject_fail(e)

    code = """
    !x = object fail()

    HANDLE (99, 1)
        RETURN 100
    ELSEHANDLE ANY
        RETURN 200
    ENDHANDLE
    """

    r = e.execute(code)

    assert r.value == 200


# ✅ 3. HANDLE success case (ELSEHANDLE NONE)
def test_handle_success_case():
    e = Engine()

    code = """
    !x = 10

    HANDLE (41, 8)
        RETURN 100
    ELSEHANDLE ANY
        RETURN 200
    ELSEHANDLE NONE
        RETURN 300
    ENDHANDLE
    """

    r = e.execute(code)

    assert r.value == 300


# ✅ 4. HANDLE inside DO loop
def test_handle_inside_loop():
    e = Engine()
    inject_fail(e)

    code = """
    DO !i FROM 1 TO 5
        !x = object fail()

        HANDLE (41, 8)
            RETURN 500
        ELSEHANDLE ANY
            RETURN 999
        ENDHANDLE
    ENDDO

    RETURN 0
    """

    r = e.execute(code)

    # ✅ should exit early due to RETURN inside HANDLE
    assert r.value == 500


# ✅ 5. HANDLE inside IF condition
def test_handle_inside_if():
    e = Engine()
    inject_fail(e)

    code = """
    IF (true) THEN

        !x = object fail()

        HANDLE (41, 8)
            RETURN 700
        ELSEHANDLE ANY
            RETURN 800
        ENDHANDLE

    ENDIF

    RETURN 0
    """

    r = e.execute(code)

    assert r.value == 700


# ✅ 6. Multiple ELSEHANDLE with priority
def test_handle_multiple_conditions():
    e = Engine()
    inject_fail(e)

    code = """
    !x = object fail()

    HANDLE (10, 1)
        RETURN 10
    ELSEHANDLE (41, 8)
        RETURN 20
    ELSEHANDLE ANY
        RETURN 30
    ENDHANDLE
    """

