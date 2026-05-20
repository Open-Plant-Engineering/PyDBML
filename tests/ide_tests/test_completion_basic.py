from pydbml.ide.completion_engine import get_completions


def test_variable_completion():
    code = """!x = 5
!y = 10
!z = !"""

    result = get_completions(code, len(code))

    assert "x" in result
    assert "y" in result
    assert "z" in result