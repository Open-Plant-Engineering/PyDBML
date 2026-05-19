from pydbml.core.engine import Engine

def test_breakpoint_manual():
    e = Engine()

    e.evaluator.debug_mode = True

    # ✅ breakpoint on line 2
    e.evaluator.add_breakpoint(2)

    print("\n--- BREAKPOINT TEST ---")

    e.execute("""
    !x = 10
    !y = !x + 5
    !z = !y + 2
    """)
