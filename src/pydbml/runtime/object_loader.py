from pydbml.parser.parser import Parser
from pydbml.ast.nodes import (
    ObjectDefNode,
    MethodDefNode,
)


class ObjectLoader:

    def __init__(self, resolver):
        self.resolver = resolver

        # ✅ cache: name → object definition
        self._cache = {}

        # ✅ dev mode toggle (bypass cache)
        self.dev_mode = False

    # ✅ FULL cache clear
    def clear_cache(self):
        self._cache.clear()

    # ✅ optional: clear specific object only
    def clear(self, name):
        name = name.lower()
        if name in self._cache:
            del self._cache[name]

    def load(self, name):
        name = name.lower()

        # ✅ STEP 1: cache check
        if not self.dev_mode and name in self._cache:
            return self._cache[name]

        # ✅ STEP 2: resolve file
        file_path = self.resolver.resolve(name)

        if not file_path.endswith(".pdobj"):
            raise TypeError(f"{name} is not an object (.pdobj)")

        # ✅ STEP 3: read file
        try:
            with open(file_path, "r") as f:
                code = f.read()
        except Exception as e:
            raise FileNotFoundError(f"Cannot read object file: {file_path}") from e

        # ✅ STEP 4: parse
        parser = Parser(code)

        nodes = []
        while not parser._at_end():
            nodes.append(parser.statement())

        obj_def = None
        methods = {}

        # --------------------------
        # ✅ STEP 5: separate object + methods
        # --------------------------
        for node in nodes:

            if isinstance(node, ObjectDefNode):
                node.name = node.name.lower()
                obj_def = node

            elif isinstance(node, MethodDefNode):
                method_name = node.name.lower()

                if method_name not in methods:
                    methods[method_name] = []

                methods[method_name].append(node)

        # ✅ STEP 6: validation
        if not obj_def:
            raise ValueError(f"No object definition found for '{name}'")

        # ✅ attach methods
        obj_def.methods = methods

        # ✅ STEP 7: cache store
        if not self.dev_mode:
            self._cache[name] = obj_def

        return obj_def