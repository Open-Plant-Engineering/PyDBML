from pydbml.ide.completion_engine import get_completions
from pydbml.core.engine import Engine


def run_hover(code, pos):
    engine = Engine()
    return get_completions(code, pos, evaluator=engine.evaluator)


# =========================================================
# ✅ VARIABLE HOVER
# =========================================================
def test_hover_variable():
    code = """!x = 5
!x"""

    result = run_hover(code, len(code))

    assert isinstance(result, dict)
    assert result["kind"] == "variable"
    assert result["type"] == "number"


# =========================================================
# ✅ STRING VARIABLE
# =========================================================
def test_hover_string():
    code = """!x = "hello"
!x"""

    result = run_hover(code, len(code))

    assert result["type"] == "string"


# =========================================================
# ✅ OBJECT VARIABLE
# =========================================================
def test_hover_object():
    code = """!x = object ob()
!x"""

    result = run_hover(code, len(code))

    assert result["type"] == "object"


# =========================================================
# ✅ METHOD HOVER
# =========================================================
def test_hover_method():
    code = """!x = 5
!x.add"""

    result = run_hover(code, len(code))

    assert isinstance(result, dict)
    assert result["kind"] == "method"
    assert "params" in result


# =========================================================
# ✅ INVALID TOKEN
# =========================================================
def test_hover_invalid():
    code = "random text"

    result = run_hover(code, len(code))

    assert result == []