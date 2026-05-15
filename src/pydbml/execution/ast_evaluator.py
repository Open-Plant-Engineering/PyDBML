from pydbml.types.primitives import Number, String, Boolean
from pydbml.types.array import Array
from pydbml.runtime.methods import MethodRegistry
from pydbml.runtime.function_loader import FunctionLoader
from pydbml.execution.return_signal import ReturnSignal
from pydbml.ast.nodes import (
    IfNode,
    LogicalOpNode,
    NotNode,
    IndexAccessNode,
    IndexAssignNode,
    ObjectNode,
    DotAccessNode, 
    DotAssignNode,
    CallNode,
    FunctionCallNode,
    FunctionDefNode, 
    ReturnNode,
)

from pydbml.utils.debug import debug


class ASTEvaluator:
    def __init__(self, env, resolver=None):
        self.env = env
        self.resolver = resolver

    def evaluate(self, node):
        if node is None:
            return None

        debug("NODE START", node)

        if isinstance(node, ReturnNode):
            value = self.evaluate(node.value)
            # special signal for return
            raise ReturnSignal(value)
        
        if isinstance(node, FunctionDefNode):
            # return last return value found
            try:
                result = None
                for stmt in node.body:
                    result = self.evaluate(stmt)
                return result
            except ReturnSignal as r:
                return r.value
            
        if isinstance(node, FunctionCallNode):
            debug("FUNCTION CALL", node.name)    
            if not hasattr(self, "resolver"):
                raise Exception("Resolver not initialized in evaluator")

            loader = FunctionLoader(self.resolver)
            func_ast = loader.load(node.name)
            return self.evaluate(func_ast)

        if isinstance(node, CallNode):
            target = self.evaluate(node.target)
            args = [self.evaluate(arg) for arg in node.args]
            debug("CALL", f"{node.method} on {target} with args {args}")
            return MethodRegistry.call(node.method, target, args)
        
        if isinstance(node, DotAccessNode):
            obj = self.evaluate(node.target)

            debug("DOT ACCESS", f"{obj}.{node.attribute}")

            if not hasattr(obj, "value") or not isinstance(obj.value, dict):
                raise TypeError("Dot access only valid on object-like structures")

            if node.attribute not in obj.value:
                raise KeyError(f"Attribute '{node.attribute}' not found")

            return obj.value[node.attribute]

        if isinstance(node, DotAssignNode):
            obj = self.evaluate(node.target)
            value = self.evaluate(node.value)

            debug("DOT ASSIGN", f"{node.attribute} = {value}")

            if not hasattr(obj, "value") or not isinstance(obj.value, dict):
                raise TypeError("Dot assignment only valid on object-like structures")

            obj.value[node.attribute] = value

            return f"{node.attribute} set"
        
        # --------------------------
        # Object creation
        # --------------------------
        if isinstance(node, ObjectNode):
            debug("OBJECT CREATE", node.type_name)

            if node.type_name == "array":
                return Array()

            if node.type_name == "string":
                return String("")

            if node.type_name == "real":
                return Number(0)

            if node.type_name == "boolean":
                return Boolean(False)

            raise TypeError(f"Unknown object type: {node.type_name}")

        # --------------------------
        # Index Assignment
        # --------------------------
        if isinstance(node, IndexAssignNode):
            debug("INDEX ASSIGN NODE", node)

            if node.target.is_global:
                var = self.env.get_global(node.target.name)
            else:
                var = self.env.get(node.target.name)

            array_obj = var.get()
            debug("ARRAY BEFORE SET", array_obj.value)

            index = self.evaluate(node.index)
            value = self.evaluate(node.value)

            debug("INDEX VALUE", index)
            debug("VALUE TO SET", value)

            array_obj.set(int(index.value), value)

            debug("ARRAY AFTER SET", array_obj.value)

            return f"{node.target.name}[{int(index.value)}] set"

        # --------------------------
        # Index Access
        # --------------------------
        if isinstance(node, IndexAccessNode):
            debug("INDEX ACCESS NODE", node)

            target = self.evaluate(node.target)
            index = self.evaluate(node.index)

            debug("TARGET ARRAY", target.value)
            debug("INDEX REQUESTED", index.value)

            result = target.get(int(index.value))

            debug("INDEX RESULT", result)

            return result

        # --------------------------
        # NOT
        # --------------------------
        if isinstance(node, NotNode):
            value = self.evaluate(node.operand)

            debug("NOT VALUE", value)

            if not isinstance(value, Boolean):
                raise TypeError("NOT requires BOOLEAN value")

            return Boolean(not value.value)

        # --------------------------
        # Logical AND / OR
        # --------------------------
        if isinstance(node, LogicalOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            debug("LOGICAL LEFT", left)
            debug("LOGICAL RIGHT", right)
            debug("OPERATOR", node.op)

            if not isinstance(left, Boolean) or not isinstance(right, Boolean):
                raise TypeError("Logical operations require BOOLEAN values")

            if node.op == "AND":
                return Boolean(left.value and right.value)

            if node.op == "OR":
                return Boolean(left.value or right.value)

        # --------------------------
        # IF Node
        # --------------------------
        if isinstance(node, IfNode):
            condition = self.evaluate(node.condition)

            debug("IF CONDITION", condition)

            if not isinstance(condition, Boolean):
                raise TypeError("IF condition must evaluate to BOOLEAN")

            if condition.value:
                debug("IF THEN EXECUTED", node.then_branch)
                return self.evaluate(node.then_branch)

            if node.else_branch is not None:
                debug("IF ELSE EXECUTED", node.else_branch)
                return self.evaluate(node.else_branch)

            return None

        # --------------------------
        # Assignment
        # --------------------------
        if node.__class__.__name__ == "AssignNode":
            value = self.evaluate(node.value)

            debug("ASSIGN", f"{node.name} = {value}")

            self.env.set(node.name, value, node.is_global)

            return f"{node.name} set"

        # --------------------------
        # Number
        # --------------------------
        if node.__class__.__name__ == "NumberNode":
            return Number(node.value)

        # --------------------------
        # String
        # --------------------------
        if node.__class__.__name__ == "StringNode":
            return String(node.value)

        # --------------------------
        # Boolean
        # --------------------------
        if node.__class__.__name__ == "BooleanNode":
            return Boolean(node.value)

        # --------------------------
        # Variable
        # --------------------------
        if node.__class__.__name__ == "VariableNode":
            if node.is_global:
                value = self.env.get_global(node.name).get()
            else:
                value = self.env.get(node.name).get()

            debug("VARIABLE RESOLVE", f"{node.name} → {value}")

            return value

        # --------------------------
        # Binary Operation
        # --------------------------
        if node.__class__.__name__ == "BinaryOpNode":
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            debug("BINOP LEFT", left)
            debug("BINOP RIGHT", right)
            debug("BINOP OP", node.op)

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
