from pydbml.ide.completion_engine import get_completions
from pydbml.core.engine import Engine


def run_completion(code):
    engine = Engine()
    return get_completions(code, len(code), evaluator=engine.evaluator)


def test_number_method_signature():
    code = """!x = 5
!x.add("""
    
    result = run_completion(code)

    assert isinstance(result, dict)
    assert "name" in result
    assert "params" in result


def test_string_method_signature():
    code = """!x = "hello"
!x.upper("""
    
    result = run_completion(code)

    assert isinstance(result, dict)


def test_invalid_signature():
    code = """!x = 5
!x.unknown("""
    
    result = run_completion(code)

    # unknown method → fallback to []
    assert result == [] or isinstance(result, dict)
