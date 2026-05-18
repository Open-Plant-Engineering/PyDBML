class ASTNode:
    def __repr__(self):
        return self.__class__.__name__ + str(self.__dict__)

# --------------------------
# Literals
# --------------------------
class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value

# --------------------------
# Variables
# --------------------------
class VariableNode(ASTNode):
    def __init__(self, name, is_global=False):
        self.name = name
        self.is_global = is_global

# --------------------------
# Assignment
# --------------------------
class AssignNode(ASTNode):
    def __init__(self, name, value, is_global=False):
        self.name = name
        self.value = value
        self.is_global = is_global

# --------------------------
# Binary Operation
# --------------------------
class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

# --------------------------
# IF Expression
# --------------------------
class IfNode:
    def __init__(self, condition, then_branch, else_branch=None, is_expression=False):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
        self.is_expression = is_expression

# --------------------------
# Logical Operations
# --------------------------
class LogicalOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class NotNode(ASTNode):
    def __init__(self, operand):
        self.operand = operand

# --------------------------
# Array Access
# --------------------------
class IndexAccessNode(ASTNode):
    def __init__(self, target, index):
        self.target = target
        self.index = index

# --------------------------
# Array Assignment
# --------------------------
class IndexAssignNode(ASTNode):
    def __init__(self, target, index, value):
        self.target = target
        self.index = index
        self.value = value

# --------------------------
# Object Creation
# --------------------------
class ObjectNode(ASTNode):
    def __init__(self, type_name, args=None):
        self.type_name = type_name
        self.args = args or []

# --------------------------
# Dot Access
# --------------------------
class DotAccessNode(ASTNode):
    def __init__(self, target, attribute):
        self.target = target
        self.attribute = attribute

# --------------------------
# Dot Assignment
# --------------------------
class DotAssignNode(ASTNode):
    def __init__(self, target, attribute, value):
        self.target = target
        self.attribute = attribute
        self.value = value

class CallNode(ASTNode):
    def __init__(self, target, method, args):
        self.target = target
        self.method = method
        self.args = args

class FunctionCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class FunctionDefNode(ASTNode):
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params          # list of (name, type)
        self.return_type = return_type
        self.body = body

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

class ObjectDefNode(ASTNode):
    def __init__(self, name, members, methods):
        self.name = name
        self.members = members    # dict {name: type}
        self.methods = methods    # dict {name: method AST}

class MethodDefNode(ASTNode):
    def __init__(self, name, body, params=None):
        self.name = name
        self.body = body
        self.params = params or []

class CommandVarNode(ASTNode):
    def __init__(self, name, is_global=False):
        self.name = name
        self.is_global = is_global
        
class PipeStringNode(ASTNode):
    def __init__(self, raw):
        self.raw = raw

class DoNode:
    def __init__(self, var=None, mode=None, iterable=None,
                 start=None, end=None, step=None, body=None):
        self.var = var          # loop variable (string)
        self.mode = mode        # "indices", "values", or None
        self.iterable = iterable

        self.start = start
        self.end = end
        self.step = step

        self.body = body or []

class BreakNode:
    pass

class BreakIfNode:
    def __init__(self, condition):
        self.condition = condition

class SkipIfNode:
    def __init__(self, condition):
        self.condition = condition

class ImportNode:
    def __init__(self, path):
        self.path = path

class HandleNode(ASTNode):
    def __init__(self, try_block, handlers=None, else_block=None):
        self.try_block = try_block              # list of statements
        self.handlers = handlers or []          # list of (condition, block)
        self.else_block = else_block            # success case

class HandleCase:
    def __init__(self, condition, block):
        self.condition = condition  # tuple OR 'ANY'
        self.block = block