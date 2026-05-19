import os
from pydbml.parser.parser import Parser


class FunctionLoader:

    def __init__(self, resolver):
        self.resolver = resolver
        self._cache = {}

        # ✅ dev flag
        self.dev_mode = False

    def clear_cache(self):
        self._cache.clear()

    def load(self, name):
        name = name.lower()

        if not self.dev_mode and name in self._cache:
            return self._cache[name]

        file_path = self.resolver.resolve(name)

        if not file_path.endswith(".pdfnc"):
            raise TypeError(f"{name} is not a function (.pdfnc)")

        with open(file_path, "r") as f:
            code = f.read()

        parser = Parser(code)
        ast = parser.parse()

        for node in ast:
            if hasattr(node, "name") and isinstance(node.name, str):
                node.name = node.name.lower()

        if not self.dev_mode:
            self._cache[name] = ast

        return ast