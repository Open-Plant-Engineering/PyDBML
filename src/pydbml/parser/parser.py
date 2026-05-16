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
    IndexAccessNode, 
    DotAccessNode,
    FunctionCallNode,
    FunctionDefNode,
    ReturnNode,
    ObjectDefNode,
    PipeStringNode,
    CommandVarNode,
    DoNode,
    BreakIfNode,
    BreakNode,
    ObjectNode,
    SkipIfNode,
)
from pydbml.utils.debug import debug

class Parser:
    def __init__(self, code: str):
        self.tokens = tokenize(code)
        self.pos = 0

    # --------------------------
    # Entry
    # --------------------------
    def parse(self):
        statements = []
        while not self._at_end():
            statements.append(self.statement())
        return statements

    # --------------------------
    # Statement
    # --------------------------
    def statement(self):
        token = self._peek()
        next_token = self._peek_next()

        # ✅ ✅ 1. ALWAYS HANDLE ASSIGNMENT FIRST (CRITICAL FIX)
        if token and token.type in ("LOCAL_VAR", "GLOBAL_VAR"):
            if next_token and next_token.type == "EQUAL":
                return self.assignment()
                
        # --------------------------
        # ✅ SKIP handling
        # --------------------------
        if self._match("SKIP"):
            self._consume()
        
            # ✅ skip if(...)
            if self._match("IF"):
                self._consume()
        
                if self._match("LPAREN"):
                    self._consume()
                    condition = self.expression()
                    self._consume_expected("RPAREN")
                else:
                    condition = self.expression()
        
                return SkipIfNode(condition)
        
            # ✅ standalone skip
            return SkipIfNode(None)
        
        # --------------------------
        # ✅ BREAK handling
        # --------------------------
        if self._match("BREAK"):
            self._consume()
        
            # ✅ break if(...)
            if self._match("IF"):
                self._consume()
        
                if self._match("LPAREN"):
                    self._consume()
                    condition = self.expression()
                    self._consume_expected("RPAREN")
                else:
                    condition = self.expression()
        
                return BreakIfNode(condition)
        
            # ✅ standalone break
            return BreakNode()        
        
        if self._match("IF"):
            pos_backup = self.pos
        
            self._consume()
        
            if self._match("LPAREN"):
                self._consume()
                condition = self.expression()
                self._consume_expected("RPAREN")
            else:
                condition = self.expression()
        
            if not self._match("THEN"):
                return SkipIfNode(condition)
        
            self.pos = pos_backup

        if self._match("DO"):
            return self._parse_do()

        if self._match("DEFINE"):
            # lookahead
            if self._peek_next() and self._peek_next().value.lower() == "function":
                return self._parse_function_def()

            if self._peek_next() and self._peek_next().value.lower() == "object":
                return self._parse_object_def()

            if self._peek_next() and self._peek_next().value.lower() == "method":
                return self._parse_method_def()

            raise SyntaxError("Unknown DEFINE type")

        if self._match("RETURN"):
            return self._parse_return()

        # ✅ dot/index AFTER assignment
        if token and token.type in ("LOCAL_VAR", "GLOBAL_VAR"):
            if self._is_dot_assignment():
                return self._parse_dot_assignment()

            if self._is_index_assignment():
                return self._parse_index_assignment()

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

        while self._match( "EQ", "NE", "GT", "LT", "GE", "LE",
            "EQ_KW", "NEQ_KW", "GT_KW", "LT_KW", "GE_KW", "LE_KW", "AMP"
        ):
            op_token = self._consume()
            op_map = {
                "EQ": "==",
                "NE": "!=",
                "GT": ">",
                "LT": "<",
                "GE": ">=",
                "LE": "<=",
                
                # PML1 keywords ✅
                "EQ_KW": "==",
                "NEQ_KW": "!=",
                "GT_KW": ">",
                "LT_KW": "<",
                "GE_KW": ">=",
                "LE_KW": "<=",
                "AMP": "&"
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
        # ✅ FIX: handle unary minus FIRST
        if self._match("MINUS"):
            self._consume()
            operand = self._parse_factor()
            return BinaryOpNode(NumberNode(0), "-", operand)

        # existing logic
        node = self._parse_primary()

        while self._match("MUL", "DIV"):
            op = self._consume().value
            right = self._parse_primary()
            node = BinaryOpNode(node, op, right)

        return node

    def _parse_primary(self):
        token = self._consume()

        if token.type == "STRING_PIPE":
            raw = token.value[1:-1]  # remove | |
            return PipeStringNode(raw)

        if token.type == "COMMAND_VAR":
            raw = token.value

            is_global = raw.startswith("$!!")
            name = raw.replace("$!!", "").replace("$!", "")

            return CommandVarNode(name, is_global)
        
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
    
        # --------------------------
        # Object creation (UPDATED ✅)
        # --------------------------
        if token.type == "OBJECT":
            type_token = self._consume()
        
            if type_token.type != "IDENTIFIER":
                raise SyntaxError("Expected type after 'object'")
        
            type_name = type_token.value.lower()
        
            self._consume_expected("LPAREN")
        
            args = []
        
            # ✅ parse arguments
            if not self._match("RPAREN"):
                args.append(self.expression())
        
                while self._match("COMMA"):
                    self._consume()
                    args.append(self.expression())
        
            self._consume_expected("RPAREN")
        
            return ObjectNode(type_name, args)

        if token.type in ("LOCAL_VAR", "GLOBAL_VAR"):
            is_global = token.type == "GLOBAL_VAR"
            name = token.value.replace("!", "").lower()

            if token.type == "GLOBAL_VAR" and self._match("LPAREN"):
                self._consume()  # (
                args = []
                if not self._match("RPAREN"):
                    args.append(self.expression())

                    while self._match("COMMA"):
                        self._consume()
                        args.append(self.expression())

                self._consume_expected("RPAREN")

                # ✅ IMPORTANT: use dedicated node
                return FunctionCallNode(name, args)

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
                # Dot access / method call
                # --------------------------
                if self._match("DOT"):
                    self._consume()
                    attr_token = self._consume()
                    method_name = attr_token.value.lower()

                    # ✅ allow identifiers + all keyword-based methods
                    if attr_token.type not in (
                        "IDENTIFIER",
                        "AND", "OR", "NOT",
                        "EQ_KW", "NEQ_KW", "GT_KW", "LT_KW", "GE_KW", "LE_KW"
                    ):
                        raise SyntaxError("Expected attribute name after '.'")

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
        
        if token.type == "IDENTIFIER":
            node = VariableNode(token.value, is_global=False)
        
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
                # Dot access / method call
                # --------------------------
                if self._match("DOT"):
                    self._consume()
                    attr_token = self._consume()
                    method_name = attr_token.value.lower()
        
                    if attr_token.type not in (
                        "IDENTIFIER",
                        "AND", "OR", "NOT",
                        "EQ_KW", "NEQ_KW", "GT_KW", "LT_KW", "GE_KW", "LE_KW"
                    ):
                        raise SyntaxError("Expected attribute name after '.'")
        
                    if self._match("LPAREN"):
                        self._consume()
        
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
        
        raise SyntaxError(f"Unexpected token: {token.type}")

    # --------------------------
    # Helpers
    # --------------------------
    def _peek(self):
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def _peek_next(self):
        if self.pos + 1 >= len(self.tokens):
            return None
        return self.tokens[self.pos + 1]

    def _consume(self):
        if self._at_end():
            raise IndexError("Unexpected end of input")

        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def _consume_expected(self, token_type):
        token = self._peek()
        print("DEBUG consume_expected:", token_type, "got:", token)
        if token is None:
            raise SyntaxError(f"Expected {token_type}, but reached end of input")
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type}")
        return self._consume()

    def _match(self, *types):
        if self.pos < len(self.tokens) and self.tokens[self.pos].type in types:
            return True
        return False
    
    def _parse_if(self):
        self._consume()  # IF

        # --------------------------
        # ✅ CONDITION (support both styles)
        # --------------------------
        if self._match("LPAREN"):
            self._consume()
            condition = self.expression()
            self._consume_expected("RPAREN")
        else:
            condition = self.expression()

        self._consume_expected("THEN")

        # ✅ Always try expression IF first
        # fallback to block IF if parsing fails
        
        # TRY expression IF
        pos_backup = self.pos
        
        try:
            then_expr = self.expression()
            self._consume_expected("ELSE")
            else_expr = self.expression()
        
            return IfNode(condition, then_expr, else_expr, is_expression=True)
        
        except Exception:
            # rollback and parse as block IF
            self.pos = pos_backup

        # --------------------------
        # ✅ BLOCK IF
        # --------------------------
        then_branch = []

        while not self._at_end() and not self._match("ENDIF") and not self._match("ELSE"):
            then_branch.append(self.statement())

        else_branch = None

        if self._match("ELSE"):
            self._consume()
            else_branch = []

            while not self._at_end() and not self._match("ENDIF"):
                else_branch.append(self.statement())

        # ✅ IMPORTANT — now ENDIF must exist
        self._consume_expected("ENDIF")

        return IfNode(condition, then_branch, else_branch, is_expression=False)

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
    
    def _parse_function_def(self):
        self._consume_expected("DEFINE")
        self._consume_expected("FUNCTION")
    
        name_token = self._consume()
    
        if name_token.type != "GLOBAL_VAR":
            raise SyntaxError("Function name must be global (!!)")
    
        func_name = name_token.value.replace("!", "").lower()
    
        # --------------------------
        # Parse parameters
        # --------------------------
        self._consume_expected("LPAREN")
    
        params = []
    
        if not self._match("RPAREN"):
        
            while True:
                var_token = self._consume()
    
                if var_token.type != "LOCAL_VAR":
                    raise SyntaxError("Expected parameter name (!var)")
    
                param_name = var_token.value.replace("!", "")
    
                self._consume_expected("IS")
    
                type_token = self._consume()
    
                param_type = type_token.value.upper()
    
                params.append((param_name, param_type))
    
                if self._match("COMMA"):
                    self._consume()
                    continue
                
                break
            
        self._consume_expected("RPAREN")
    
        # --------------------------
        # Return type (mandatory)
        # --------------------------
        self._consume_expected("IS")
    
        return_type_token = self._consume()
        return_type = return_type_token.value.upper()
    
        # --------------------------
        # Body
        # --------------------------
        body = []
    
        while not self._match("ENDFUNCTION"):
            body.append(self.statement())
    
        self._consume_expected("ENDFUNCTION")
    
        return FunctionDefNode(func_name, params, return_type, body)
    
    def _parse_return(self):
        self._consume_expected("RETURN")
        value = self.expression()
        return ReturnNode(value)
    
    def _parse_object_def(self):
        self._consume_expected("DEFINE")
        self._consume_expected("OBJECT")

        name_token = self._consume()
        obj_name = name_token.value.lower()

        members = {}

        # --------------------------
        # Parse members
        # --------------------------
        while True:
            token = self._peek()

            # ✅ stop condition
            if token and token.type == "ENDOBJECT":
                break

            # ✅ member
            if token.value.lower() == "member":
                self._consume()

                self._consume_expected("DOT")
                attr = self._consume().value

                self._consume_expected("IS")
                type_token = self._consume()

                members[attr] = type_token.value.upper()
                continue

            raise SyntaxError(f"Unexpected token in object: {token}")

        # ✅ consume ENDOBJECT
        self._consume_expected("ENDOBJECT")

        from pydbml.ast.nodes import ObjectDefNode
        return ObjectDefNode(obj_name, members, methods={})
    
    def _parse_method_def(self):
    
        self._consume_expected("DEFINE")
        self._consume_expected("METHOD")
    
        self._consume_expected("DOT")
    
        name_token = self._consume()
        method_name = name_token.value.lower()
    
        # --------------------------
        # Parse parameters (currently empty)
        # --------------------------
        self._consume_expected("LPAREN")

        params = []

        if not self._match("RPAREN"):
            while True:
                param_token = self._consume()  # !x
                param_name = param_token.value.replace("!", "")

                self._consume_expected("IS")
                type_token = self._consume()

                params.append((param_name, type_token.value.upper()))

                if self._match("COMMA"):
                    self._consume()
                    continue
                break
            
        self._consume_expected("RPAREN")
    
        # ✅ optional return type (your test uses: "is real")
        if self._match("IS"):
            self._consume()
            self._consume()  # type token (ignore for now)
    
        # --------------------------
        # Parse body
        # --------------------------
        body = []
    
        while True:
            token = self._peek()
    
            # ✅ STOP HERE
            if token and token.type == "ENDMETHOD":
                break
            
            body.append(self.statement())
    
        # ✅ consume ENDMETHOD
        self._consume_expected("ENDMETHOD")
    
        from pydbml.ast.nodes import MethodDefNode
        return MethodDefNode(method_name, body, params)
    
    def _at_end(self):
        return self.pos >= len(self.tokens)

    def _parse_do(self):
        self._consume_expected("DO")
    
        var_name = None
        mode = None
        iterable = None
        start = None
        end = None
        step = None
    
        # --------------------------
        # CASE 1: LOOP WITH VARIABLE (SAFE CHECK)
        # --------------------------
        if self._peek() and self._peek().type == "LOCAL_VAR":
        
            next_token = self._peek_next()
    
            # ✅ IMPORTANT: only treat as loop variable IF proper syntax follows
            if next_token and next_token.type in ("INDICES", "VALUES", "FROM", "TO"):
            
                var_token = self._consume_expected("LOCAL_VAR")
                var_name = var_token.value.lstrip("!")
    
                # --------------------------
                # SUBCASE: indices loop
                # --------------------------
                if self._peek() and self._peek().type == "INDICES":
                    self._consume_expected("INDICES")

                    token = self._peek()
                    if token and token.type in ("LOCAL_VAR", "GLOBAL_VAR"):
                        iterable_token = self._consume()
                    else:
                        raise SyntaxError(f"Expected variable, got {token}")

                    iterable = iterable_token.value.lstrip("!")
    
                    return self._parse_do_body(
                        var_name=var_name,
                        mode="indices",
                        iterable=iterable
                    )
    
                # --------------------------
                # SUBCASE: values loop
                # --------------------------
                if self._peek() and self._peek().type == "VALUES":
                    self._consume_expected("VALUES")

                    token = self._peek()
                    if token and token.type in ("LOCAL_VAR", "GLOBAL_VAR"):
                        iterable_token = self._consume()
                    else:
                        raise SyntaxError(f"Expected variable after VALUES, got {token}")

                    iterable = iterable_token.value.lstrip("!")
    
                    return self._parse_do_body(
                        var_name=var_name,
                        mode="values",
                        iterable=iterable
                    )
    
                # --------------------------
                # SUBCASE: range loop (FROM)
                # --------------------------
                if self._peek() and self._peek().type == "FROM":
                    self._consume_expected("FROM")
    
                    start = self.expression()
    
                    self._consume_expected("TO")
    
                    end = self.expression()
    
                    if self._peek() and self._peek().type == "BY":
                        self._consume_expected("BY")
                        step = self.expression()
    
                    return self._parse_do_body(
                        var_name=var_name,
                        start=start,
                        end=end,
                        step=step
                    )
    
                # --------------------------
                # SUBCASE: shorthand TO loop
                # --------------------------
                if self._peek() and self._peek().type == "TO":
                    self._consume_expected("TO")
    
                    start = NumberNode(1)
                    end = self.expression()
    
                    return self._parse_do_body(
                        var_name=var_name,
                        start=start,
                        end=end
                    )
    
            # ✅ IMPORTANT: fallback → NOT a loop variable
            # treat as infinite loop
            return self._parse_do_body()
    
        # --------------------------
        # CASE 2: infinite loop
        # --------------------------
        return self._parse_do_body()

    def _parse_do_body(self, var_name=None, mode=None,
                       iterable=None, start=None, end=None, step=None):

        body = []

        while self._peek() and self._peek().type != "ENDDO":
            stmt = self.statement()
            if stmt:
                body.append(stmt)

        self._consume_expected("ENDDO")

        return DoNode(
            var=var_name,
            mode=mode,
            iterable=iterable,
            start=start,
            end=end,
            step=step,
            body=body
        )