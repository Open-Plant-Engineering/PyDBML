import builtins
from pydbml.core.engine import Engine


def run_with_debug_input(engine, code, inputs):
    input_iter = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(input_iter)
        except StopIteration:
            return "c"

    original_input = builtins.input
    builtins.input = fake_input

    try:
        engine.execute(code)
        return engine.evaluator.debug_log
    finally:
        builtins.input = original_input


# =========================================================
# ✅ BASIC WATCH TEST
# =========================================================
def test_watch_basic():
    code = """!x = 5
!y = 10
!z = !x + !y
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = [
        "watch x",
        "watch z",
        "s",
        "s",
        "s",
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for line in logs:
        print(line)

    result = engine.env.get("z").get()
    assert result.value == 15


# =========================================================
# ✅ WATCH + STEP OVER
# =========================================================
def test_watch_with_step_over():
    code = """define FUNCtion !!add(!a is real, !b is real) is real
    RETURN !a + !b
ENDfunction

!x = 2
!y = 3
!z = !!add(!x, !y)
!w = !z + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = [
        "watch z",
        "s",
        "n",   # step over function
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for line in logs:
        print(line)

    result = engine.env.get("w").get()
    assert result.value == 6


# =========================================================
# ✅ WATCH WITH STEP OUT
# =========================================================
def test_watch_with_step_out():
    code = """define FUNCtion !!inc(!x is real) is real
    RETURN !x + 1
ENDfunction

!a = 5
!b = !!inc(!a)
!c = !b + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = [
        "watch a",
        "watch b",
        "s",
        "s",
        "o",  # step out
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for line in logs:
        print(line)

    result = engine.env.get("c").get()
    assert result.value == 7


# =========================================================
# ✅ WATCH NESTED FUNCTIONS
# =========================================================
def test_watch_nested():
    code = """define FUNCtion !!inner(!x is real) is real
    RETURN !x + 1
ENDfunction

define FUNCtion !!outer(!x is real) is real
    RETURN !!inner(!x)
ENDfunction

!x = 4
!y = !!outer(!x)
!z = !y + 2
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = [
        "watch x",
        "watch y",
        "watch z",
        "s",
        "s",
        "s",
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for line in logs:
        print(line)

    result = engine.env.get("z").get()
    assert result.value == 7


# =========================================================
# ✅ WATCH ADD + REMOVE
# =========================================================
def test_watch_add_remove():
    code = """!x = 1
!y = 2
!z = !x + !y
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = [
        "watch x",
        "watch z",
        "unwatch x",
        "s",
        "s",
        "s",
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for line in logs:
        print(line)

    result = engine.env.get("z").get()
    assert result.value == 3


# =========================================================
# ✅ WATCH UNKNOWN VARIABLE
# =========================================================
def test_watch_unknown_variable():
    code = """!x = 5
!y = !x + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = [
        "watch z",  # not created yet
        "s",
        "s",
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for line in logs:
        print(line)

    result = engine.env.get("y").get()
    assert result.value == 6
