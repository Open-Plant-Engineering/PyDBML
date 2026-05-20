from pydbml.ide.completion_engine import get_completions


def test_single_bang():
    code = """!x = 5
!y = 10
!z = !"""

    result = get_completions(code, len(code))

    assert "x" in result
    assert "y" in result


def test_double_bang():
    code = """!!func1 = 5
!!func2 = 10
!!"""

    result = get_completions(code, len(code))

    assert "func1" in result
    assert "func2" in result


def test_dot_context():
    code = """!x = 5
!x."""

    result = get_completions(code, len(code))

    assert "add" in result or "length" in result