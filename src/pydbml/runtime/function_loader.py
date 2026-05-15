import os
from pydbml.parser.parser import Parser


class FunctionLoader:

    def __init__(self, resolver):
        self.resolver = resolver

    def load(self, name):
        # ✅ resolve file path
        file_path = self.resolver.resolve(name)

        if not file_path.endswith(".pdfnc"):
            raise Exception(f"{name} is not a function (.pdfnc)")

        # ✅ read file
        with open(file_path, "r") as f:
            code = f.read()

        # ✅ parse using existing parser
        parser = Parser(code)
        ast = parser.parse()

        return ast