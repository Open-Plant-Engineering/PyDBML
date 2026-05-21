import re
from pydbml.lexer.tokens import Token
from pydbml.utils.debug import debug
from pydbml.runtime.error_codes import raise_error

DYNAMIC_OPERATORS = {}
TOKEN_SPEC = [
    
    ("COMMENT_BLOCK", r"\$\([\s\S]*?\$\)"),
    ("COMMENT_LINE", r"--.*"),

    # --------------------------
    # Keywords (MUST COME FIRST)
    # --------------------------
    ("DEFINE", r"\bdefine\b"),
    ("FUNCTION", r"\bfunction\b"),
    ("ENDFUNCTION", r"\bendfunction\b"),
    ("RETURN", r"\breturn\b"),

    ("OBJECT", r"\bobject\b"),
    ("ENDOBJECT", r"\bendobject\b"),
    ("MEMBER", r"\bmember\b"),

    ("METHOD", r"\bmethod\b"),
    ("ENDMETHOD", r"\bendmethod\b"),

    ("FROM", r"\bfrom\b"),
    ("TO", r"\bto\b"),
    ("BY", r"\bby\b"),
    ("IS", r"\bis\b"),

    ("IF", r"\bif\b"),
    ("THEN", r"\bthen\b"),
    ("ELSE", r"\belse\b"),
    ("ENDIF", r"\bendif\b"),

    ("HANDLE", r"\bhandle\b"),
    ("ELSEHANDLE", r"\belsehandle\b"),
    ("ANY", r"\bany\b"),
    ("NONE", r"\bnone\b"),
    ("ENDHANDLE", r"\bendhandle\b"),

    ("LABEL", r"\blabel\b"),
    ("GOLABEL", r"\bgolabel\b"),
    
    ("AND", r"\band\b"),
    ("OR", r"\bor\b"),
    ("NOT", r"\bnot\b"),

    # --------------------------
    # Boolean
    # --------------------------
    ("BOOLEAN", r"\btrue\b|\bfalse\b"),

    # --------------------------
    # PML1 Keywords
    # --------------------------
    ("EQ_KW", r"\beq\b"),
    ("NEQ_KW", r"\bneq\b"),
    ("LT_KW", r"\blt\b"),
    ("GT_KW", r"\bgt\b"),
    ("LE_KW", r"\ble\b"),
    ("GE_KW", r"\bge\b"),

    # --------------------------
    # Custom tokens
    # --------------------------
    ("COMMAND_VAR", r"\$\!\!?[a-zA-Z_][a-zA-Z0-9_]*"),
    ("STRING_PIPE", r"\|[\s\S]*?\|"),
    ("STRING", r"'[^']*'"),

    # --------------------------
    # Numbers
    # --------------------------
    ("NUMBER", r"\d+(\.\d+)?"),

    # --------------------------
    # Variables
    # --------------------------
    ("GLOBAL_VAR", r"!![a-zA-Z_]\w*"),
    ("LOCAL_VAR", r"![a-zA-Z_]\w*"),

    # --------------------------
    # Operators (multi BEFORE single)
    # --------------------------
    ("EQ", r"=="),
    ("NE", r"!="),
    ("GE", r">="),
    ("LE", r"<="),

    ("GT", r">"),
    ("LT", r"<"),

    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),
    ("AMP", r"&"),

    # --------------------------
    # Symbols
    # --------------------------
    ("DOT", r"\."),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("COMMA", r","),

    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),

    ("EQUAL", r"="),

    # --------------------------
    # Control keywords / late keywords
    # --------------------------
    ("IMPORT", r"\bimport\b"),
    ("DO", r"\bdo\b"),
    ("ENDDO", r"\benddo\b"),
    ("BREAK", r"\bbreak\b"),
    ("SKIP", r"\bskip\b"),
    
    ("INDICES", r"\bindices\b"),
    ("VALUES", r"\bvalues\b"),
    
    # ✅ ALWAYS LAST
    ("IDENTIFIER", r"[a-zA-Z_]\w*"),
    ("WHITESPACE", r"\s+"),
]

BUILTIN_OPERATORS = {
    "+", "-", "*", "/", "&",
    "==", "!=", ">", "<", ">=", "<="
}

_COMPILED_REGEX = None

def tokenize(code: str):
    """
    Tokenizer (Lexer) for PyDBML.

    Responsibilities:
        ✔ converts raw code → tokens
        ✔ tracks positions (line, column)
        ✔ normalizes token values
        ✔ supports dynamic operator injection

    Design:
        - regex-based lexer
        - ordered token priority system
        - extensible via plugin operators

    Notes:
        - keyword order matters (must appear before IDENTIFIER)
        - dynamic operators inserted before IDENTIFIER
    """

    global _COMPILED_REGEX

    if _COMPILED_REGEX is None:
        _COMPILED_REGEX = re.compile(build_token_regex(), re.IGNORECASE)

    tokens = []

    # ✅ split source lines (needed for ^ pointer)
    lines = code.splitlines()

    matches = list(_COMPILED_REGEX.finditer(code))

    # -----------------------------------
    # ✅ STRICT VALIDATION (NO GAPS)
    # -----------------------------------
    pos = 0
    for match in matches:
        if match.start() != pos:
            start = pos

            line = code.count("\n", 0, start) + 1
            last_newline = code.rfind("\n", 0, start)
            last_newline = last_newline if last_newline >= 0 else -1
            column = start - last_newline

            dummy = Token("UNKNOWN", code[start], line, column)
            dummy.source_line = lines[line - 1] if line - 1 < len(lines) else ""

            raise raise_error(
                "SYNTAX_ERROR",
                f"Unexpected character '{code[start]}'",
                node=type("DummyNode", (), {"token": dummy})()
            )

        pos = match.end()

    if pos != len(code):
        start = pos

        line = code.count("\n", 0, start) + 1
        last_newline = code.rfind("\n", 0, start)
        last_newline = last_newline if last_newline >= 0 else -1
        column = start - last_newline

        dummy = Token("UNKNOWN", code[start], line, column)
        dummy.source_line = lines[line - 1] if line - 1 < len(lines) else ""

        raise raise_error(
            "SYNTAX_ERROR",
            f"Unexpected character '{code[start]}'",
            node=type("DummyNode", (), {"token": dummy})()
        )

    # -----------------------------------
    # ✅ TOKEN CREATION
    # -----------------------------------
    for match in matches:
        kind = match.lastgroup
        value = match.group()

        if kind in ("COMMENT_LINE", "COMMENT_BLOCK", "WHITESPACE"):
            continue

        start = match.start()
        line = code.count("\n", 0, start) + 1
        last_newline = code.rfind("\n", 0, start)
        last_newline = last_newline if last_newline >= 0 else -1
        column = start - last_newline

        # ✅ normalize values
        if kind in {"IF", "THEN", "ELSE", "AND", "OR", "NOT"}:
            value = value.upper()

        if kind == "BOOLEAN":
            value = value.lower()

        if kind in {"LOCAL_VAR", "GLOBAL_VAR"}:
            value = value.lower()

        # ✅ create token
        t = Token(kind, value, line, column)

        # ✅ attach source line for pointer (^)
        t.source_line = lines[line - 1] if line - 1 < len(lines) else ""

        tokens.append(t)

    return tokens

def register_operator_token(symbol, token_name=None):
    global _COMPILED_REGEX

    token_name = token_name or _safe_token_name(symbol)

    if token_name not in DYNAMIC_OPERATORS:
        DYNAMIC_OPERATORS[token_name] = re.escape(symbol)
        _COMPILED_REGEX = None  # ✅ only invalidate when new

def build_token_regex():
    spec = TOKEN_SPEC.copy()

    insert_index = len(spec) - 1

    # ✅ add dynamic operators
    for name, pattern in sorted(DYNAMIC_OPERATORS.items()):
        spec.insert(insert_index, (name, pattern))
        insert_index += 1
        # insert before IDENTIFIER

    return "|".join(f"(?P<{name}>{pattern})" for name, pattern in spec)

def _safe_token_name(symbol):
    return "OP_" + (
        symbol
        .replace("+", "PLUS")
        .replace("-", "MINUS")
        .replace("*", "MUL")
        .replace("/", "DIV")
        .replace("%", "MOD")
        .replace("^", "POW")
        .replace("&", "AMP")
        .replace("=", "EQ")
        .replace("!", "NOT")
        .replace("<", "LT")
        .replace(">", "GT")
        .replace("!=", "NE")
        .replace(">=", "GE")
        .replace("<=", "LE")
    )
