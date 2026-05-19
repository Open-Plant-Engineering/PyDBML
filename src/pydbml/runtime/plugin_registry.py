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
        self.extended_classes = set()
        self._load_builtins()
        self.extensions = {} 

    def register_module(self, module):
        print(f"\n[DEBUG] Registering module: {module}")
        for name in dir(module):
            obj = getattr(module, name)

            if hasattr(obj, "_pydbml_class"):
                
                print(f"[DEBUG] Found class: {obj.__name__}")
                print(f"[DEBUG] Class aliases: {obj._pydbml_class_names}")

                for cls_name in obj._pydbml_class_names:
                    self.classes[cls_name] = obj

                # ✅ scan class methods for operators
                for attr in dir(obj):
                    method = getattr(obj, attr)
                    if hasattr(method, "_pydbml_operator"):
                        for op in method._pydbml_operator_names:
                            register_operator_token(op)
                            self.operators[(name.lower(), op)] = attr

            # ✅ function
            if hasattr(obj, "_pydbml_function"):
                self.functions[name.lower()] = obj

            # --------------------------
            # ✅ EXTENSION SUPPORT (UPDATED)
            # --------------------------
            if hasattr(obj, "_pydbml_extend"):
                
                print(f"[DEBUG] Found extension class: {obj.__name__}")
                print(f"[DEBUG] Extending: {obj._pydbml_extend_names}")

                for target_name in obj._pydbml_extend_names:

                    if target_name not in self.classes:
                        raise Exception(f"Cannot extend unknown type '{target_name}'")

                    target_cls = self.classes[target_name]
                    print(f"[DEBUG] Attaching methods to {target_cls}")
                    
                    for attr in dir(obj):
                        if attr.startswith("__"):
                            continue  # ✅ skip internal methods

                        member = getattr(obj, attr)

                        if callable(member):
                        
                            # ✅ operator from extension → register token
                            if hasattr(member, "_pydbml_operator"):
                                for op in member._pydbml_operator_names:
                                    print(f"[DEBUG] Registering operator token (extension): {op}")
                                    register_operator_token(op)

                            if hasattr(member, "_pydbml_method") or hasattr(member, "_pydbml_operator"):
                                if target_cls not in self.extensions:
                                    self.extensions[target_cls] = []
                                    self.extensions[target_cls].append(obj)

                    # ✅ mark cache dirty
                    self.extended_classes.add(target_cls)

    def _load_builtins(self):
        """
        Automatically register all built-in types
        using existing decorators (@pydbml_class)
        """
        print("\n[DEBUG] Loading builtins...")

        # ✅ register each module
        self.register_module(real)
        self.register_module(string)
        self.register_module(boolean)
        self.register_module(array)

        print("[DEBUG] Builtin classes after load:", list(self.classes.keys()))
