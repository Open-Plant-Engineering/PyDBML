from pydbml.core.engine import Engine


# =========================================================
# ✅ HELPER
# =========================================================
def run_debug(engine, code, commands):
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True
    engine.evaluator.interactive_mode = False

    engine.evaluator.debug_controller.add_commands(commands)
    engine.execute(code)

    return engine


# =========================================================
# ✅ BASIC STATE CAPTURE
# =========================================================
def test_state_basic():
    code = """!x = 5
!y = 10
!z = !x + !y
"""

    engine = run_debug(
        Engine(),
        code,
        ["s", "c"]
    )

    state = engine.evaluator.debug_controller.last_state

    assert state is not None
    assert state["node"] is not None
    assert "locals" in state


# =========================================================
# ✅ LINE + NODE VALIDATION
# =========================================================
def test_state_line_and_node():
    code = """!x = 1
!x = !x + 1
"""

    engine = run_debug(
        Engine(),
        code,
        ["s"]
    )

    state = engine.evaluator.debug_controller.last_state

    assert state["line"] is not None
    assert state["node"] in ("AssignNode", "BinaryOpNode", "NumberNode")


# =========================================================
# ✅ LOCAL VARIABLES TRACKING
# =========================================================
def test_state_locals():
    code = """!x = 2
!y = 3
!z = !x + !y
"""

    engine = run_debug(
        Engine(),
        code,
        ["s", "s"]
    )

    state = engine.evaluator.debug_controller.last_state

    assert "x" in state["locals"] or "y" in state["locals"]


# =========================================================
# ✅ GLOBAL VARIABLES TRACKING
# =========================================================
def test_state_globals():
    code = """!!g = 10
"""

    engine = run_debug(
        Engine(),
        code,
        ["s", "s"]
    )

    state = engine.evaluator.debug_controller.last_state

    assert isinstance(state["globals"], dict)


# =========================================================
# ✅ WATCH VARIABLES
# =========================================================
def test_state_watch():
    code = """!x = 5
!x = !x + 1
"""

    engine = run_debug(
        Engine(),
        code,
        [
            "watch x",
            "s",
            "s",
            "c"
        ]
    )

    state = engine.evaluator.debug_controller.last_state

    assert "x" in state["watch"]
    assert state["watch"]["x"] is not None


# =========================================================
# ✅ STACK TRACE
# =========================================================
def test_state_stack():
    code = """!x = 1
!x = !x + 1
"""

    engine = run_debug(
        Engine(),
        code,
        ["s"]
    )

    state = engine.evaluator.debug_controller.last_state

    assert isinstance(state["stack"], list)
    assert len(state["stack"]) > 0

    first_frame = state["stack"][0]
    assert "node" in first_frame
    assert "line" in first_frame


# =========================================================
# ✅ DEPTH VALIDATION
# =========================================================
def test_state_depth():
    code = """!x = 1
!x = !x + 1
"""

    engine = run_debug(
        Engine(),
        code,
        ["s", "s"]
    )

    state = engine.evaluator.debug_controller.last_state

    assert state["depth"] >= 1


# =========================================================
# ✅ MULTI-STEP SNAPSHOT UPDATE
# =========================================================
def test_state_updates_over_steps():
    code = """!x = 1
!x = !x + 1
!x = !x + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True
    engine.evaluator.interactive_mode = False

    controller = engine.evaluator.debug_controller
    controller.add_commands(["s", "s", "s", "c"])

    engine.execute(code)

    state = controller.last_state

    assert state["locals"]["x"] in ("1.0", "2.0", "3.0", "4.0") # depends where pause happened
