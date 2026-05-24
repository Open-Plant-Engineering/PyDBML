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
# ✅ CONDITIONAL BREAKPOINT BASIC
# =========================================================
def test_conditional_breakpoint_basic():
    code = """!x = 1
!x = !x + 1
!x = !x + 1
!x = !x + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = False

    inputs = [
        "b 3 if !x == 2",
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for l in logs:
        print(l)

    result = engine.env.get("x").get()
    assert result.value == 4


# =========================================================
# ✅ BREAKPOINT WITHOUT CONDITION
# =========================================================
def test_simple_breakpoint():
    code = """!x = 1
!x = !x + 1
!x = !x + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = False

    inputs = [
        "b 2",
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for l in logs:
        print(l)

    result = engine.env.get("x").get()
    assert result.value == 3


# =========================================================
# ✅ CONDITION FALSE → SHOULD NOT BREAK
# =========================================================
def test_condition_false():
    code = """!x = 1
!x = !x + 1
!x = !x + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = False

    inputs = [
        "b 3 if !x == 100",
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    # Should not pause at line 3
    for l in logs:
        print(l)

    result = engine.env.get("x").get()
    assert result.value == 3


# =========================================================
# ✅ MULTIPLE BREAKPOINTS
# =========================================================
def test_multiple_breakpoints():
    code = """!x = 1
!x = !x + 1
!x = !x + 1
!x = !x + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = False

    inputs = [
        "b 2",
        "b 4 if !x == 3",
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for l in logs:
        print(l)

    result = engine.env.get("x").get()
    assert result.value == 4


# =========================================================
# ✅ REMOVE BREAKPOINT
# =========================================================
def test_remove_breakpoint():
    code = """!x = 1
!x = !x + 1
!x = !x + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = False

    inputs = [
        "b 2",
        "rb 2",
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for l in logs:
        print(l)

    result = engine.env.get("x").get()
    assert result.value == 3
