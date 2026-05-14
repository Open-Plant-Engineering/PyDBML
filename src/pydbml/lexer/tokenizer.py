import re
from pydbml.lexer.tokens import Token


TOKEN_SPEC = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("STRING", r"'[^']*'"),

    # Keywords (case-insensitive handled later)
    ("IF", r"\b(IF|if)\b"),
    ("THEN", r"\b(THEN|then)\b"),
    ("ELSE", r"\b(ELSE|else)\b"),

    ("AND", r"\b(AND|and)\b"),
    ("OR", r"\b(OR|or)\b"),
    ("NOT", r"\b(NOT|not)\b"),

    ("BOOLEAN", r"\b(true|false)\b"),

    # Multi-char operators
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

    ("GLOBAL_VAR", r"!![a-zA-Z_]\w*"),
    ("LOCAL_VAR", r"![a-zA-Z_]\w*"),

    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
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

    return tokens