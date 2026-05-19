import builtins
from pydbml.core.engine import Engine


def run_with_debug_input(engine, code, inputs):
    input_iter = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(input_iter)
        except StopIteration:
            return "n"  # default continue

    original_input = builtins.input
    builtins.input = fake_input

    try:
        return engine.execute(code)
    finally:
        builtins.input = original_input


def test_step_over_basic():
    code = """define FUNCtion !!add(!a is real, !b is real) is real
    RETURN !a + !b
ENDfunction

!x = 10
!y = 20

!z = !!add(!x, !y)
!w = !z + 5
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = ["s", "n", "p z", "c"]

    run_with_debug_input(engine, code, inputs)

    result = engine.env.get("w").get()
    assert result.value == 35


def test_step_over_nested():
    code = """define FUNCtion !!add(!a is real, !b is real) is real
    RETURN !a + !b
ENDfunction

define FUNCtion !!double(!x is real) is real
    RETURN !!add(!x, !x)
ENDfunction

!x = 5
!y = !!double(!x)
!z = !y + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = ["s", "n", "p y", "c"]

    run_with_debug_input(engine, code, inputs)

    result = engine.env.get("z").get()
    assert result.value == 11
