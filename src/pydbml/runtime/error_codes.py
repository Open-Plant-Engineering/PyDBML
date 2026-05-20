# ✅ Central error code registry

ERROR_CODES = {
    # --------------------------
    # Type & Value Errors
    # --------------------------
    "TYPE_ERROR": (10, 1, "Invalid type"),
    "VALUE_ERROR": (10, 2, "Invalid value"),

    # --------------------------
    # Variables / Scope
    # --------------------------
    "NAME_ERROR": (11, 1, "Variable not defined"),

    # --------------------------
    # Function / Call
    # --------------------------
    "ARG_COUNT": (12, 1, "Argument count mismatch"),
    "RETURN_TYPE": (12, 2, "Invalid return type"),

    # --------------------------
    # Object / Attribute
    # --------------------------
    "ATTRIBUTE_ERROR": (20, 1, "Attribute not found"),
    "METHOD_NOT_FOUND": (20, 2, "Method not found"),
    "OVERLOAD_NOT_FOUND": (20, 3, "No matching overload"),

    # --------------------------
    # Index / Collection
    # --------------------------
    "INDEX_ERROR": (30, 1, "Invalid index"),
    "KEY_ERROR": (30, 2, "Invalid key"),

    # --------------------------
    # Operators
    # --------------------------
    "OPERATOR_ERROR": (40, 1, "Operator not supported"),

    # --------------------------
    # Object Construction
    # --------------------------
    "CONSTRUCTOR_ERROR": (50, 1, "Constructor mismatch"),

    # --------------------------
    # Internal
    # --------------------------
    "INTERNAL": (99, 1, "Internal error"),

    "SYNTAX_ERROR": (100, 1, "Syntax error"),
}

from pydbml.runtime.exceptions import PyDBMLError

def raise_error(key, message=None, node=None, stack=None):
    if key not in ERROR_CODES:
        # fallback
        code1, code2, default_msg = ERROR_CODES["INTERNAL_ERROR"]
        return PyDBMLError(code1, code2, message or f"Unknown error key: {key}", node=node, stack=stack)

    code1, code2, default_msg = ERROR_CODES[key]

    return PyDBMLError(
        code1,
        code2,
        message or default_msg,
        node=node,
        stack=stack
    )