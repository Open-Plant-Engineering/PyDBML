from pydbml.lexer.tokenizer import tokenize
from pydbml.ast.nodes import (
    NumberNode,
    StringNode,
    BooleanNode,
    VariableNode,
    AssignNode,
    BinaryOpNode,
    IfNode,
    IndexAssignNode,
    DotAssignNode,
    CallNode,
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

        # ✅ DOT assignment FIRST (highest priority)
        if self._peek().type in ("LOCAL_VAR", "GLOBAL_VAR"):
            if self._is_dot_assignment():
                return self._parse_dot_assignment()

            if self._is_index_assignment():
                return self._parse_index_assignment()

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
    
        # ✅ ADD THIS BLOCK HERE
        if token.type == "IDENTIFIER" and token.value.lower() == "object":
            from pydbml.ast.nodes import ObjectNode
    
            type_token = self._consume()
    
            if type_token.type != "IDENTIFIER":
                raise SyntaxError("Expected type after 'object'")
    
            type_name = type_token.value.lower()
    
            self._consume_expected("LPAREN")
            self._consume_expected("RPAREN")
    
            return ObjectNode(type_name)
    
        if token.type in ("LOCAL_VAR", "GLOBAL_VAR"):
            is_global = token.type == "GLOBAL_VAR"
            name = token.value.replace("!", "")

            from pydbml.ast.nodes import VariableNode, IndexAccessNode, DotAccessNode

            node = VariableNode(name, is_global)

            while True:
            
                # --------------------------
                # Index access
                # --------------------------
                if self._match("LBRACKET"):
                    self._consume()
                    index_expr = self.expression()
                    self._consume_expected("RBRACKET")
                    node = IndexAccessNode(node, index_expr)
                    continue
                
                # --------------------------
                # Dot access
                # --------------------------
                if self._match("DOT"):
                    self._consume()
                    attr_token = self._consume()

                    if attr_token.type not in ("IDENTIFIER", "AND", "OR", "NOT"):
                        raise SyntaxError("Expected attribute name after '.'")

                    method_name = attr_token.value

                    # ✅ method call
                    if self._match("LPAREN"):
                        self._consume()  # (

                        args = []

                        if not self._match("RPAREN"):
                            args.append(self.expression())

                            while self._match("COMMA"):
                                self._consume()
                                args.append(self.expression())

                        self._consume_expected("RPAREN")
                        node = CallNode(node, method_name, args)
                    else:
                        node = DotAccessNode(node, method_name)
                    continue
                break
            return node
    
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

    def _is_index_assignment(self):
        """
        Detect pattern: !x[ ... ] = ...
        """

        if self._peek().type not in ("LOCAL_VAR", "GLOBAL_VAR"):
            return False

        if not self._peek_next() or self._peek_next().type != "LBRACKET":
            return False

        pos = self.pos + 1
        depth = 0

        while pos < len(self.tokens):
            token = self.tokens[pos]

            if token.type == "LBRACKET":
                depth += 1
            elif token.type == "RBRACKET":
                depth -= 1

                if depth == 0:
                    if pos + 1 < len(self.tokens) and self.tokens[pos + 1].type == "EQUAL":
                        return True
                    return False

            pos += 1

        return False
    
    def _parse_index_assignment(self):
        token = self._consume()

        is_global = token.type == "GLOBAL_VAR"
        name = token.value.replace("!", "")

        target = VariableNode(name, is_global)

        # parse index
        self._consume_expected("LBRACKET")
        index_expr = self.expression()
        self._consume_expected("RBRACKET")

        # expect '='
        self._consume_expected("EQUAL")

        # parse value
        value = self.expression()

        return IndexAssignNode(target, index_expr, value)
    
    def _is_dot_assignment(self):
        """
        Detect pattern:
        !x.name = ...
        !x[1].name = ...
        """

        if self._peek().type not in ("LOCAL_VAR", "GLOBAL_VAR"):
            return False

        pos = self.pos

        while pos < len(self.tokens):
            t = self.tokens[pos]

            # found a dot
            if t.type == "DOT":
                # ensure IDENTIFIER follows and then '='
                if (
                    pos + 2 < len(self.tokens)
                    and self.tokens[pos + 1].type == "IDENTIFIER"
                    and self.tokens[pos + 2].type == "EQUAL"
                ):
                    return True

            # also handle nested cases like !x[1].name
            if t.type == "EQUAL":
                break

            pos += 1

        return False


    def _parse_dot_assignment(self):
        # parse full left-hand side (supports chaining)
        target = self._parse_primary()

        if not hasattr(target, "attribute"):
            raise SyntaxError("Invalid dot assignment")

        self._consume_expected("EQUAL")

        value = self.expression()

        return DotAssignNode(target.target, target.attribute, value)
