def detect_signature_context(code: str, cursor_pos: int):
    """
    Detect method call like:
    !x.add(
    
    Returns:
        (var_name, method_name)
    """

    i = cursor_pos - 1

    # ✅ find '('
    while i >= 0 and code[i] != "(":
        i -= 1

    if i < 0:
        return None

    # ✅ get method name
    j = i - 1
    method_name = ""

    while j >= 0 and (code[j].isalnum() or code[j] == "_"):
        method_name = code[j] + method_name
        j -= 1

    if not method_name:
        return None

    # ✅ skip dot
    if j >= 0 and code[j] == ".":
        j -= 1
    else:
        return None  # not method call

    # ✅ get variable name
    var_name = ""
    while j >= 0 and (code[j].isalnum() or code[j] == "_"):
        var_name = code[j] + var_name
        j -= 1

    if not var_name:
        return None

    return (var_name, method_name)


def get_method_signature(method):
    """
    Extract parameters from Python function
    """
    try:
        code_obj = method.__code__

        params = list(code_obj.co_varnames[:code_obj.co_argcount])

        # remove 'self'
        if params and params[0] == "self":
            params = params[1:]

        return {
            "name": method.__name__,
            "params": params
        }

    except Exception:
        return {
            "name": "unknown",
            "params": []
        }

from pydbml.ide.method_resolver import get_class_from_type


def get_signature_for_call(symbols, method_name, evaluator, var_name):
    cls = None
    
    if evaluator:
        try:
            var_value = evaluator.env.get(var_name).get()
            cls = var_value.__class__
        except Exception:
            pass
        
    # fallback
    if not cls:
        var_type = symbols["variables"].get(var_name)
        cls = get_class_from_type(var_type)

    if not cls or not evaluator:
        return None

    # build cache if needed
    if cls not in evaluator._method_cache:
        evaluator._build_cache(cls)

    method_map = evaluator._method_cache.get(cls, {})

    method = method_map.get(method_name.upper())

    if not method:
        method = method_map.get(method_name.lower())

    return get_method_signature(method)
