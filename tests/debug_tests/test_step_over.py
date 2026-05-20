import builtins
from pydbml.core.engine import Engine


def run_with_debug_input(engine, code, inputs):
    input_iter = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(input_iter)
        except StopIteration:
            return "c"

    import builtins
    original_input = builtins.input
    builtins.input = fake_input

    try:
        engine.execute(code)
        return engine.evaluator.debug_log   # ✅ RETURN LOGS
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

    logs = run_with_debug_input(engine, code, inputs)

    for l in logs:
        print(l)

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

def test_step_out_basic():
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
        "s",   # step to z assignment
        "s",   # enter function
        "o",   # step OUT ✅
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for l in logs:
        print(l)

    result = engine.env.get("w").get()
    assert result.value == 6

def test_step_out_nested():
    code = """define FUNCtion !!inner(!x is real) is real
    RETURN !x + 1
ENDfunction

define FUNCtion !!middle(!x is real) is real
    RETURN !!inner(!x)
ENDfunction

define FUNCtion !!outer(!x is real) is real
    RETURN !!middle(!x)
ENDfunction

!a = !!outer(5)
!b = !a + 2
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = [
        "s",  # enter outer
        "s",  # enter middle
        "s",  # enter inner
        "o",  # exit inner ✅
        "o",  # exit middle ✅
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for l in logs:
        print(l)

    result = engine.env.get("b").get()
    assert result.value == 8

def test_step_over_skips_function():
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
        "s",
        "n",  # step-over ✅
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for l in logs:
        print(l)

    result = engine.env.get("c").get()
    assert result.value == 7

def test_variable_visibility():
    code = """!x = 1
!y = 2
!z = !x + !y
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = [
        "p z",  # before z exists
        "s",
        "s",
        "p z",  # after assignment
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for l in logs:
        print(l)

    result = engine.env.get("z").get()
    assert result.value == 3

def test_mixed_debug_flow():
    code = """define FUNCtion !!double(!x is real) is real
    RETURN !x * 2
ENDfunction

!a = 3
!b = !!double(!a)
!c = !b + 5
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = [
        "p a",
        "s",
        "n",
        "p b",
        "o",  # step out if inside
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for l in logs:
        print(l)

    result = engine.env.get("c").get()
    assert result.value == 11

def test_step_out_at_top_level():
    code = """!x = 5
!y = !x + 1
"""

    engine = Engine()
    engine.evaluator.debug_mode = True
    engine.evaluator.step_mode = True

    inputs = [
        "o",  # step out at top level
        "c"
    ]

    logs = run_with_debug_input(engine, code, inputs)

    for l in logs:
        print(l)

    result = engine.env.get("y").get()
    assert result.value == 6

