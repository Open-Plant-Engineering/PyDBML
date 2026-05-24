from pydbml.parser.parser import Parser

def test_ast_has_position():
    code = "!x = 10 + 5"

    parser = Parser(code)
    ast = parser.parse()

    node = ast[0].value  # BinaryOpNode

    assert node.token is not None
    assert node.token.line == 1

