from pydbml.types.primitives import Number, String, Boolean
from pydbml.types.array import Array
from pydbml.types.object import ObjectInstance
from pydbml.runtime.methods import MethodRegistry
from pydbml.runtime.function_loader import FunctionLoader
from pydbml.runtime.type_system import check_type
from pydbml.execution.return_signal import ReturnSignal
from pydbml.runtime.type_system import check_type
from pydbml.runtime.object_loader import ObjectLoader
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

        if isinstance(node, ObjectNode):
        
            if node.type_name == "array":
                return Array()

            if node.type_name.lower() != "object":
                # load custom object
                try:
                    loader = ObjectLoader(self.resolver)
                except NameError:
                    raise Exception("ObjectLoader not available - import missing")
                obj_def = loader.load(node.type_name)

                instance = ObjectInstance(obj_def)

                # ✅ call constructor if exists
                if node.type_name in obj_def.methods:
                    self._execute_method(instance, obj_def.methods[node.type_name], [])

                return instance

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
        
            loader = FunctionLoader(self.resolver)
            func_ast = loader.load(node.name)

            # ✅ Validate function structure
            if not isinstance(func_ast, FunctionDefNode):
                raise Exception(f"{node.name} is not a valid function")

            # --------------------------
            # Evaluate arguments
            # --------------------------
            arg_values = [self.evaluate(arg) for arg in node.args]

            # --------------------------
            # Argument count validation
            # --------------------------
            if len(arg_values) != len(func_ast.params):
                raise Exception(
                    f"{node.name} expects {len(func_ast.params)} args, got {len(arg_values)}"
                )

            # --------------------------
            # Create new scope
            # --------------------------
            self.env.push_scope()

            try:
                # bind params
                for (param_name, param_type), value in zip(func_ast.params, arg_values):
                
                    if not check_type(value, param_type):
                        raise TypeError(...)

                    self.env.set(param_name, value, is_global=False)

                result = None

                for stmt in func_ast.body:
                    result = self.evaluate(stmt)

                return result

            except ReturnSignal as r:
            
                if not check_type(r.value, func_ast.return_type):
                    raise TypeError(...)

                return r.value

            finally:
                # ✅ always restore scope
                self.env.pop_scope()


        if isinstance(node, CallNode):
        
            target = self.evaluate(node.target)
            args = [self.evaluate(arg) for arg in node.args]

            method_name = node.method

            # --------------------------
            # ✅ Case 1: Object method
            # --------------------------
            if isinstance(target, ObjectInstance):
            
                # ✅ check object-defined methods FIRST
                if method_name in target.definition.methods:
                    method = target.definition.methods[method_name]
                    return self._execute_method(target, method, args)

            # --------------------------
            # ✅ Case 2: Generic method (PML-style)
            # --------------------------
            return MethodRegistry.call(method_name, target, args)
        
        # --------------------------
        # DOT ACCESS
        # --------------------------
        if isinstance(node, DotAccessNode):
            obj = self.evaluate(node.target)

            debug("DOT ACCESS", f"{obj}.{node.attribute}")

            # ✅ ObjectInstance
            if isinstance(obj, ObjectInstance):
            
                if node.attribute in obj.value:
                    return obj.value[node.attribute]

                if node.attribute in obj.definition.methods:
                    return ("__method__", obj, node.attribute)

                raise KeyError(f"Attribute '{node.attribute}' not found")

            # ✅ Primitive / Array support (fallback)
            if hasattr(obj, "value"):
            
                if isinstance(obj.value, dict) and node.attribute in obj.value:
                    return obj.value[node.attribute]

            raise TypeError("Dot access not supported for this type")

        # --------------------------
        # DOT ASSIGN
        # --------------------------
        if isinstance(node, DotAssignNode):
            obj = self.evaluate(node.target)
            value = self.evaluate(node.value)

            debug("DOT ASSIGN", f"{node.attribute} = {value}")

            # ✅ ObjectInstance (typed enforcement)
            if isinstance(obj, ObjectInstance):
                # ✅ attribute must exist
                if node.attribute not in obj.definition.members:
                    raise KeyError(f"Unknown member '{node.attribute}'")

                expected_type = obj.definition.members[node.attribute]

                # ✅ allow None assignment (optional design choice)
                if value is not None and not check_type(value, expected_type):
                    raise TypeError(
                        f"Member '{node.attribute}' expects {expected_type}"
                    )

                obj.value[node.attribute] = value
                return value

            # ✅ fallback (old behavior for arrays/dicts)
            if hasattr(obj, "value") and isinstance(obj.value, dict):
                obj.value[node.attribute] = value
                return value

            raise TypeError("Dot assignment not supported for this type")
        
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
    
    def _execute_method(self, instance, method_node, args):

        self.env.push_scope()

        try:
            # ✅ bind THIS
            self.env.set("this", instance, False)

            result = None

            for stmt in method_node.body:
                result = self.evaluate(stmt)

            return result

        except ReturnSignal as r:
            return r.value

        finally:
            self.env.pop_scope()