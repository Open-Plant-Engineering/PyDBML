from pydbml.ide.completion_engine import get_completions


def test_object_detection():
    code = """!x = object ob()
!y = 5
!z = !"""

    result = get_completions(code, len(code))

    assert "x" in result  # object variable
    assert "y" in result


def test_double_bang_all_symbols():
    code = """!!f1 = 1
!!f2 = object ob()
!!"""

    result = get_completions(code, len(code))

    assert "f1" in result
    assert "f2" in result