from pydbml.lexer.tokenizer import tokenize


def test_tokenize_simple_assignment():
    tokens = tokenize("!x = 10")

    assert [t.type for t in tokens] == [
        "LOCAL_VAR",
        "EQUAL",
        "NUMBER",
    ]


def test_tokenize_expression():
    tokens = tokenize("!z = (!x + !y) * 2")

    assert [t.type for t in tokens] == [
        "LOCAL_VAR",
        "EQUAL",
        "LPAREN",
        "LOCAL_VAR",
        "PLUS",
        "LOCAL_VAR",
        "RPAREN",
        "MUL",
        "NUMBER",
    ]


def test_string_token():
    tokens = tokenize("!name = 'Tommy'")

    assert tokens[2].type == "STRING"