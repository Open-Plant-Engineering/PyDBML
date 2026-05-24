from pydbml.core.engine import Engine


# =========================================================
# BASIC LOOP BEHAVIOR
# =========================================================

def test_do_loop_basic_break():
    engine = Engine()

    engine.execute("""
    !x = 1
    do
      break if(!x > 5)
      !x = !x + 1
    enddo
    """)

    result = engine.execute("!x")
    assert result.value == 6


def test_do_loop_break_statement():
    engine = Engine()

    engine.execute("""
    !x = 1
    do
      !x = !x + 1
      break
      !x = 100
    enddo
    """)

    result = engine.execute("!x")
    assert result.value == 2


def test_do_loop_without_break_guard():
    engine = Engine()

    engine.execute("""
    !x = 1
    do
      break if(!x > 3)
      !x = !x + 1
    enddo
    """)

    result = engine.execute("!x")
    assert result.value == 4


# =========================================================
# IF INSIDE LOOP
# =========================================================

def test_do_loop_with_if_inside():
    engine = Engine()

    engine.execute("""
    !x = 1
    do
      if(!x == 3) then
        break
      endif
      !x = !x + 1
    enddo
    """)

    result = engine.execute("!x")
    assert result.value == 3


# =========================================================
# NESTED LOOPS
# =========================================================

def test_nested_do_loop():
    engine = Engine()

    engine.execute("""
    !outer = 0

    do
      !inner = 0

      do
        !inner = !inner + 1
        break if(!inner > 2)
      enddo

      !outer = !outer + 1
      break if(!outer > 2)
    enddo
    """)

    result_outer = engine.execute("!outer")
    result_inner = engine.execute("!inner")

    assert result_outer.value == 3
    assert result_inner.value == 3


# =========================================================
# COMMENT SUPPORT (CRITICAL)
# =========================================================

def test_single_line_comment():
    engine = Engine()

    engine.execute("""
    !x = 1
    -- increment once
    !x = !x + 1
    """)

    result = engine.execute("!x")
    assert result.value == 2


def test_inline_comment():
    engine = Engine()

    engine.execute("!x = 5 -- ignored comment")

    result = engine.execute("!x")
    assert result.value == 5


def test_multiline_comment_block():
    engine = Engine()

    engine.execute("""
    !x = 1

    $(
      !x = 100
      !x = 200
    $)

    !x = !x + 1
    """)

    result = engine.execute("!x")
    assert result.value == 2


# =========================================================
# COMMENTS INSIDE LOOP
# =========================================================

def test_comment_inside_loop():
    engine = Engine()

    engine.execute("""
    !x = 1

    do
      -- increment value
      !x = !x + 1

      break if(!x > 3)
    enddo
    """)

    result = engine.execute("!x")
    assert result.value == 4


def test_multiline_comment_inside_loop():
    engine = Engine()

    engine.execute("""
    !x = 1

    do
      $(
        skipped block
      $)

      !x = !x + 1
      break if(!x > 2)
    enddo
    """)

    result = engine.execute("!x")
    assert result.value == 3