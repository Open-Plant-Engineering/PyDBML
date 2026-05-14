import re
from pydbml.lexer.tokens import Token


TOKEN_SPEC = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("STRING", r"'[^']*'"),

    # ✅ Boolean keywords
    ("BOOLEAN", r"\btrue\b|\bfalse\b"),

    # ✅ Multi-character operators FIRST
    ("EQ", r"=="),
    ("NE", r"!="),
    ("GE", r">="),
    ("LE", r"<="),

    # ✅ Single-character operators
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

        tokens.append(Token(kind, value))

    return tokens