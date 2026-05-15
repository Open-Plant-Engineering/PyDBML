from pydbml.parser.parser import Parser

class ObjectLoader:

    def __init__(self, resolver):
        self.resolver = resolver

    def load(self, name):
        file_path = self.resolver.resolve(name)

        if not file_path.endswith(".pdobj"):
            raise Exception(f"{name} is not an object")

        with open(file_path) as f:
            code = f.read()

        parser = Parser(code)
        ast = parser.parse()

        return ast