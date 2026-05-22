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
    StringNode,
    BooleanNode,
    AssignNode,
    PrintNode,
)
from pydbml.parser.parser import Parser
from pydbml.utils.debug import debug
import importlib
import importlib.util
from pydbml.runtime.plugin_registry import PluginRegistry
from pydbml.runtime.exceptions import PyDBMLError
from pydbml.runtime.error_codes import raise_error
from pydbml.debugger.debug_controller import DebugController
from pydbml.builtins.iftrue import builtin_iftrue
from pydbml.builtins.undefined import builtin_undefined
from pydbml.builtins.unset import builtin_unset
from pydbml.types.unset import UNSET
from pydbml.runtime.builtins import BuiltinRegistry

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
        self.breakpoints = {}
        self._debug_vars = set()
        self._pipe_cache = {}
        self._attr_cache = {}
        self.step_over_depth = None
        self.step_out_depth = None
        self.debug_log = []
        self.watch_vars = set()
        self.debug_controller = DebugController()
        self.interactive_mode = True
        self.builtins = BuiltinRegistry()

        self.builtins.register("iftrue", builtin_iftrue)
        self.builtins.register("undefined", builtin_undefined)
        self.builtins.register("unset", builtin_unset)

    # --------------------------
    # ✅ Builtin Registration
    # --------------------------
    def register_builtin(self, name, func):
        """
        Allow users to register custom builtins.

        func signature:
            func(evaluator, args, node)
        """
        self.builtins.register(name, func)

    def evaluate(self, node):
        try:
            if node is None:
                return None
            
            debug("NODE START", node)
            self.call_stack.append(node)
            self._trace(node)

            if isinstance(node, PrintNode):
                value = self.evaluate(node.expr)
                val = value.value if hasattr(value, "value") else value
                print(val)
                return value

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
                    
                        # ✅ HANDLE ANY
                        if condition == "ANY":
                            for stmt in block:
                                self.evaluate(stmt)
                            return None

                        # ✅ HANDLE (code1, code2) or (code1,)
                        if isinstance(condition, tuple):
                        
                            # ✅ SINGLE CODE MATCH (code1, None)
                            if len(condition) == 2 and condition[1] is None:
                                if e.code1 == condition[0]:
                                    for stmt in block:
                                        self.evaluate(stmt)
                                    return None

                            # ✅ EXACT MATCH (code1, code2)
                            elif len(condition) == 2:
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
                return self._eval_do(node)

            if isinstance(node, BreakIfNode):
                condition = self.evaluate(node.condition)
                if condition.value:
                    raise BreakSignal()
                return None

            if isinstance(node, BreakNode):
                raise BreakSignal()

            if isinstance(node, PipeStringNode):
                return self._eval_pipe_string(node)

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
                    args = [self.evaluate(arg) for arg in node.args]
                    self._construct_object(instance, obj_def, type_name, args, node)
                    return instance

                # --------------------------
                # ✅ 4. Existing file loader (unchanged)
                # --------------------------
                if type_name != "object":
                    loader = ObjectLoader(self.resolver)
                    obj_def = loader.load(type_name)
                    instance = ObjectInstance(obj_def)
                    args = [self.evaluate(arg) for arg in node.args]
                    self._construct_object(instance, obj_def, type_name, args, node)
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
                return self._eval_function_call(node)

            if isinstance(node, CallNode):
                return self._eval_method_call(node)

            # --------------------------
            # DOT ACCESS
            # --------------------------
            if isinstance(node, DotAccessNode):
                return self._eval_dot_access(node)

            # --------------------------
            # DOT ASSIGN
            # --------------------------
            if isinstance(node, DotAssignNode):
                return self._eval_dot_assign(node)

            # --------------------------
            # Index Assignment
            # --------------------------
            if isinstance(node, IndexAssignNode):
                return self._eval_index_assign(node)

            # --------------------------
            # Index Access
            # --------------------------
            if isinstance(node, IndexAccessNode):
                return self._eval_index_access(node)

            # --------------------------
            # NOT
            # --------------------------
            if isinstance(node, NotNode):
                return self._eval_not(node)

            # --------------------------
            # Logical AND / OR
            # --------------------------
            if isinstance(node, LogicalOpNode):
                return self._eval_logical(node)

            # --------------------------
            # IF Node
            # --------------------------
            if isinstance(node, IfNode):
                return self._eval_if(node)
                
            # --------------------------
            # Assignment
            # --------------------------
            if isinstance(node, AssignNode):
                return self._eval_assign(node)

            if isinstance(node, NumberNode):
                return self._eval_number(node)

            if isinstance(node, StringNode):
                return self._eval_string(node)

            if isinstance(node, BooleanNode):
                return self._eval_boolean(node)

            # ✅ NULL literal support
            if isinstance(node, VariableNode) and node.name.lower() == "null":
                return UNSET

            # --------------------------
            # Variable
            # --------------------------
            if isinstance(node, VariableNode):
                return self._eval_variable(node)

            # --------------------------
            # Binary Operation
            # --------------------------
            if isinstance(node, BinaryOpNode):
                return self._eval_binary(node)

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
                msg = str(e)
                if not msg or msg == "Ellipsis":
                    msg = "Invalid operation"

                raise raise_error(
                    "TYPE_ERROR",
                    msg,
                    node=node,
                    stack=self.call_stack.copy()
                )
            
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

    def _eval_not(self, node):
        """
        Evaluate NOT operator.
        """

        value = self.evaluate(node.operand)

        debug("NOT VALUE", value)

        if not isinstance(value, Boolean):
            raise raise_error(
                "TYPE_ERROR",
                "NOT requires BOOLEAN value",
                node=node
            )

        return Boolean(not value.value)

    def _eval_logical(self, node):
        """
        Evaluate logical AND / OR with short-circuit.
        """

        left = self.evaluate(node.left)

        # ✅ short circuit
        if node.op == "AND" and not left.value:
            return Boolean(False)

        if node.op == "OR" and left.value:
            return Boolean(True)

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

        return Boolean(left.value or right.value)

    def _eval_number(self, node):
        """Return numeric literal."""
        return Real(node.value)

    def _eval_string(self, node):
        """Return string literal."""
        return String(node.value)

    def _eval_boolean(self, node):
        """Return boolean literal."""
        return Boolean(node.value)

    def _eval_variable(self, node):
        """
        Resolve variable from environment.
        Handles NULL → UNSET.
        """

        if node.name.lower() == "null":
            return UNSET

        try:
            if node.is_global:
                value = self.env.get_global(node.name).get()
            else:
                value = self.env.get(node.name).get()

        except KeyError:
            raise raise_error(
                "NAME_ERROR",
                f"Variable '{node.name}' is not defined",
                node=node,
                stack=self.call_stack
            )

        debug("VARIABLE RESOLVE", f"{node.name} → {value}")
        return value

    def _eval_assign(self, node):
        """Assign value to variable."""

        value = self.evaluate(node.value)

        debug("ASSIGN", f"{node.name} = {value}")

        self.env.set(node.name, value, node.is_global)

        # debugger tracking
        self._debug_vars.add(node.name)

        return f"{node.name} set"



    def _execute_method(self, instance, method_node, args):

        self.env.push_scope()

        try:
            # ✅ bind THIS
            self.env.set("this", instance, False)

            # ✅ bind parameters
            for (param_name, param_type), value in zip(method_node.params, args):

                if not check_type(value, param_type):
                    raise raise_error(
                        "TYPE_ERROR",
                        f"{param_name} expects {param_type}",
                        node=method_node
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
                    raise raise_error(
                        "TYPE_ERROR",
                        "Dict keys must be convertible to int"
                    )

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

        self._method_cache[cls] = method_map
        self._operator_cache[cls] = operator_map

    def _trace(self, node):
        if not self.debug_mode:
            return

        token = getattr(node, "token", None)

        if token:
            line = token.line
            col = token.column
            msg = f"[STEP] depth={len(self.call_stack)} Line {line}:{col} → {node.__class__.__name__}"
        else:
            line = None
            msg = f"[STEP] depth={len(self.call_stack)} → {node.__class__.__name__}"

        self._append_debug_log(msg)

        current_depth = len(self.call_stack)

        should_pause = False

        # ✅ STEP OUT
        if self.step_out_depth is not None:
            if current_depth <= self.step_out_depth:
                should_pause = True
                self.step_out_depth = None

        # ✅ STEP OVER
        elif self.step_over_depth is not None:
            if current_depth <= self.step_over_depth:
                should_pause = True
                self.step_over_depth = None

        # ✅ STEP MODE
        elif self.step_mode:
            should_pause = True

        # ✅ BREAKPOINT
        elif line and line in self.breakpoints:
            condition_ast = self.breakpoints[line]

            if condition_ast is None:
                should_pause = True
            else:
                try:
                    cond_val = self.evaluate(condition_ast)

                    # ✅ must be Boolean
                    if isinstance(cond_val, Boolean) and cond_val.value:
                        should_pause = True
                    else:
                        should_pause = False

                except Exception:
                    should_pause = False

        if not should_pause:
            return

        # ✅ LOG PAUSE ONCE
        self._append_debug_log(
            f"[PAUSE] depth={current_depth}, "
            f"step_over={self.step_over_depth}, "
            f"step_out={self.step_out_depth}, "
            f"step_mode={self.step_mode}"
        )

        # ✅ SHOW WATCH VARIABLES
        self._print_watch_vars()

        # ✅ BUILD DEBUG STATE
        state = self._build_debug_state(node)

        # ✅ SEND IT TO CONTROLLER
        self.debug_controller.on_pause(state)

        # ✅ DEBUG LOOP
        while True:
            cmd = self.debug_controller.get_next_command()

            if cmd is None:
                if not self.interactive_mode:
                    self.step_mode = False
                    return
                cmd = input("(debug) ").strip()
            print(f"(debug) {cmd}")  # optional: simulate input

            self._append_debug_log(f"[CMD] {cmd}")

            # --------------------------
            # CONTINUE
            # --------------------------
            if cmd in ("c", "continue"):
                self.step_mode = False
                return

            # --------------------------
            # STEP INTO
            # --------------------------
            elif cmd in ("s", "step"):
                self.step_mode = True
                return

            # --------------------------
            # STEP OVER
            # --------------------------
            elif cmd in ("n", "next"):
                self.step_over_depth = len(self.call_stack)
                self.step_mode = False
                return

            # --------------------------
            # STEP OUT
            # --------------------------
            elif cmd in ("o", "out"):
                self.step_out_depth = len(self.call_stack) - 1
                self.step_mode = False
                return

            # --------------------------
            # WATCH ADD
            # --------------------------
            elif cmd.startswith("watch"):
                parts = cmd.split()
                if len(parts) < 2:
                    self._append_debug_log("Usage: watch <var>")
                    continue

                var_name = parts[1].lower()
                self.watch_vars.add(var_name)
                self._append_debug_log(f"[WATCH ADDED] {var_name}")
                continue

            # --------------------------
            # WATCH REMOVE
            # --------------------------
            elif cmd.startswith("unwatch"):
                parts = cmd.split()
                if len(parts) < 2:
                    print("Usage: unwatch <var>")
                    continue

                var_name = parts[1].lower()

                if var_name in self.watch_vars:
                    self.watch_vars.remove(var_name)
                    self._append_debug_log(f"[WATCH REMOVED] {var_name}")
                else:
                    self._append_debug_log(f"{var_name} not being watched")

                continue

            # --------------------------
            # PRINT VARIABLES
            # --------------------------
            elif cmd.startswith("p"):
                parts = cmd.split()

                if len(parts) == 1:
                    print("Variables:")

                    for scope in reversed(self.env._local_stack):
                        for name, var in scope.items():
                            try:
                                val = var.get()
                            except Exception:
                                val = var
                            print(f"  {name} = {val}")

                    for name, var in self.env._global.items():
                        try:
                            val = var.get()
                        except Exception:
                            val = var
                        print(f"  {name} (global) = {val}")

                    continue

                var_name = parts[1].lower()

                found = False
                for scope in reversed(self.env._local_stack):
                    if var_name in scope:
                        val = scope[var_name].get()
                        self._append_debug_log(f"{var_name} = {val}")
                        found = True
                        break

                if not found and var_name in self.env._global:
                    val = self.env._global[var_name].get()
                    self._append_debug_log(f"{var_name} (global) = {val}")
                    found = True

                if not found:
                    self._append_debug_log(f"{var_name} not found")

            # --------------------------
            # STACK TRACE
            # --------------------------
            elif cmd in ("bt", "stack"):
                self._append_debug_log("[STACK]")
                for n in reversed(self.call_stack):
                    t = getattr(n, "token", None)
                    if t:
                        self._append_debug_log(f"  Line {t.line}:{t.column} → {n.__class__.__name__}")
                    else:
                        self._append_debug_log(f"  → {n.__class__.__name__}")

            # --------------------------
            # QUIT
            # --------------------------
            elif cmd in ("q", "quit"):
                raise SystemExit("Debugger exited")
            
            # --------------------------
            # Conditional Break
            # --------------------------
            elif cmd.startswith("b "):
                # Example: b 8 if !x > 5
                parts = cmd.split(" ", 2)

                if len(parts) < 2:
                    print("Usage: b <line> [if condition]")
                    continue
                
                try:
                    line_no = int(parts[1])
                except ValueError:
                    print("Invalid line number")
                    continue
                
                condition_code = None

                if len(parts) == 3 and parts[2].startswith("if "):
                    condition_code = parts[2][3:].strip()

                self.add_breakpoint(line_no, condition_code)

                self._append_debug_log(f"[BREAKPOINT] line {line_no} condition={condition_code}")

                continue

            # --------------------------
            # Remove Conditional Break
            # --------------------------
            elif cmd.startswith("rb"):
                parts = cmd.split()

                if len(parts) < 2:
                    print("Usage: rb <line>")
                    continue
                
                line_no = int(parts[1])

                if line_no in self.breakpoints:
                    del self.breakpoints[line_no]
                    self._append_debug_log(f"[BREAKPOINT REMOVED] {line_no}")
                else:
                    self._append_debug_log("No breakpoint at that line")

                continue
            else:
                print("Commands: c(continue), s(step), n(next), o(out), p var, watch var, unwatch var, bt")

    def add_breakpoint(self, line, condition_code=None):
        if condition_code:
            # ✅ parse PyDBML expression
            parser = Parser(condition_code)
            ast = parser.parse()
            self.breakpoints[line] = ast
        else:
            self.breakpoints[line] = None

    def _eval_do(self, node):
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

                # ✅ loop variable = actual index
                self.env.set(node.var, Real(key), False)

                try:
                    eval_fn = self.evaluate
                    for stmt in node.body:
                        eval_fn(stmt)
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

    def _construct_object(self, instance, obj_def, type_name, args, node):
        
        for attr in obj_def.members:
            instance.value[attr] = UNSET

        constructor_name = type_name

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
                f"{type_name} does not accept arguments",
                node=node
            )

    def _eval_if(self, node):
        condition = self.evaluate(node.condition)

        if not isinstance(condition, Boolean):
            raise raise_error(
                "TYPE_ERROR",
                "IF condition must be BOOLEAN",
                node=node
            )

        # --------------------------
        # ✅ EXPRESSION IF
        # --------------------------
        if node.is_expression:
            if condition.value:
                return self.evaluate(node.then_branch)
            else:
                return self.evaluate(node.else_branch)
    
        # --------------------------
        # ✅ BLOCK IF
        # --------------------------
        if condition.value:
            result = None
            for stmt in node.then_branch:
                result = self.evaluate(stmt)
            return result

        # --------------------------
        # ✅ ELIF BLOCKS
        # --------------------------
        for cond, block in getattr(node, "elif_blocks", []):
            cond_val = self.evaluate(cond)

            if not isinstance(cond_val, Boolean):
                raise raise_error(
                    "TYPE_ERROR",
                    "ELSEIF condition must be BOOLEAN",
                    node=cond
                )

            if cond_val.value:
                result = None
                for stmt in block:
                    result = self.evaluate(stmt)
                return result

        # --------------------------
        # ✅ ELSE BLOCK
        # --------------------------
        if node.else_branch is not None:
            result = None
            for stmt in node.else_branch:
                result = self.evaluate(stmt)
            return result

        return None

    def _eval_binary(self, node):
        left = self.evaluate(node.left)
        
        if node.op == "AND" and not left.value:
            return Boolean(False)

        if node.op == "OR" and left.value:
            return Boolean(True)

        right = self.evaluate(node.right)

        # ✅ unwrap plugin objects
        if isinstance(left, PluginObject):
            left = left.obj

        if isinstance(right, PluginObject):
            right = right.obj

        debug("BINOP LEFT", left)
        debug("BINOP RIGHT", right)
        debug("BINOP OP", node.op)

        # ✅ get class
        cls = left.__class__

        # ✅ build cache only once
        if cls not in self._operator_cache:
            self._build_cache(cls)

        operator_map = self._operator_cache[cls]

        if node.op in operator_map:
            method = operator_map[node.op].__get__(left, cls)
            py_right = self._to_python(right)
            result = method(py_right)
            return self._to_pydbml(result)

        raise raise_error(
            "OPERATOR_ERROR",
            f"{node.op} not supported for {type(left).__name__}",
            node=node
        )

    def _eval_function_call(self, node):
        name = node.name.lower()

        # ✅ BUILTIN DISPATCH
        builtin = self.builtins.get(name)
        if builtin:
            use_raw = getattr(builtin, "_raw_args", False)

            if use_raw:
                args = node.args            # raw AST nodes
            else:
                args = [self.evaluate(arg) for arg in node.args]           # evaluated later inside builtin

            return builtin(self, args, node)

        # --------------------------
        # ✅ REGISTERED FUNCTIONS
        # --------------------------
        if name in self.registry.functions:
            func = self.registry.functions[name]

            # ✅ CASE 1: Python plugin function
            if callable(func):
                py_args = [self._to_python(self.evaluate(a)) for a in node.args]
                result = func(*py_args)
                return self._to_pydbml(result)

            # ✅ CASE 2: DSL function
            if isinstance(func, FunctionDefNode):
                func_ast = func

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

        # --------------------------
        # ✅ FILE-LOADED FUNCTION
        # --------------------------
        loader = FunctionLoader(self.resolver)
        func_ast = loader.load(node.name)

        if isinstance(func_ast, list):
            func_ast = func_ast[0]

        if not isinstance(func_ast, FunctionDefNode):    
            raise raise_error(
                "NAME_ERROR",
                f"{node.name} is not a valid function",
                node=node
            )

        arg_values = [self.evaluate(arg) for arg in node.args]

        if len(arg_values) != len(func_ast.params):
            raise raise_error(
                "ARG_COUNT",
                f"{node.name} expects {len(func_ast.params)} args, got {len(arg_values)}",
                node=node
            )

        self.env.push_scope()

        try:
            for (param_name, param_type), value in zip(func_ast.params, arg_values):
                if not check_type(value, param_type):
                    raise raise_error(
                        "TYPE_ERROR",
                        f"{param_name} expects {param_type}",
                        node=node
                    )

                self.env.set(param_name, value, is_global=False)

            result = None
            for stmt in func_ast.body:
                result = self.evaluate(stmt)

            return result

        except ReturnSignal as r:
            if not check_type(r.value, func_ast.return_type):               
                raise raise_error(
                    "RETURN_TYPE",
                    f"Expected {func_ast.return_type}, got {type(r.value).__name__}",
                    node=node
                )

            return r.value

        finally:
            self.env.pop_scope()

    def _eval_method_call(self, node):
        method_name = node.method.lower()

        # ✅ BUILTIN FIRST (IMPORTANT FIX)
        builtin = self.builtins.get(method_name)

        if builtin:
            allow_method = getattr(builtin, "_allow_method", True)
            if allow_method:
                use_raw = getattr(builtin, "_raw_args", False)

                if use_raw:
                    args = [node.target] + node.args
                else:
                    # ✅ IMPORTANT: include evaluated target
                    evaluated_target = self.evaluate(node.target)
                    args = [evaluated_target] + [self.evaluate(arg) for arg in node.args]

                return builtin(self, args, node)

        # ✅ SAFE TO EVALUATE AFTER
        target = self.evaluate(node.target)
        args = [self.evaluate(arg) for arg in node.args]

        # --------------------------
        # ✅ Case 1: Object method (DSL object)
        # --------------------------
        if isinstance(target, ObjectInstance):

            if method_name in target.definition.methods:

                candidates = target.definition.methods[method_name]

                if not isinstance(candidates, list):
                    candidates = [candidates]

                for method in candidates:
                    if len(method.params) == len(args):
                        return self._execute_method(target, method, args)

                raise raise_error(
                    "OVERLOAD_NOT_FOUND",
                    f"{method_name} with {len(args)} args",
                    node=node
                )

        # --------------------------
        # ✅ Case 2: Plugin / Python methods
        # --------------------------
        cls = target.__class__

        if cls not in self._method_cache:
            self._build_cache(cls)

        method_map = self._method_cache[cls]
        method_name_upper = method_name.upper()

        if method_name_upper in method_map:
            method = method_map[method_name_upper].__get__(target, cls)

            py_args = [self._to_python(a) for a in args]

            result = method(*py_args)

            return self._to_pydbml(result)

        # --------------------------
        # ❌ Not found
        # --------------------------
        raise raise_error(
            "METHOD_NOT_FOUND",
            f"{method_name} for type '{type(target).__name__}'",
            node=node
        )

    def _eval_dot_access(self, node):
        obj = self.evaluate(node.target)
        
        if obj is UNSET:
            return UNSET

        if isinstance(obj, PluginObject):
            obj = obj.obj

        attr_name = node.attribute.lower()

        # --------------------------
        # ✅ Plugin object
        # --------------------------
        if not isinstance(obj, ObjectInstance):
            real_attr = None

            for attr in dir(obj):
                if attr.lower() == attr_name:
                    real_attr = attr
                    break

            if real_attr is not None:
                value = getattr(obj, real_attr)

                if callable(value):
                    return value

                return self._to_pydbml(value)

        debug("DOT ACCESS", f"{obj}.{node.attribute}")

        # --------------------------
        # ✅ ObjectInstance
        # --------------------------
        if isinstance(obj, ObjectInstance):

            if node.attribute in obj.definition.members:
                return obj.value.get(node.attribute, UNSET)

            if node.attribute in obj.definition.methods:
                return ("__method__", obj, node.attribute)

            raise raise_error(
                "ATTRIBUTE_ERROR",
                f"{node.attribute} not found",
                node=node
            )

        # --------------------------
        # ✅ Array special case
        # --------------------------
        if isinstance(obj, Array):
            if node.attribute in obj.value:
                return self._to_pydbml(obj.value[node.attribute])

        raise raise_error(
            "TYPE_ERROR",
            "Dot access not supported for this type",
            node=node
        )

    def _eval_dot_assign(self, node):
        obj = self.evaluate(node.target)
        value = self.evaluate(node.value)

        debug("DOT ASSIGN", f"{node.attribute} = {value}")

        # --------------------------
        # ✅ ObjectInstance (typed)
        # --------------------------
        if isinstance(obj, ObjectInstance):

            if node.attribute not in obj.definition.members:
                raise raise_error(
                    "ATTRIBUTE_ERROR",
                    f"{node.attribute}",
                    node=node
                )

            expected_type = obj.definition.members[node.attribute]

            if value is not None and not check_type(value, expected_type):
                raise raise_error(
                    "TYPE_ERROR",
                    f"{node.attribute} expects {expected_type}",
                    node=node
                )

            obj.value[node.attribute] = value
            return value

        # --------------------------
        # ✅ fallback (dict-like)
        # --------------------------
        if hasattr(obj, "value") and isinstance(obj.value, dict):
            obj.value[node.attribute] = value
            return value

        raise raise_error(
            "TYPE_ERROR",
            "Dot assignment not supported",
            node=node
        )

    def _eval_index_access(self, node):
        array_obj = self.evaluate(node.target)

        index_val = self.evaluate(node.index)

        if not isinstance(index_val, Real):
            raise raise_error(
                "INDEX_ERROR",
                "Index must be numeric",
                node=node
            )

        index = int(index_val.value)

        # ✅ Python list fallback
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

    def _eval_index_assign(self, node):
        debug("INDEX ASSIGN NODE", node)

        target_obj = self.evaluate(node.target)
        index_val = self.evaluate(node.index).value
        value = self.evaluate(node.value)

        debug("INDEX VALUE", index_val)
        debug("VALUE TO SET", value)

        try:
            target_obj.set(int(index_val), value)
        except Exception:
            raise raise_error(
                "INDEX_ERROR",
                f"Invalid index {index_val}",
                node=node
            )

        return value

    def _eval_pipe_string(self, node):
        text = node.raw
        text = text.replace("$$", "\n")

        def replace_expr(match):
            expr_group = match.group(1)
            var_group = match.group(2)

            if expr_group is not None:
                expr_code = expr_group.strip()

                if expr_code not in self._pipe_cache:
                    parser = Parser(expr_code)
                    self._pipe_cache[expr_code] = parser.parse()

                ast = self._pipe_cache[expr_code]
                result = self.evaluate(ast)

                val = result.value if hasattr(result, "value") else result

                if isinstance(val, float) and val.is_integer():
                    val = int(val)

                return str(val)

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
    
    def _print_watch_vars(self):
        if not self.watch_vars:
            return

        for var in sorted(self.watch_vars):
            found = False

            # ✅ local scopes first
            for scope in reversed(self.env._local_stack):
                if var in scope:
                    val = scope[var].get()
                    print(f"[WATCH] {var} = {val}")
                    self.debug_log.append(f"[WATCH] {var} = {val}")
                    found = True
                    break

            # ✅ global fallback
            if not found and var in self.env._global:
                val = self.env._global[var].get()
                print(f"[WATCH] {var} = {val} (global)")
                self.debug_log.append(f"[WATCH] {var} = {val}")
                found = True

            if not found:
                print(f"[WATCH] {var} not found")
                self.debug_log.append(f"[WATCH] {var} not found")

    def _append_debug_log(self, msg,  echo=True):
        if echo:
            print(msg)
        self.debug_log.append(msg)

    def _build_debug_state(self, node):
        token = getattr(node, "token", None)

        # ✅ current location
        line = token.line if token else None
        col = token.column if token else None

        # ✅ variables
        locals_vars = {}
        for scope in self.env._local_stack:
            for name, var in scope.items():
                try:
                    val = var.get()
                except Exception:
                    val = var
                locals_vars[name] = str(val)

        globals_vars = {}
        for name, var in self.env._global.items():
            try:
                val = var.get()
            except Exception:
                val = var
            globals_vars[name] = str(val)

        # ✅ watch values
        watch = {}
        for var in self.watch_vars:
            found = False
            for scope in reversed(self.env._local_stack):
                if var in scope:
                    watch[var] = str(scope[var].get())
                    found = True
                    break

            if not found and var in self.env._global:
                watch[var] = str(self.env._global[var].get())
            elif not found:
                watch[var] = None

        # ✅ stack
        stack = []
        for n in self.call_stack:
            t = getattr(n, "token", None)
            stack.append({
                "node": n.__class__.__name__,
                "line": t.line if t else None,
                "col": t.column if t else None
            })

        return {
            "line": line,
            "column": col,
            "node": node.__class__.__name__,
            "depth": len(self.call_stack),
            "locals": locals_vars,
            "globals": globals_vars,
            "watch": watch,
            "stack": stack
        }
