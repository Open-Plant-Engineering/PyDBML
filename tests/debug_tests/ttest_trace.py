from pydbml.core.engine import Engine

def test_trace_output(capsys):
    e = Engine()

    # ✅ enable debugger
    e.evaluator.debug_mode = True

    e.execute("""
    !x = 10
    !y = !x + 5
    """)

    captured = capsys.readouterr().out

    assert "[STEP]" in captured
    assert "AssignNode" in captured
    assert "BinaryOpNode" in captured
