import re
from pydbml.types.primitives import Number, String, Boolean
from pydbml.types.array import Array
from pydbml.types.object import ObjectInstance
from pydbml.runtime.methods import MethodRegistry
from pydbml.runtime.function_loader import FunctionLoader
from pydbml.runtime.type_system import check_type
from pydbml.execution.return_signal import ReturnSignal
from pydbml.execution.signals import BreakSignal, ContinueSignal
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
    PipeStringNode,
    CommandVarNode,
    BreakNode,
    BreakIfNode,
    DoNode,
    SkipIfNode,
    ObjectDefNode,
    MethodDefNode,
)
from pydbml.parser.parser import Parser
from pydbml.lexer.tokenizer import tokenize
from pydbml.utils.debug import debug


class ASTEvaluator:
    def __init__(self, env, resolver=None):
        self.env = env
        self.resolver = resolver

    def evaluate(self, node):
        if node is None:
            return None

        debug("NODE START", node)
        if isinstance(node, SkipIfNode):
        
            # ✅ standalone skip
            if node.condition is None:
                raise ContinueSignal()

            # ✅ conditional skip
            condition = self.evaluate(node.condition)
            if condition.value:
                raise ContinueSignal()
            return None

        if isinstance(node, list):
            result = None
            for stmt in node:
                result = self.evaluate(stmt)
            return result

        if isinstance(node, DoNode):
        
            print("\n=== DO LOOP START ===")
            print("MODE:", node.mode)

            # --------------------------
            # ✅ 1. INDICES LOOP
            # --------------------------
            if node.mode == "indices":
                array_obj = self.env.get(node.iterable).get()

                for key in sorted(array_obj.value.keys()):
                    print(f"[INDICES] {node.var} = {key}")

                    # ✅ loop variable = actual index
                    self.env.set(node.var, Number(key), False)

                    try:
                        for stmt in node.body:
                            self.evaluate(stmt)
                    except ContinueSignal:
                        continue
                    except BreakSignal:
                        break
                    
                return None

            # --------------------------
            # ✅ 2. VALUES LOOP
            # --------------------------
            if node.mode == "values":
                array_obj = self.env.get(node.iterable).get()

                for val in array_obj.value.values():
                    print(f"[VALUES] {node.var} = {val}")

                    # ✅ loop variable = value
                    self.env.set(node.var, val, False)

                    try:
                        for stmt in node.body:
                            self.evaluate(stmt)
                    except ContinueSignal:
                        continue
                    except BreakSignal:
                        break
                    
                return None

            # --------------------------
            # ✅ 3. RANGE LOOP
            # --------------------------
            if node.start is not None:
            
                start_val = self.evaluate(node.start).value
                end_val = self.evaluate(node.end).value
                step_val = self.evaluate(node.step).value if node.step else 1

                i = start_val

                while True:
                
                    if step_val > 0 and i > end_val:
                        break
                    if step_val < 0 and i < end_val:
                        break
                    
                    print(f"[RANGE] {node.var} = {i}")

                    self.env.set(node.var, Number(i), False)

                    try:
                        for stmt in node.body:
                            self.evaluate(stmt)
                    except ContinueSignal:
                        i += step_val
                        continue
                    except BreakSignal:
                        break
                    
                    i += step_val

                return None

            # --------------------------
            # ✅ 4. INFINITE LOOP
            # --------------------------
            while True:
                try:
                    for stmt in node.body:
                        self.evaluate(stmt)
                except ContinueSignal:
                    continue
                except BreakSignal:
                    break
                
            return None

        if isinstance(node, BreakIfNode):
            condition = self.evaluate(node.condition)
            if condition.value:
                raise BreakSignal()
            return None

        if isinstance(node, BreakNode):
            raise BreakSignal()
        
        if isinstance(node, PipeStringNode):
            text = node.raw

            # ✅ newline support
            text = text.replace("$$", "\n")

            def replace_expr(match):
                expr_group = match.group(1)   # $!(...)
                var_group = match.group(2)    # $!x or $!!x

                # --------------------------
                # ✅ CASE 1: Expression
                # --------------------------
                if expr_group is not None:
                    expr_code = expr_group.strip()
                    
                    parser = Parser(expr_code)
                    ast = parser.parse()

                    result = self.evaluate(ast)

                    val = result.value if hasattr(result, "value") else result

                    if isinstance(val, float) and val.is_integer():
                        val = int(val)

                    return str(val)

                # --------------------------
                # ✅ CASE 2: Variable
                # --------------------------
                expr = var_group

                is_global = expr.startswith("!")
                expr = expr.lstrip("!")

                parts = expr.split(".")

                if is_global:
                    value = self.env.get_global(parts[0]).get()
                else:
                    value = self.env.get(parts[0]).get()

                for attr in parts[1:]:
                    if isinstance(value, ObjectInstance):
                        value = value.value[attr]
                    else:
                        value = value.get(attr)

                val = value.value if hasattr(value, "value") else value

                if isinstance(val, float) and val.is_integer():
                    val = int(val)

                return str(val)

            text = re.sub(
                r"\$\!\((.*?)\)|\$\!(\!?[a-zA-Z_][a-zA-Z0-9_.]*)",
                replace_expr,
                text
            )

            return String(text)
        
        if isinstance(node, CommandVarNode):
            if node.is_global:
                value = self.env.get_global(node.name).get()
            else:
                value = self.env.get(node.name).get()
            debug("COMMAND VAR", f"{node.name} → {value} (global={node.is_global})")
            return value
        
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
                method_name = node.type_name.lower()
                
                if method_name in obj_def.methods:
                    methods = obj_def.methods[method_name]
                
                    if not isinstance(methods, list):
                        methods = [methods]
                
                    # ✅ constructor must have 0 params
                    for method in methods:
                        if len(method.params) == 0:
                            self._execute_method(instance, method, [])
                            break

                return instance

        if isinstance(node, ReturnNode):
            value = self.evaluate(node.value)
            # special signal for return
            raise ReturnSignal(value)
        
        # --------------------------
        # Object Definition
        # --------------------------
        if isinstance(node, ObjectDefNode):
            # ✅ definition only, no runtime execution
            return None

        # --------------------------
        # Method Definition
        # --------------------------
        if isinstance(node, MethodDefNode):
            # ✅ definition only, no runtime execution
            return None
        
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
            if isinstance(func_ast, list):
                func_ast = func_ast[0]

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

            method_name = node.method.lower()

            # --------------------------
            # ✅ Case 1: Object method
            # --------------------------
            if isinstance(target, ObjectInstance):
            
                # ✅ check object-defined methods FIRST
                if method_name in target.definition.methods:
                
                    candidates = target.definition.methods[method_name]

                    # ✅ normalize to list
                    if not isinstance(candidates, list):
                        candidates = [candidates]

                    # ✅ select by argument count
                    for method in candidates:
                        if len(method.params) == len(args):
                            return self._execute_method(target, method, args)

                    raise Exception(
                        f"No matching overload for {method_name} with {len(args)} args"
                    )
                    
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
            array_obj = self.evaluate(node.target)
            index = int(self.evaluate(node.index).value)
        
            return array_obj.get(index)

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
        
            if not isinstance(condition, Boolean):
                raise TypeError("IF condition must be BOOLEAN")
        
            # ✅ Expression IF
            if node.is_expression:
                if condition.value:
                    result = self.evaluate(node.then_branch)
                else:
                    result = self.evaluate(node.else_branch)
        
                return result
        
            # ✅ Block IF
            if condition.value:
                result = None
                for stmt in node.then_branch:
                    result = self.evaluate(stmt)
                return result
        
            if node.else_branch is not None:
                result = None
                for stmt in node.else_branch:
                    result = self.evaluate(stmt)
                return result
        
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
            try:
                if node.is_global:
                    value = self.env.get_global(node.name).get()
                else:
                    value = self.env.get(node.name).get()
            except KeyError:
                # ✅ auto initialize numeric variable
                value = Number(0)
                self.env.set(node.name, value, node.is_global)
        
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
            
            if node.op == "&":
                def fmt(v):
                    if isinstance(v, float) and v.is_integer():
                        return str(int(v))
                    return str(v)
                return String(fmt(left.value) + fmt(right.value))

        raise Exception(f"Unsupported AST node: {node}")
    
    def _execute_method(self, instance, method_node, args):

        self.env.push_scope()

        try:
            # ✅ bind THIS
            self.env.set("this", instance, False)

            # ✅ bind parameters
            for (param_name, param_type), value in zip(method_node.params, args):

                if not check_type(value, param_type):
                    raise TypeError(
                        f"{param_name} expects {param_type}"
                    )

                self.env.set(param_name, value, False)

            result = None

            for stmt in method_node.body:
                result = self.evaluate(stmt)

            return result

        except ReturnSignal as r:
            return r.value

        finally:
            self.env.pop_scope()