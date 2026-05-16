import re
from pydbml.lexer.tokens import Token
from pydbml.utils.debug import debug

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

    ("IS", r"\bis\b"),

    ("IF", r"\bif\b"),
    ("THEN", r"\bthen\b"),
    ("ELSE", r"\belse\b"),
    ("ENDIF", r"\bendif\b"),

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
    # Whitespace
    # --------------------------
    ("DO", r"\bdo\b"),
    ("ENDDO", r"\benddo\b"),
    ("BREAK", r"\bbreak\b"),
    ("SKIP", r"\bskip\b"),

    # ✅ ALWAYS LAST
    ("IDENTIFIER", r"[a-zA-Z_]\w*"),
]


TOKEN_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)


def tokenize(code: str):
    tokens = []

    for match in re.finditer(TOKEN_REGEX, code, flags=re.IGNORECASE):
        kind = match.lastgroup
        value = match.group()

        if kind in ("SKIP", "COMMENT_LINE", "COMMENT_BLOCK"):
            continue

        # ✅ normalize keywords
        if kind in {"IF", "THEN", "ELSE", "AND", "OR", "NOT"}:
            value = value.upper()

        # ✅ normalize boolean
        if kind == "BOOLEAN":
            value = value.lower()

        # ✅ normalize variable names (case-insensitive)
        if kind in {"LOCAL_VAR", "GLOBAL_VAR"}:
            value = value.lower()

        tokens.append(Token(kind, value))

    debug("TOKENS", tokens)
    return tokens