from pydbml.parser.parser import Parser


class FunctionLoader:

    def __init__(self, resolver):
        self.resolver = resolver

    def load(self, name):
        file_path = self.resolver.resolve(name, ".pdfnc")

        with open(file_path, "r") as f:
            code = f.read()

        parser = Parser(code)
        ast = parser.parse()

        return ast