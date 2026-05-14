from pydbml.lexer.tokenizer import tokenize
from pydbml.ast.nodes import (
    NumberNode,
    StringNode,
    BooleanNode,
    VariableNode,
    AssignNode,
    BinaryOpNode,
    IfNode,
    IndexAccessNode,
)


class Parser:
    def __init__(self, code: str):
        self.tokens = tokenize(code)
        self.pos = 0

    # --------------------------
    # Entry
    # --------------------------
    def parse(self):
        return self.statement()

    # --------------------------
    # Statement
    # --------------------------
    def statement(self):
        # Assignment: VAR = expr
        if self._peek().type in ("LOCAL_VAR", "GLOBAL_VAR"):
            if self._peek_next() and self._peek_next().type == "EQUAL":
                return self.assignment()

        return self.expression()

    # --------------------------
    # Assignment
    # --------------------------
    def assignment(self):
        token = self._consume()

        is_global = token.type == "GLOBAL_VAR"
        name = token.value.replace("!", "")

        self._consume_expected("EQUAL")

        value = self.expression()

        return AssignNode(name, value, is_global)

    # --------------------------
    # Expression (precedence)
    # --------------------------
    def expression(self):
        if self._match("IF"):
            return self._parse_if()

        return self._parse_or()

    def _parse_comparison(self):
        node = self._parse_term()

        while self._match("EQ", "NE", "GT", "LT", "GE", "LE"):
            op_token = self._consume()
            op_map = {
                "EQ": "==",
                "NE": "!=",
                "GT": ">",
                "LT": "<",
                "GE": ">=",
                "LE": "<=",
            }
            op = op_map[op_token.type]
            right = self._parse_term()
            node = BinaryOpNode(node, op, right)

        return node

    def _parse_term(self):
        node = self._parse_factor()

        while self._match("PLUS", "MINUS"):
            op = self._consume().value
            right = self._parse_factor()
            node = BinaryOpNode(node, op, right)

        return node

    def _parse_factor(self):
        node = self._parse_primary()

        while self._match("MUL", "DIV"):
            op = self._consume().value
            right = self._parse_primary()
            node = BinaryOpNode(node, op, right)

        return node

    def _parse_primary(self):
        token = self._consume()

        # --------------------------
        # Boolean
        # --------------------------
        if token.type == "BOOLEAN":
            return BooleanNode(token.value.lower() == "true")

        # --------------------------
        # Number
        # --------------------------
        if token.type == "NUMBER":
            return NumberNode(float(token.value))

        # --------------------------
        # String
        # --------------------------
        if token.type == "STRING":
            return StringNode(token.value.strip("'"))

        if token.type == "LOCAL_VAR":
            return VariableNode(token.value[1:], False)

        if token.type == "GLOBAL_VAR":
            return VariableNode(token.value[2:], True)

        if token.type == "LPAREN":
            node = self.expression()
            self._consume_expected("RPAREN")
            return node

        raise SyntaxError(f"Unexpected token: {token.type}")

    # --------------------------
    # Helpers
    # --------------------------
    def _peek(self):
        return self.tokens[self.pos]

    def _peek_next(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    def _consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def _consume_expected(self, token_type):
        token = self._consume()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type}")

    def _match(self, *types):
        if self.pos < len(self.tokens) and self.tokens[self.pos].type in types:
            return True
        return False
    
    def _parse_if(self):
        """
        IF condition THEN expr ELSE expr
        """
    
        self._consume_expected("IF")
    
        condition = self.expression()
    
        self._consume_expected("THEN")
    
        then_branch = self.expression()
    
        else_branch = None
    
        if self._match("ELSE"):
            self._consume()  # consume ELSE
            else_branch = self.expression()
    
        return IfNode(condition, then_branch, else_branch)

    def _parse_or(self):
        node = self._parse_and()

        while self._match("OR"):
            self._consume()
            right = self._parse_and()
            from pydbml.ast.nodes import LogicalOpNode
            node = LogicalOpNode(node, "OR", right)

        return node

    def _parse_and(self):
        node = self._parse_not()

        while self._match("AND"):
            self._consume()
            right = self._parse_not()
            from pydbml.ast.nodes import LogicalOpNode
            node = LogicalOpNode(node, "AND", right)

        return node

    def _parse_not(self):
        if self._match("NOT"):
            self._consume()
            from pydbml.ast.nodes import NotNode
            return NotNode(self._parse_not())

        return self._parse_comparison()