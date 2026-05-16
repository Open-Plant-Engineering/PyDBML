from pydbml.core.engine import Engine


# =========================================================
# BASIC COUNTING LOOPS
# =========================================================

def test_do_to():
    engine = Engine()

    engine.execute("""
    do !i to 5
      !last = !i
    enddo
    """)

    result = engine.execute("!last")
    assert result.value == 5


def test_do_from_to():
    engine = Engine()

    engine.execute("""
    do !i from 5 to 7
      !last = !i
    enddo
    """)

    result = engine.execute("!last")
    assert result.value == 7


def test_do_from_to_default_step():
    engine = Engine()

    engine.execute("""
    do !i from 1 to 3
      !sum = !sum + 1
    enddo
    """)

    result = engine.execute("!sum")
    assert result.value == 3


def test_do_by_step():
    engine = Engine()

    engine.execute("""
    do !i from 1 to 5 by 2
      !last = !i
    enddo
    """)

    result = engine.execute("!last")
    assert result.value == 5


# =========================================================
# REVERSE LOOP
# =========================================================

def test_do_reverse():
    engine = Engine()

    engine.execute("""
    do !i from 5 to 1 by -2
      !last = !i
    enddo
    """)

    result = engine.execute("!last")
    assert result.value == 1


# =========================================================
# BREAK SUPPORT
# =========================================================

def test_do_break_in_count_loop():
    engine = Engine()

    engine.execute("""
    do !i to 10
      break if(!i > 3)
      !last = !i
    enddo
    """)

    result = engine.execute("!last")
    assert result.value == 3


def test_do_break_direct():
    engine = Engine()

    engine.execute("""
    do !i to 10
      !last = !i
      break
    enddo
    """)

    result = engine.execute("!last")
    assert result.value == 1


# =========================================================
# IF INSIDE LOOP
# =========================================================

def test_if_inside_count_loop():
    engine = Engine()

    engine.execute("""
    do !i to 5
      if(!i == 3) then
        break
      endif
      !last = !i
    enddo
    """)

    result = engine.execute("!last")
    assert result.value == 2


# =========================================================
# NESTED LOOPS
# =========================================================

def test_nested_loops_with_counter():
    engine = Engine()

    engine.execute("""
    !outer = 0

    do !i to 3
      do !j to 2
        !inner = !j
      enddo
      !outer = !outer + 1
    enddo
    """)

    outer = engine.execute("!outer")
    inner = engine.execute("!inner")

    assert outer.value == 3
    assert inner.value == 2


# =========================================================
# INFINITE LOOP COMPATIBILITY
# =========================================================

def test_infinite_loop_with_break():
    engine = Engine()

    engine.execute("""
    !x = 1

    do
      !x = !x + 1
      break if(!x > 3)
    enddo
    """)

    result = engine.execute("!x")
    assert result.value == 4


# =========================================================
# NEGATIVE STEP EDGE CASES
# =========================================================

def test_negative_step_exact():
    engine = Engine()

    engine.execute("""
    do !i from 3 to 1 by -1
      !last = !i
    enddo
    """)

    result = engine.execute("!last")
    assert result.value == 1


def test_negative_step_skip():
    engine = Engine()

    engine.execute("""
    do !i from 5 to 1 by -2
      !last = !i
    enddo
    """)

    result = engine.execute("!last")
    assert result.value == 1
