from pydbml.ide.context import detect_context
from pydbml.ide.symbol_extractor import extract_symbols, extract_symbols_safe
from pydbml.parser.parser import Parser


def get_completions(code: str, cursor_pos: int):
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
    
        if var_type and var_type in TYPE_METHODS:
            return TYPE_METHODS[var_type]
    
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
