from pydbml.types.primitives import Number, String, Boolean
from pydbml.ast.nodes import IfNode

class ASTEvaluator:
    def __init__(self, env):
        self.env = env

    def evaluate(self, node):
        if node is None:
            return None
        
        # --------------------------
        # IF Node
        # --------------------------
        if isinstance(node, IfNode):
            condition = self.evaluate(node.condition)

            if not isinstance(condition, Boolean):
                raise TypeError("IF condition must evaluate to BOOLEAN")

            if condition.value:
                return self.evaluate(node.then_branch)

            if node.else_branch is not None:
                return self.evaluate(node.else_branch)

            return None
        
        # --------------------------
        # Assignment
        # --------------------------
        if node.__class__.__name__ == "AssignNode":
            value = self.evaluate(node.value)
            self.env.set(node.name, value, node.is_global)
            return f"{node.name} set"

        # --------------------------
        # Number
        # --------------------------
        if node.__class__.__name__ == "NumberNode":
            return Number(node.value)

        if node.__class__.__name__ == "StringNode":
            return String(node.value)

        if node.__class__.__name__ == "BooleanNode":
           if isinstance(node.value, str):
               return Boolean(node.value.lower() == "true")
           return Boolean(node.value)

        # --------------------------
        # Variable
        # --------------------------
        if node.__class__.__name__ == "VariableNode":
            if node.is_global:
                return self.env.get_global(node.name).get()
            return self.env.get(node.name).get()

        # --------------------------
        # Binary operation
        # --------------------------
        if node.__class__.__name__ == "BinaryOpNode":
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if node.op == "+":
                return Number(left.value + right.value)

            if node.op == "-":
                return Number(left.value - right.value)

            if node.op == "*":
                return Number(left.value * right.value)

            if node.op == "/":
                return Number(left.value / right.value)

            if node.op == "==":
                return Boolean(left.value == right.value)

            if node.op == "!=":
                return Boolean(left.value != right.value)

            if node.op == ">":
                return Boolean(left.value > right.value)

            if node.op == "<":
                return Boolean(left.value < right.value)

            if node.op == ">=":
                return Boolean(left.value >= right.value)

            if node.op == "<=":
                return Boolean(left.value <= right.value)

        raise Exception(f"Unsupported AST node: {node}")
