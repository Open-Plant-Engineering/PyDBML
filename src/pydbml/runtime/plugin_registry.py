# pydbml/runtime/plugin_registry.py

class PluginRegistry:
    def __init__(self):
        self.classes = {}
        self.functions = {}

    def register_module(self, module):
        for name in dir(module):
            obj = getattr(module, name)

            if hasattr(obj, "_pydbml_class"):
                self.classes[name.lower()] = obj

            if hasattr(obj, "_pydbml_function"):
                self.functions[name.lower()] = obj