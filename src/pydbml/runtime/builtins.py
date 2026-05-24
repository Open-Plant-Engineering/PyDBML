from pydbml.types.boolean import Boolean

class BuiltinRegistry:

    def __init__(self):
        self.functions = {}

    def register(self, name, func):
        self.functions[name.lower()] = func

    def get(self, name):
        return self.functions.get(name.lower())
