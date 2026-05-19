import re
from pydbml.lexer.tokens import Token
from pydbml.utils.debug import debug

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
    # Whitespace
    # --------------------------
    ("IMPORT", r"import"),
    ("DO", r"\bdo\b"),
    ("ENDDO", r"\benddo\b"),
    ("BREAK", r"\bbreak\b"),
    ("SKIP", r"\bskip\b"),
    
    ("INDICES", r"\bindices\b"),
    ("VALUES", r"\bvalues\b"),
    
    # ✅ ALWAYS LAST
    ("IDENTIFIER", r"[a-zA-Z_]\w*"),
]

BUILTIN_OPERATORS = {
    "+", "-", "*", "/", "&",
    "==", "!=", ">", "<", ">=", "<="
}


def tokenize(code: str):
    tokens = []

    regex = build_token_regex()

    for match in re.finditer(regex, code, flags=re.IGNORECASE):
        kind = match.lastgroup
        value = match.group()

        if kind in ("COMMENT_LINE", "COMMENT_BLOCK"):
            continue

        # ✅ line & column tracking
        start = match.start()

        line = code.count("\n", 0, start) + 1
        last_newline = code.rfind("\n", 0, start)

        if last_newline < 0:
            last_newline = -1

        column = start - last_newline

        # ✅ normalize keywords
        if kind in {"IF", "THEN", "ELSE", "AND", "OR", "NOT"}:
            value = value.upper()

        # ✅ normalize boolean
        if kind == "BOOLEAN":
            value = value.lower()

        # ✅ normalize variable names
        if kind in {"LOCAL_VAR", "GLOBAL_VAR"}:
            value = value.lower()

        tokens.append(Token(kind, value, line, column))

    # ✅ enhanced debug
    debug("TOKENS", [f"{t} @({t.line},{t.column})" for t in tokens])

    return tokens

def register_operator_token(symbol, token_name=None):
    token_name = token_name or _safe_token_name(symbol)

    DYNAMIC_OPERATORS[token_name] = re.escape(symbol)

def build_token_regex():
    spec = TOKEN_SPEC.copy()

    insert_index = len(spec) - 1

    # ✅ add dynamic operators
    for name, pattern in DYNAMIC_OPERATORS.items():
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
        .replace("==", "EQ")
        .replace("!=", "NE")
        .replace(">=", "GE")
        .replace("<=", "LE")
    )
