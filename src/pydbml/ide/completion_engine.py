from pydbml.ide.context import detect_context
from pydbml.ide.symbol_extractor import extract_symbols, extract_symbols_safe
from pydbml.parser.parser import Parser
from pydbml.ide.method_resolver import (
    get_class_from_type,
    get_methods_from_class
)
from pydbml.execution.ast_evaluator import ASTEvaluator
from pydbml.ide.signature_engine import (
    detect_signature_context,
    get_signature_for_call
)
from pydbml.ide.hover_engine import get_hover_info


def get_completions(code: str, cursor_pos: int, evaluator=None):
    try:
        parser = Parser(code)
        ast = parser.parse()
        symbols = extract_symbols(ast, evaluator)

    except Exception:
        symbols = extract_symbols_safe(code)

    sig_ctx = detect_signature_context(code, cursor_pos)

    if sig_ctx:
        var_name, method_name = sig_ctx

        sig = get_signature_for_call(symbols, method_name, evaluator, var_name)

        if sig:
            return sig

    context = detect_context(code, cursor_pos)

    # ✅ ! → variables only
    if context == "single_bang":
        return list(symbols["variables"].keys())
    
    # ✅ !! → functions + globals + objects
    elif context == "double_bang":
        return list(set(
            list(symbols["variables"].keys()) +
            symbols["functions"] +
            symbols["objects"]
        ))
    
    # ✅ dot → methods
    elif context == "dot":
        var_name = get_var_before_cursor(code, cursor_pos)
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

        # ✅ REAL methods if evaluator given
        if evaluator and cls:
            methods = get_methods_from_class(cls, evaluator)
            if methods:
                return methods

        # ✅ fallback (for tests without evaluator)
        if var_type == "number":
            return ["add", "sub", "mul", "div"]

        if var_type == "string":
            return ["upper", "lower", "length"]

        if var_type == "object":
            return ["get", "set", "init"]

        return []
    
    hover = get_hover_info(code, cursor_pos, symbols, evaluator)
    if hover and context == "unknown":
        return hover
    
    return []

def get_var_before_cursor(code: str, cursor_pos: int):
    i = cursor_pos - 2  # skip '.'
    var_name = ""

    while i >= 0:
        ch = code[i]

        if ch.isalnum() or ch == "_":
            var_name = ch + var_name
            i -= 1
        else:
            break

    return var_name

TYPE_METHODS = {
    "object": ["init", "get", "set"],
    "number": ["add", "sub", "mul", "div"],
    "string": ["length", "upper", "lower"]
}
