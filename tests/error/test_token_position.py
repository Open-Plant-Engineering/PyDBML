from pydbml.lexer.tokenizer import tokenize

def test_token_position_basic():
    code = "!x = 10\n!y = !x + 5"

    tokens = tokenize(code)

    plus = [t for t in tokens if t.value == "+"][0]

    assert plus.line == 2
    assert plus.column > 0