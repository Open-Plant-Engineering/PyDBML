import re
from pydbml.types.real import Real
from pydbml.types.string import String
from pydbml.types.boolean import Boolean
from pydbml.types.array import Array
from pydbml.types.object import ObjectInstance
from pydbml.types.plugin_object import PluginObject
from pydbml.types.base import PyDBMLType
from pydbml.runtime.function_loader import FunctionLoader
from pydbml.runtime.type_system import check_type
from pydbml.execution.signals import BreakSignal, ContinueSignal, GoLabelSignal, ReturnSignal
from pydbml.runtime.object_loader import ObjectLoader
from pydbml.runtime.variable import Variable
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
    ImportNode,
    HandleNode,
    GoLabelNode,
    LabelNode,
    BinaryOpNode,
    NumberNode,
    VariableNode,
)
from pydbml.parser.parser import Parser
from pydbml.utils.debug import debug
import importlib
import importlib.util
from pydbml.runtime.plugin_registry import PluginRegistry
from pydbml.runtime.exceptions import PyDBMLError
from pydbml.runtime.error_codes import raise_error

class ASTEvaluator:
    def __init__(self, env, resolver=None):
        self.env = env
        self.resolver = resolver
        self.registry = PluginRegistry()
        self._method_cache = {}
        self._operator_cache = {}
        self.call_stack = []
        self.debug_mode = False
        self.step_mode = False
        self.breakpoints = set()
        self._debug_vars = set()

    def evaluate(self, node):
        try:
            if node is None:
                return None
            
            debug("NODE START", node)
            self.call_stack.append(node)
            self._trace(node)

            if isinstance(node, GoLabelNode):
                raise GoLabelSignal(node.name)
            if isinstance(node, LabelNode):
                return None

            if callable(node):
                return node()

            if isinstance(node, HandleNode):
            
                try:
                    result = None

                    for stmt in node.try_block:
                        result = self.evaluate(stmt)

                    # ✅ success case
                    if node.else_block:
                        for stmt in node.else_block:
                            result = self.evaluate(stmt)

                    return result

                except PyDBMLError as e:
                
                    for condition, block in node.handlers:
                    
                        if condition == "ANY":
                            for stmt in block:
                                self.evaluate(stmt)
                            return None

                        if isinstance(condition, tuple):
                            if (e.code1, e.code2) == condition:
                                for stmt in block:
                                    self.evaluate(stmt)
                                return None

                    raise
                
            if isinstance(node, ImportNode):
                return self.eval_import(node)

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
                    iter_value = self.evaluate(node.iterable)

                    # unwrap variable if needed
                    if isinstance(iter_value, Variable):
                        iter_value = iter_value.get()

                    array_obj = iter_value

                    for key in sorted(array_obj.value.keys()):
                        print(f"[INDICES] {node.var} = {key}")

                        # ✅ loop variable = actual index
                        self.env.set(node.var, Real(key), False)

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
                    iter_value = self.evaluate(node.iterable)

                    # unwrap variable if needed
                    if isinstance(iter_value, Variable):
                        iter_value = iter_value.get()

                    array_obj = iter_value

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

                        self.env.set(node.var, Real(i), False)

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
            
                # ✅ PLUGIN HOOK
                type_name = node.type_name.lower()

                # --------------------------
                # ✅ 1. Plugin classes
                # --------------------------
                if type_name in self.registry.classes:
                    py_class = self.registry.classes[type_name]
                    args = [self._to_python(self.evaluate(arg)) for arg in node.args]
                    instance = py_class(*args)
                    return instance

                # --------------------------
                # ✅ 2. Built-in array
                # --------------------------
                if type_name == "array":
                    return Array()

                # --------------------------
                # ✅ 3. NEW: In-memory object definitions ✅
                # --------------------------
                if hasattr(self, "object_defs") and type_name in self.object_defs:
                    obj_def = self.object_defs[type_name]

                    instance = ObjectInstance(obj_def)

                    constructor_name = type_name
                    args = [self.evaluate(arg) for arg in node.args]

                    if constructor_name in obj_def.methods:
                    
                        methods = obj_def.methods[constructor_name]

                        if not isinstance(methods, list):
                            methods = [methods]

                        selected = None

                        for m in methods:
                            if len(m.params) == len(args):
                                selected = m
                                break
                            
                        if selected is None:
                            raise raise_error(
                                "CONSTRUCTOR_ERROR",
                                f"{constructor_name} with {len(args)} args",
                                node=node
                            )

                        self._execute_method(instance, selected, args)

                    elif len(args) > 0:
                        raise raise_error(
                            "CONSTRUCTOR_ERROR",
                            f"{node.type_name} does not accept arguments",
                            node=node
                        )

                    return instance

                # --------------------------
                # ✅ 4. Existing file loader (unchanged)
                # --------------------------
                if type_name != "object":
                
                    loader = ObjectLoader(self.resolver)
                    obj_def = loader.load(type_name)

                    instance = ObjectInstance(obj_def)

                    constructor_name = type_name
                    args = [self.evaluate(arg) for arg in node.args]

                    if constructor_name in obj_def.methods:
                    
                        methods = obj_def.methods[constructor_name]

                        selected = None

                        for m in methods:
                            if len(m.params) == len(args):
                                selected = m
                                break
                            
                        if selected is None:
                            raise raise_error(
                                "CONSTRUCTOR_ERROR",
                                f"{constructor_name} with {len(args)} args",
                                node=node
                            )

                        self._execute_method(instance, selected, args)

                    elif len(args) > 0:
                        raise raise_error(
                            "CONSTRUCTOR_ERROR",
                            f"{node.type_name} does not accept arguments",
                            node=node
                        )

                    return instance

            if isinstance(node, ReturnNode):
                value = self.evaluate(node.value)
                # special signal for return
                raise ReturnSignal(value)

            # --------------------------
            # Object Definition
            # --------------------------
            if isinstance(node, ObjectDefNode):
                name = node.name.lower()
                # ✅ store object definition
                if not hasattr(self, "object_defs"):
                    self.object_defs = {}
                self.object_defs[name] = node
                return None

            # --------------------------
            # Method Definition
            # --------------------------
            if isinstance(node, MethodDefNode):
            
                # ✅ ensure object storage exists
                if not hasattr(self, "object_defs"):
                    self.object_defs = {}

                method_name = node.name.lower()

                # ✅ attach to ALL objects that match method name (simple rule)
                for obj_name, obj_def in self.object_defs.items():
                
                    # ✅ initialize method dict if missing
                    if not hasattr(obj_def, "methods") or obj_def.methods is None:
                        obj_def.methods = {}

                    if method_name not in obj_def.methods:
                        obj_def.methods[method_name] = []

                    obj_def.methods[method_name].append(node)

                return None

            if isinstance(node, FunctionDefNode):
                name = node.name.lower()
                # ✅ store function definition
                self.registry.functions[name] = node
                return None

            if isinstance(node, FunctionCallNode):

                name = node.name.lower()

                if name in self.registry.functions:
                    func = self.registry.functions[name]

                    # --------------------------
                    # ✅ CASE 1: Python plugin function
                    # --------------------------
                    if callable(func):
                        py_args = [self._to_python(self.evaluate(a)) for a in node.args]
                        result = func(*py_args)
                        return self._to_pydbml(result)

                    # --------------------------
                    # ✅ CASE 2: DSL function (FunctionDefNode)
                    # --------------------------
                    if isinstance(func, FunctionDefNode):
                        func_ast = func
                        # evaluate arguments
                        arg_values = [self.evaluate(arg) for arg in node.args]
                        if len(arg_values) != len(func_ast.params):
                            raise raise_error(
                                "ARG_COUNT",
                                f"{name} expects {len(func_ast.params)} args, got {len(arg_values)}",
                                node=node
                            )

                        self.env.push_scope()
                        try:
                            # bind parameters
                            for (param_name, param_type), value in zip(func_ast.params, arg_values):
                                self.env.set(param_name, value, is_global=False)

                            result = None

                            for stmt in func_ast.body:
                                result = self.evaluate(stmt)

                            return result

                        except ReturnSignal as r:
                            return r.value

                        finally:
                            self.env.pop_scope()

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

                print(f"[DEBUG] Calling method '{method_name}'")

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
                # ✅ FAST CACHE METHOD LOOKUP (NEW)
                # --------------------------
                cls = target.__class__
                
                # build cache once
                self._build_cache(cls)
                
                method_map = self._method_cache[cls]
                method_name_upper = method_name.upper()
                
                if method_name_upper in method_map:
                    # ✅ bind method to instance
                    method = method_map[method_name_upper].__get__(target, cls)
                
                    py_args = [self._to_python(a) for a in args]
                
                    result = method(*py_args)
                
                    return self._to_pydbml(result)

                raise raise_error(
                    "METHOD_NOT_FOUND",
                    f"{method_name} for type '{type(target).__name__}'",
                    node=node
                )

            # --------------------------
            # DOT ACCESS
            # --------------------------
            if isinstance(node, DotAccessNode):
                obj = self.evaluate(node.target)

                if isinstance(obj, PluginObject):
                    obj = obj.obj

                attr_name = node.attribute.lower()

                # ✅ PLUGIN OBJECT SUPPORT (case-insensitive)
                if not isinstance(obj, ObjectInstance):
                    real_attr = None

                    for attr in dir(obj):
                        if attr.lower() == attr_name:
                            real_attr = attr
                            break
                        
                    if real_attr is not None:
                        value = getattr(obj, real_attr)

                        # ✅ methods allowed (checked later)
                        if callable(value):
                            return value

                        # ✅ attributes allowed
                        return self._to_pydbml(value)

                # ✅ Other LOGIC
                debug("DOT ACCESS", f"{obj}.{node.attribute}")

                # ✅ ObjectInstance
                if isinstance(obj, ObjectInstance):
                
                    if node.attribute in obj.value:
                        return self._to_pydbml(obj.value[node.attribute])

                    if node.attribute in obj.definition.methods:
                        return ("__method__", obj, node.attribute)

                    raise raise_error(
                        "ATTRIBUTE_ERROR",
                        f"{node.attribute} not found",
                        node=node
                    )

                # --------------------------
                # ✅ Array supports dot access (IMPORTANT FIX)
                # --------------------------
                if isinstance(obj, Array):
                    if node.attribute in obj.value:
                        return self._to_pydbml(obj.value[node.attribute])

                raise raise_error(
                    "TYPE_ERROR",
                    "Dot access not supported for this type",
                    node=node
                )

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
                        raise raise_error(
                            "ATTRIBUTE_ERROR",
                            f"{node.attribute}",
                            node=node
                        )

                    expected_type = obj.definition.members[node.attribute]

                    # ✅ allow None assignment (optional design choice)
                    if value is not None and not check_type(value, expected_type):
                        raise raise_error(
                            "TYPE_ERROR",
                            f"{node.attribute} expects {expected_type}",
                            node=node
                        )

                    obj.value[node.attribute] = value
                    return value

                # ✅ fallback (old behavior for arrays/dicts)
                if hasattr(obj, "value") and isinstance(obj.value, dict):
                    obj.value[node.attribute] = value
                    return value

                raise raise_error(
                    "TYPE_ERROR",
                    "Dot assignment not supported",
                    node=node
                )

            # --------------------------
            # Index Assignment
            # --------------------------
            if isinstance(node, IndexAssignNode):
                debug("INDEX ASSIGN NODE", node)

                # ✅ evaluate target (this handles nested arrays properly)
                target_obj = self.evaluate(node.target)

                index_val = self.evaluate(node.index).value
                value = self.evaluate(node.value)

                debug("INDEX VALUE", index_val)
                debug("VALUE TO SET", value)

                # ✅ actual assignment
                try:
                    target_obj.set(int(index_val), value)
                except Exception:
                    raise raise_error(
                        "INDEX_ERROR",
                        f"Invalid index {index_val}",
                        node=node
                    )

                return value

            # --------------------------
            # Index Access
            # --------------------------
            if isinstance(node, IndexAccessNode):
                array_obj = self.evaluate(node.target)

                index_val = self.evaluate(node.index)
                if not isinstance(index_val, Real):
                    raise raise_error(
                        "INDEX_ERROR",
                        "Index must be numeric",
                        node=node
                    )
                index = int(index_val.value)

                if isinstance(array_obj, list):
                    return self._to_pydbml(array_obj[index - 1])

                try:
                    return array_obj.get(index)
                except Exception:
                    raise raise_error(
                        "INDEX_ERROR",
                        f"{index}",
                        node=node
                    )

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
                    raise raise_error(
                        "TYPE_ERROR",
                        "Logical operations require BOOLEAN values",
                        node=node
                    )

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
                    raise raise_error(
                        "TYPE_ERROR",
                        "IF condition must be BOOLEAN",
                        node=node
                    )

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

                # ✅ TRACK VARIABLE FOR DEBUGGER
                self._debug_vars.add(node.name)

                return f"{node.name} set"

            # --------------------------
            # Number
            # --------------------------
            if isinstance(node, NumberNode):
                return Real(node.value)

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
            if isinstance(node, VariableNode):
                try:
                    if node.is_global:
                        value = self.env.get_global(node.name).get()
                    else:
                        value = self.env.get(node.name).get()
                except KeyError:
                    # ✅ auto initialize numeric variable
                    value = Real(0)
                    self.env.set(node.name, value, node.is_global)

                debug("VARIABLE RESOLVE", f"{node.name} → {value}")
                return value

            # --------------------------
            # Binary Operation
            # --------------------------
            if isinstance(node, BinaryOpNode):
                left = self.evaluate(node.left)
                right = self.evaluate(node.right)

                # ✅ unwrap plugin objects
                if isinstance(left, PluginObject):
                    left = left.obj

                if isinstance(right, PluginObject):
                    right = right.obj

                debug("BINOP LEFT", left)
                debug("BINOP RIGHT", right)
                debug("BINOP OP", node.op)

                # =====================================================
                # ✅ FAST OPERATOR LOOKUP (NEW)
                # =====================================================
                cls = left.__class__

                self._build_cache(cls)

                operator_map = self._operator_cache[cls]

                if node.op in operator_map:
                    # ✅ bind method
                    method = operator_map[node.op].__get__(left, cls)
                    py_right = self._to_python(right)
                    result = method(py_right)
                    return self._to_pydbml(result)

                
                raise raise_error(
                    "OPERATOR_ERROR",
                    f"{node.op} not supported for {type(left).__name__}",
                    node=node
                )

        except Exception as e:
            # ✅ control flow → never touch
            if isinstance(e, (ReturnSignal, BreakSignal, ContinueSignal, GoLabelSignal)):
                raise
            
            # ✅ DSL error → keep
            if isinstance(e, PyDBMLError):
                e.node = node if not e.node else e.node
                e.stack = self.call_stack.copy()
                raise
            
            # ✅ Python semantic/runtime errors → keep as-is
            if isinstance(e, (KeyError, TypeError, ValueError)):
                raise
            
            # ✅ only unexpected/internal errors → wrap
            raise raise_error(
                "INTERNAL",
                str(e),
                node=node,
                stack=self.call_stack.copy()
            )

        finally:
            if self.call_stack:
                self.call_stack.pop()

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

    def eval_import(self, node):
        path = node.path

        # ✅ file path
        if path.endswith(".py") or "/" in path or "\\" in path:
            spec = importlib.util.spec_from_file_location("plugin_mod", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            module = importlib.import_module(path)

        self.registry.register_module(module)

    def _to_python(self, value):
        if isinstance(value, PluginObject):
            return value.obj
        if isinstance(value, Real):
            val = value.value
            if isinstance(val, float) and val.is_integer():
                return int(val)   # ✅ remove .0
            return val
        if isinstance(value, String):
            return value.value
        if isinstance(value, Boolean):
            return value.value
        if isinstance(value, Array):
            return {
                k: self._to_python(v)
                for k, v in value.value.items()
            }
        return value

    def _to_pydbml(self, value):
        if value is None:
            return None

        # ✅ primitives FIRST
        if isinstance(value, bool):
            return Boolean(value)
        if isinstance(value, (int, float)):
            return Real(float(value))
        if isinstance(value, str):
            return String(value)
        # ✅ dict FIRST (important)
        if isinstance(value, dict):
            arr = Array()
            for k, v in value.items():
                try:
                    idx = int(k)
                except Exception:
                    raise TypeError("Dict keys must be convertible to int")

                arr.set(idx, self._to_pydbml(v))  # ✅ recursive
            return arr
        # ✅ list / tuple / set AFTER dict
        if isinstance(value, (list, tuple, set)):
            arr = Array()
            for i, v in enumerate(value, 1):   # ✅ enumerate ONLY
                arr.set(i, self._to_pydbml(v)) # ✅ recursive
            return arr
        
        if isinstance(value, PluginObject):
            return value
        
        if not isinstance(value, PyDBMLType) and not isinstance(value, (int, float, bool, str, dict, list, tuple, set, type(None))):
            return PluginObject(value)

        return value
    
    def _build_cache(self, cls):

        print(f"[DEBUG] Building cache for: {cls}")

        method_map = {}
        operator_map = {}

        # ✅ STEP 1: BUILTIN METHODS (from class)
        for attr in dir(cls):
            member = getattr(cls, attr)

            if callable(member):

                if hasattr(member, "_pydbml_method"):
                    for name in member._pydbml_method_names:
                        method_map[name] = member

                if hasattr(member, "_pydbml_operator"):
                    for symbol in member._pydbml_operator_names:
                        operator_map[symbol] = member

        # ✅ STEP 2: EXTENSIONS (apply AFTER builtins)
        ext_list = self.registry.extensions.get(cls, [])

        for ext_cls in ext_list:

            for attr in dir(ext_cls):
                if attr.startswith("__"):
                    continue

                member = getattr(ext_cls, attr)

                if not callable(member):
                    continue

                # ✅ METHODS
                if hasattr(member, "_pydbml_method"):
                    for name in member._pydbml_method_names:
                        method_map[name] = member

                # ✅ OPERATORS
                if hasattr(member, "_pydbml_operator"):

                    for symbol in member._pydbml_operator_names:

                        override = getattr(member, "_pydbml_operator_override", False)

                        # ✅ DO NOT override builtins unless explicit
                        if symbol in operator_map and not override:
                            continue

                        operator_map[symbol] = member

        print(f"[DEBUG] Methods found for {cls}: {list(method_map.keys())}")
        print(f"[DEBUG] Operators found for {cls}: {list(operator_map.keys())}")

        self._method_cache[cls] = method_map
        self._operator_cache[cls] = operator_map
    
    def _trace(self, node):
        if not self.debug_mode:
            return

        token = getattr(node, "token", None)

        if token:
            line = token.line
            col = token.column
            print(f"[STEP] Line {line}:{col} → {node.__class__.__name__}")
        else:
            line = None
            print(f"[STEP] → {node.__class__.__name__}")

        # ✅ break condition
        should_pause = self.step_mode or (line in self.breakpoints if line else False)

        if not should_pause:
            return

        # ✅ interactive debugger loop
        while True:
            cmd = input("(debug) ").strip()

            if cmd in ("c", "continue"):
                self.step_mode = False
                return

            elif cmd in ("s", "step"):
                self.step_mode = True
                return

            elif cmd.startswith("p"):
                parts = cmd.split()
            
                # ✅ print all variables
                if len(parts) == 1:
                    print("Variables:")
            
                    # ✅ local scopes (inner → outer)
                    for scope in reversed(self.env._local_stack):
                        for name, var in scope.items():
                            try:
                                val = var.get()
                            except Exception:
                                val = var
                            print(f"  {name} = {val}")
            
                    # ✅ global variables
                    for name, var in self.env._global.items():
                        try:
                            val = var.get()
                        except Exception:
                            val = var
                        print(f"  {name} (global) = {val}")
            
                    continue
                
                # ✅ print specific variable
                var_name = parts[1].lower()
            
                # ✅ check local first
                found = False
                for scope in reversed(self.env._local_stack):
                    if var_name in scope:
                        val = scope[var_name].get()
                        print(f"{var_name} = {val}")
                        found = True
                        break
                    
                # ✅ fallback global
                if not found and var_name in self.env._global:
                    val = self.env._global[var_name].get()
                    print(f"{var_name} (global) = {val}")
                    found = True
            
                if not found:
                    print(f"{var_name} not found")

            elif cmd in ("q", "quit"):
                raise SystemExit("Debugger exited")
            
            elif cmd in ("bt", "stack"):
                print("Call stack:")
                for n in reversed(self.call_stack):
                    t = getattr(n, "token", None)
                    if t:
                        print(f"  Line {t.line}:{t.column} → {n.__class__.__name__}")
                    else:
                        print(f"  → {n.__class__.__name__}")
                        
            else:
                print("Commands: c(continue), s(step), p var, q(quit)")

    def add_breakpoint(self, line):
        self.breakpoints.add(line)