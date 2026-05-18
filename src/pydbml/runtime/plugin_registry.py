# pydbml/runtime/plugin_registry.py

class PluginRegistry:
    def __init__(self):
        self.classes = {}
        self.functions = {}
        self.operators = {}

    def register_module(self, module):
        for name in dir(module):
            obj = getattr(module, name)

            if hasattr(obj, "_pydbml_class"):
                self.classes[name.lower()] = obj

                # ✅ scan class methods for operators
                for attr in dir(obj):
                    method = getattr(obj, attr)
                    if hasattr(method, "_pydbml_operator"):
                        for op in method._pydbml_operator_names:
                            self.operators[(name.lower(), op)] = attr

            # ✅ function
            if hasattr(obj, "_pydbml_function"):
                self.functions[name.lower()] = obj
