from pydbml.core.engine import Engine


# =========================================================
# ✅ HELPER (NEW STYLE - NO input mocking)
# =========================================================
def run_debug(engine, code, commands):
    engine.evaluator.interactive_mode = False
    engine.evaluator.debug_controller.add_commands(commands)
    engine.execute(code)
    return engine.evaluator.debug_log


# =========================================================
# ✅ STEP MODE (s)
# =========================================================
def test_step_commands():
    code = """!x = 1
!y = 2
!z = !x + !y
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    logs = run_debug(engine, code, [
        "s", "s", "s", "c"
    ])

    for l in logs:
        print(l)

    assert any("[STEP]" in l for l in logs)
    assert engine.env.get("z").get().value == 3


# =========================================================
# ✅ STEP OVER (n)
# =========================================================
def test_step_over():
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

    logs = run_debug(engine, code, [
        "n", "c"
    ])

    for l in logs:
        print(l)

    assert engine.env.get("c").get().value == 7


# =========================================================
# ✅ STEP OUT (o)
# =========================================================
def test_step_out():
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

    logs = run_debug(engine, code, [
        "s", "s", "o", "c"
    ])

    for l in logs:
        print(l)

    assert engine.env.get("c").get().value == 7


# =========================================================
# ✅ WATCH VARIABLES
# =========================================================
def test_watch_variables():
    code = """!x = 5
!y = 10
!z = !x + !y
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    logs = run_debug(engine, code, [
        "watch x",
        "watch z",
        "s", "s", "s", "c"
    ])

    for l in logs:
        print(l)

    # ensure watch logs exist
    assert any("[WATCH] x" in l for l in logs)
    assert engine.env.get("z").get().value == 15


# =========================================================
# ✅ CONDITIONAL BREAKPOINT (non-interactive)
# =========================================================
def test_conditional_breakpoint():
    code = """!x = 1
!x = !x + 1
!x = !x + 1
!x = !x + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    logs = run_debug(engine, code, [
        "b 3 if !x == 2",
        "c"
    ])

    for l in logs:
        print(l)

    assert any("[BREAKPOINT]" in l for l in logs)
    assert engine.env.get("x").get().value == 4


# =========================================================
# ✅ MULTIPLE COMMAND FLOW
# =========================================================
def test_mixed_commands():
    code = """!x = 2
!y = 3
!z = !x + !y
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    logs = run_debug(engine, code, [
        "watch x",
        "s",
        "p x",
        "n",
        "c"
    ])

    for l in logs:
        print(l)

    assert engine.env.get("z").get().value == 5


# =========================================================
# ✅ NO COMMANDS (fallback behavior)
# =========================================================
def test_no_commands():
    code = """!x = 5
!y = !x + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = False

    logs = run_debug(engine, code, [])

    for l in logs:
        print(l)

    assert engine.env.get("y").get().value == 6