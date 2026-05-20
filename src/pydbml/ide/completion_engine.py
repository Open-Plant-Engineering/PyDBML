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
        return symbols["variables"]
    
    # ✅ !! → functions + globals + objects
    elif context == "double_bang":
        return list(set(
            symbols["variables"] +
            symbols["functions"] +
            symbols["objects"]
        ))
    
    # ✅ dot → object methods (still placeholder)
    elif context == "dot":
        return ["add", "remove", "length"]  # next step we'll fix this
    
    return []