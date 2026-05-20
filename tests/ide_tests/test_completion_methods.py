from pydbml.ide.completion_engine import get_completions


def test_object_methods():
    code = """!x = object ob()
!x."""

    result = get_completions(code, len(code))

    assert "get" in result
    assert "set" in result


def test_number_methods():
    code = """!x = 5
!x."""

    result = get_completions(code, len(code))

    assert "add" in result
    assert "sub" in result


def test_string_methods():
    code = """!x = "hello"
!x."""

    result = get_completions(code, len(code))

    assert "upper" in result
    assert "lower" in result
