from pydbml.ide.context import detect_context
from pydbml.ide.symbol_extractor import extract_symbols, extract_symbols_safe
from pydbml.parser.parser import Parser
from pydbml.ide.method_resolver import (
    get_class_from_type,
    get_methods_from_class
)
from pydbml.execution.ast_evaluator import ASTEvaluator

def get_completions(code: str, cursor_pos: int, evaluator=None):
    try:
        parser = Parser(code)
        ast = parser.parse()
        symbols = extract_symbols(ast)

    except Exception:
        symbols = extract_symbols_safe(code)

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
