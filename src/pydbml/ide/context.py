def detect_context(code: str, cursor_pos: int):
    if cursor_pos < 1:
        return "none"

    # ✅ look behind safely
    prev = code[cursor_pos - 1]
    prev2 = code[cursor_pos - 2] if cursor_pos >= 2 else ""

    # ✅ !! context
    if prev == "!" and prev2 == "!":
        return "double_bang"

    # ✅ ! context
    if prev == "!":
        return "single_bang"

    # ✅ method access
    if prev == ".":
        return "dot"

    return "unknown"
