def detect_context(code: str, cursor_pos: int):
    if cursor_pos < 1:
        return "none"

    prev = code[cursor_pos - 1]

    # ✅ variable prefix
    if prev == "!":
        if cursor_pos >= 2 and code[cursor_pos - 2] == "!":
            return "double_bang"
        return "single_bang"

    # ✅ method access
    if prev == ".":
        return "dot"

    # ✅ inside identifier (IMPORTANT)
    if prev.isalnum() or prev == "_":
        # check if inside dot chain
        i = cursor_pos - 1
        while i >= 0:
            if code[i] == ".":
                return "dot"
            if code[i] in " \n\t":
                break
            i -= 1

    return "unknown"
