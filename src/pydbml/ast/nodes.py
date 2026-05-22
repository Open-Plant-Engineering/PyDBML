class ASTNode:
    def __init__(self, token=None):
        self.token = token

    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if k != "token")
        return f"{self.__class__.__name__}({fields})"

# --------------------------
# Literals
# --------------------------
class NumberNode(ASTNode):
    def __init__(self, value, token=None):
        super().__init__(token)
        self.value = value

class StringNode(ASTNode):
    def __init__(self, value, token=None):
        super().__init__(token)
        self.value = value

class BooleanNode(ASTNode):
    def __init__(self, value, token=None):
        super().__init__(token)
        self.value = value

# --------------------------
# Variables
# --------------------------
class VariableNode(ASTNode):
    def __init__(self, name, is_global=False,  token=None):
        super().__init__(token)
        self.name = name
        self.is_global = is_global

# --------------------------
# Assignment
# --------------------------
class AssignNode(ASTNode):
    def __init__(self, name, value, is_global=False, token=None):
        super().__init__(token)
        self.name = name
        self.value = value
        self.is_global = is_global

# --------------------------
# Binary Operation
# --------------------------
class BinaryOpNode(ASTNode):
    """
    Represents a binary operation.

    Example:
        a + b
        x * y

    Fields:
        left   → left AST node
        op     → operator string ('+', '-', etc.)
        right  → right AST node
    """
    def __init__(self, left, op, right, token=None):
        super().__init__(token)
        self.left = left
        self.op = op
        self.right = right

# --------------------------
# IF Expression
# --------------------------
class IfNode(ASTNode):
    """
    Represents both expression and block IF.

    Modes:
        is_expression = True:
            IF cond THEN a ELSE b

        is_expression = False:
            IF cond THEN
                ...
            ENDIF
    """
    def __init__(
        self,
        condition,
        then_branch,
        else_branch,
        is_expression=False,
        elif_blocks=None,
        token=None,
    ):
        super().__init__(token)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        self.is_expression = is_expression
        self.elif_blocks = elif_blocks or []

# --------------------------
# Logical Operations
# --------------------------
class LogicalOpNode(ASTNode):
    def __init__(self, left, op, right, token=None):
        super().__init__(token)
        self.left = left
        self.op = op
        self.right = right

class NotNode(ASTNode):
    def __init__(self, operand, token=None):
        super().__init__(token)
        self.operand = operand

# --------------------------
# Array Access
# --------------------------
class IndexAccessNode(ASTNode):
    def __init__(self, target, index, token=None):
        super().__init__(token)
        self.target = target
        self.index = index

# --------------------------
# Array Assignment
# --------------------------
class IndexAssignNode(ASTNode):
    def __init__(self, target, index, value, token=None):
        super().__init__(token)
        self.target = target
        self.index = index
        self.value = value

# --------------------------
# Object Creation
# --------------------------
class ObjectNode(ASTNode):
    def __init__(self, type_name, args=None, token=None):
        super().__init__(token)
        self.type_name = type_name
        self.args = list(args) if args else []

# --------------------------
# Dot Access
# --------------------------
class DotAccessNode(ASTNode):
    def __init__(self, target, attribute, token=None):
        super().__init__(token)
        self.target = target
        self.attribute = attribute

# --------------------------
# Dot Assignment
# --------------------------
class DotAssignNode(ASTNode):
    def __init__(self, target, attribute, value, token=None):
        super().__init__(token)
        self.target = target
        self.attribute = attribute
        self.value = value

class CallNode(ASTNode):
    def __init__(self, target, method, args, token=None):
        super().__init__(token)
        self.target = target
        self.method = method
        self.args = args

class FunctionCallNode(ASTNode):
    def __init__(self, name, args, token=None):
        super().__init__(token)
        self.name = name
        self.args = args

class FunctionDefNode(ASTNode):
    def __init__(self, name, params, return_type, body, token=None):
        super().__init__(token)
        self.name = name
        self.params = params          # list of (name, type)
        self.return_type = return_type
        self.body = body

class ReturnNode(ASTNode):
    def __init__(self, value, token=None):
        super().__init__(token)
        self.value = value

class ObjectDefNode(ASTNode):
    def __init__(self, name, members, methods, token=None):
        super().__init__(token)
        self.name = name
        self.members = members    # dict {name: type}
        self.methods = methods    # dict {name: method AST}

class MethodDefNode(ASTNode):
    def __init__(self, name, body, params=None, token=None):
        super().__init__(token)
        self.name = name
        self.body = body
        self.params = params or []

class CommandVarNode(ASTNode):
    def __init__(self, name, is_global=False, token=None):
        super().__init__(token)
        self.name = name
        self.is_global = is_global
        
class PipeStringNode(ASTNode):
    def __init__(self, raw, token=None):
        super().__init__(token)
        self.raw = raw

class DoNode(ASTNode):
    """
    Represents loop constructs.

    Modes:
        indices loop
        values loop
        range loop
        infinite loop
    """
    def __init__(self, var=None, mode=None, iterable=None,
                 start=None, end=None, step=None, body=None, token=None):
        super().__init__(token)
        self.var = var          # loop variable (string)
        self.mode = mode        # "indices", "values", or None
        self.iterable = iterable

        self.start = start
        self.end = end
        self.step = step

        self.body = body or []

class BreakNode(ASTNode):
    def __init__(self, token=None):
        super().__init__(token)

class BreakIfNode(ASTNode):
    def __init__(self, condition, token=None):
        super().__init__(token)
        self.condition = condition

class SkipIfNode(ASTNode):
    def __init__(self, condition, token=None):
        super().__init__(token)
        self.condition = condition

class ImportNode(ASTNode):
    def __init__(self, path, token=None):
        super().__init__(token)
        self.path = path

class HandleNode(ASTNode):
    def __init__(self, try_block, handlers=None, else_block=None, token=None):
        super().__init__(token)
        self.try_block = try_block              # list of statements
        self.handlers = handlers or []          # list of (condition, block)
        self.else_block = else_block            # success case

class LabelNode(ASTNode):
    def __init__(self, name, token=None):
        super().__init__(token)
        self.name = name

class GoLabelNode(ASTNode):
    def __init__(self, name, token=None):
        super().__init__(token)
        self.name = name

class PrintNode(ASTNode):
    def __init__(self, expr, token=None):
        super().__init__(token)
        self.expr = expr
