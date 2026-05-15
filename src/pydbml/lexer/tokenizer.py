import re
from pydbml.lexer.tokens import Token
from pydbml.utils.debug import debug

TOKEN_SPEC = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("STRING", r"'[^']*'"),

    ("DEFINE", r"\bdefine\b"),
    ("METHOD", r"\bmethod\b"),
    ("ENDMETHOD", r"\bendmethod\b"),
    ("OBJECT", r"\bobject\b"),
    ("MEMBER", r"\bmember\b"),
    ("ENDOBJECT", r"\bendobject\b"),
    ("FUNCTION", r"\b(FUNCTION|function)\b"),
    ("ENDFUNCTION", r"\b(ENDFUNCTION|endfunction)\b"),
    ("RETURN", r"\b(RETURN|return)\b"),
    ("IS", r"\b(IS|is)\b"),

    # Keywords (case-insensitive handled later)
    ("IF", r"\b(IF|if)\b"),
    ("THEN", r"\b(THEN|then)\b"),
    ("ELSE", r"\b(ELSE|else)\b"),

    ("AND", r"\b(AND|and)\b"),
    ("OR", r"\b(OR|or)\b"),
    ("NOT", r"\b(NOT|not)\b"),

    ("BOOLEAN", r"\b(true|false)\b"),

    # --------------------------
    # PML1 Comparison keywords
    # --------------------------
    ("EQ_KW", r"\b(EQ|eq)\b"),
    ("NEQ_KW", r"\b(NEQ|neq)\b"),
    ("LT_KW", r"\b(LT|lt)\b"),
    ("GT_KW", r"\b(GT|gt)\b"),
    ("LE_KW", r"\b(LE|le)\b"),
    ("GE_KW", r"\b(GE|ge)\b"),

    # Multi-char operators
    ("EQ", r"=="),
    ("NE", r"!="),
    ("GE", r">="),
    ("LE", r"<="),

    ("DOT", r"\."),

    ("GT", r">"),
    ("LT", r"<"),

    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),

    ("GLOBAL_VAR", r"!![a-zA-Z_]\w*"),
    ("LOCAL_VAR", r"![a-zA-Z_]\w*"),

    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),

    ("COMMA", r","),

    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    
    ("EQUAL", r"="),

    ("IDENTIFIER", r"[a-zA-Z_]\w*"),
    ("SKIP", r"[ \t]+"),
]


TOKEN_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)


def tokenize(code: str):
    tokens = []

    for match in re.finditer(TOKEN_REGEX, code):
        kind = match.lastgroup
        value = match.group()

        if kind == "SKIP":
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