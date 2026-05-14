class ASTNode:
    pass


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
class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
