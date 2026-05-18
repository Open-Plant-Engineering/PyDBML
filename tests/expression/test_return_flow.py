from pydbml.core.engine import Engine

def test_return_inside_if():
    e = Engine()

    code = """
DEFINE FUNCTION !!f(!x IS REAL) IS REAL
    IF (!x > 5) THEN
        RETURN 100
    ENDIF

    RETURN 1
ENDFUNCTION
"""

    e.execute(code)

    r1 = e.execute("!!f(10)")
    r2 = e.execute("!!f(2)")

    assert r1.value == 100
    assert r2.value == 1

def test_return_inside_do_loop():
    e = Engine()

    code = """
DEFINE FUNCTION !!f() IS REAL
    DO !i FROM 1 TO 5
        IF (!i == 3) THEN
            RETURN !i
        ENDIF
    ENDDO

    RETURN 0
ENDFUNCTION
"""

    e.execute(code)

    r = e.execute("!!f()")

    assert r.value == 3

def test_return_nested_if_loop():
    e = Engine()

    code = """
DEFINE FUNCTION !!f() IS REAL
    DO !i FROM 1 TO 5
        IF (!i == 4) THEN
            RETURN 40
        ENDIF
    ENDDO

    RETURN 0
ENDFUNCTION
"""

    e.execute(code)

    r = e.execute("!!f()")

    assert r.value == 40

def test_return_inside_method():
    e = Engine()

    code = """
DEFINE OBJECT test
    member.val IS REAL
ENDOBJECT

DEFINE METHOD .test()
    RETURN 55
ENDMETHOD
"""

    e.execute(code)

    e.execute("!x = object test()")
    r = e.execute("!x.test()")

    assert r.value == 55

def test_return_breaks_loop():
    e = Engine()

    code = """
DEFINE FUNCTION !!f() IS REAL
    !count = 0

    DO !i FROM 1 TO 10
        !count = !count + 1

        IF (!i == 2) THEN
            RETURN !count
        ENDIF
    ENDDO

    RETURN -1
ENDFUNCTION
"""

    e.execute(code)

    r = e.execute("!!f()")

    # loop should stop at i = 2 → count = 2
    assert r.value == 2

