from pydbml.core.engine import Engine

def test_debugger_full():
    e = Engine()

    e.evaluator.debug_mode = True
    e.evaluator.step_mode = True

    print("\n--- FULL DEBUGGER TEST ---")

    e.execute("""
    !x = 10
    !y = !x + 5
    """)