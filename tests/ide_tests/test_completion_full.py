from pydbml.ide.completion_engine import get_completions
from pydbml.core.engine import Engine


# =========================================================
# ✅ HELPER
# =========================================================
def run_completion(code: str, cursor_pos: int):
    engine = Engine()
    return get_completions(code, cursor_pos, evaluator=engine.evaluator)


# =========================================================
# ✅ SINGLE BANG (! variables)
# =========================================================
def test_single_bang_variables():
    code = """!x = 5
!y = 10
!z = !"""

    result = run_completion(code, len(code))

    assert "x" in result
    assert "y" in result
    assert "z" in result


# =========================================================
# ✅ DOUBLE BANG (!! globals/functions/objects)
# =========================================================
def test_double_bang_symbols():
    code = """!!a = 5
!!b = object ob()
!!func = 10
!!"""

    result = run_completion(code, len(code))

    assert "a" in result
    assert "b" in result
    assert "func" in result


# =========================================================
# ✅ DOT COMPLETION – NUMBER
# =========================================================
def test_number_methods():
    code = """!x = 5
!x."""

    result = run_completion(code, len(code))

    assert isinstance(result, list)
    assert len(result) > 0   # real methods should exist


# =========================================================
# ✅ DOT COMPLETION – STRING
# =========================================================
def test_string_methods():
    code = """!x = "hello"
!x."""

    result = run_completion(code, len(code))

    assert isinstance(result, list)
    assert len(result) > 0


# =========================================================
# ✅ DOT COMPLETION – OBJECT
# =========================================================
def test_object_methods():
    code = """!x = object ob()
!x."""

    result = run_completion(code, len(code))

    assert isinstance(result, list)
    assert len(result) > 0


# =========================================================
# ✅ MIXED VARIABLES + TYPES
# =========================================================
def test_mixed_types():
    code = """!x = 5
!y = "hi"
!z = object ob()
!"""

    result = run_completion(code, len(code))

    assert "x" in result
    assert "y" in result
    assert "z" in result


# =========================================================
# ✅ FALLBACK PARSER (INVALID CODE)
# =========================================================
def test_incomplete_code():
    code = """!x = 5
!y = 10
!z = !"""

    result = run_completion(code, len(code))

    assert "x" in result
    assert "y" in result


# =========================================================
# ✅ DOT CONTEXT DETECTION
# =========================================================
def test_dot_context():
    code = """!x = 5
!x."""

    result = run_completion(code, len(code))

    assert isinstance(result, list)


# =========================================================
# ✅ UNKNOWN VARIABLE AFTER DOT
# =========================================================
def test_unknown_variable_dot():
    code = """!x = 5
!unknown."""

    result = run_completion(code, len(code))

    assert result == []


# =========================================================
# ✅ SAFE EXTRACTOR TYPES
# =========================================================
def test_safe_type_inference():
    code = """!x = 5
!y = "test"
!z = object ob()
!x."""

    result = run_completion(code, len(code))

    assert isinstance(result, list)
    assert len(result) > 0


# =========================================================
# ✅ MULTI-LINE CONTEXT
# =========================================================
def test_multiline_completion():
    code = """!a = 1
!b = 2

!c = !"""

    result = run_completion(code, len(code))

    assert "a" in result
    assert "b" in result
    assert "c" in result


# =========================================================
# ✅ EMPTY INPUT
# =========================================================
def test_empty_input():
    code = ""

    result = run_completion(code, 0)

    assert result == []


# =========================================================
# ✅ RANDOM TEXT (ROBUSTNESS)
# =========================================================
def test_random_text():
    code = "random invalid text !!! ###"

    result = run_completion(code, len(code))

    assert isinstance(result, list)