# pydbml/runtime/plugin_registry.py
import pydbml.types.real as real
import pydbml.types.string as string
import pydbml.types.boolean as boolean
import pydbml.types.array as array
from pydbml.lexer.tokenizer import register_operator_token

class PluginRegistry:
    def __init__(self):
        self.classes = {}
        self.functions = {}
        self.operators = {}
        self.extensions = {}
        self.extended_classes = set()

        # ✅ track unique operators only
        self._registered_ops = set()

        self._load_builtins()

    def register_module(self, module):

        for name in dir(module):
            obj = getattr(module, name)

            # --------------------------
            # ✅ CLASS REGISTRATION
            # --------------------------
            if hasattr(obj, "_pydbml_class"):

                for cls_name in obj._pydbml_class_names:
                    cls_name = cls_name.lower()

                    # ✅ avoid silent override (safe)
                    if cls_name not in self.classes:
                        self.classes[cls_name] = obj

                # ✅ scan class operators
                for attr in dir(obj):
                    method = getattr(obj, attr)

                    if hasattr(method, "_pydbml_operator"):
                        for op in method._pydbml_operator_names:

                            # ✅ FIX: use dedicated operator cache
                            if op not in self._registered_ops:
                                register_operator_token(op)
                                self._registered_ops.add(op)

                            self.operators[(name.lower(), op)] = attr

            # --------------------------
            # ✅ FUNCTION REGISTRATION
            # --------------------------
            if hasattr(obj, "_pydbml_function"):
                # ✅ keep your current behavior (compatible)
                self.functions[name.lower()] = obj

                # ✅ OPTIONAL (safe enhancement — supports aliases if present)
                if hasattr(obj, "_pydbml_function_names"):
                    for fn_name in obj._pydbml_function_names:
                        self.functions[fn_name.lower()] = obj

            # --------------------------
            # ✅ EXTENSION SUPPORT
            # --------------------------
            if hasattr(obj, "_pydbml_extend"):

                for target_name in obj._pydbml_extend_names:
                    target_name = target_name.lower()

                    if target_name not in self.classes:
                        raise Exception(f"Cannot extend unknown type '{target_name}'")

                    target_cls = self.classes[target_name]

                    # ✅ register extension once
                    if target_cls not in self.extensions:
                        self.extensions[target_cls] = []

                    if obj not in self.extensions[target_cls]:
                        self.extensions[target_cls].append(obj)

                    # ✅ scan extension members for operators
                    for attr in dir(obj):
                        if attr.startswith("__"):
                            continue

                        member = getattr(obj, attr)

                        if callable(member) and hasattr(member, "_pydbml_operator"):
                            for op in member._pydbml_operator_names:
                                if op not in self._registered_ops:
                                    register_operator_token(op)
                                    self._registered_ops.add(op)

                    self.extended_classes.add(target_cls)

    def _load_builtins(self):
        """
        Automatically register all built-in types
        using existing decorators (@pydbml_class)
        """
        self.register_module(real)
        self.register_module(string)
        self.register_module(boolean)
        self.register_module(array)