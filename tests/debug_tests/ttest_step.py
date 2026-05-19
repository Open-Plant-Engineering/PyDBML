from pydbml.core.engine import Engine

def test_step_mode():
    e = Engine()

    e.evaluator.debug_mode = True
    e.evaluator.step_mode = True

    print("\n--- STEP MODE TEST ---")

    e.execute("""
    !x = 10
    !y = !x + 5
    """)
