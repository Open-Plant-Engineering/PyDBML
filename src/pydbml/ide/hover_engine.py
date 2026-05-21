def get_token_at_cursor(code: str, cursor_pos: int):
    """
    Extract the word under cursor
    """

    if not code:
        return None

    i = cursor_pos - 1

    # move left if cursor is on non-word
    while i >= 0 and not (code[i].isalnum() or code[i] == "_"):
        i -= 1

    if i < 0:
        return None

    # extract token
    token = ""
    while i >= 0 and (code[i].isalnum() or code[i] == "_"):
        token = code[i] + token
        i -= 1

    return token


def get_hover_context(code: str, cursor_pos: int):
    i = cursor_pos - 1

    # check if inside method call or dot access
    while i >= 0:
        if code[i] == ".":
            return "method"
        if code[i] in (" ", "\n", "\t"):
            break
        i -= 1

    return "variable"

from pydbml.ide.method_resolver import get_class_from_type


def get_hover_info(code: str, cursor_pos: int, symbols, evaluator=None):
    token = get_token_at_cursor(code, cursor_pos)

    if not token:
        return None

    context = get_hover_context(code, cursor_pos)

    # ✅ VARIABLE HOVER
    if context == "variable":
        var_type = symbols["variables"].get(token)

        if var_type:
            return {
                "type": var_type,
                "name": token,
                "kind": "variable"
            }

    # ✅ METHOD HOVER
    elif context == "method":
        # find variable before method
        i = code.rfind(".", 0, cursor_pos)
        if i == -1:
            return None

        var_name = ""
        j = i - 1

        while j >= 0 and (code[j].isalnum() or code[j] == "_"):
            var_name = code[j] + var_name
            j -= 1

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

        if evaluator and cls:
            if cls not in evaluator._method_cache:
                evaluator._build_cache(cls)

            method_map = evaluator._method_cache.get(cls, {})

            method = method_map.get(token.upper())

            if method:
                try:
                    params = method.__code__.co_varnames[:method.__code__.co_argcount]

                    if params and params[0] == "self":
                        params = params[1:]

                except Exception:
                    params = []

                return {
                    "name": token,
                    "params": list(params),
                    "kind": "method",
                    "type": var_type
                }

    return None
