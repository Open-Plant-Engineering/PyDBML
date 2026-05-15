from pydbml.parser.parser import Parser
from pydbml.ast.nodes import ( 
    ObjectDefNode,
    MethodDefNode,
)
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

        nodes = []

        # ✅ collect ALL statements
        while not parser._at_end():
            nodes.append(parser.statement())

        obj_def = None
        methods = {}

        # --------------------------
        # Separate object + methods
        # --------------------------
        for node in nodes:

            if isinstance(node, ObjectDefNode):
                obj_def = node

            if isinstance(node, MethodDefNode):
                if node.name not in methods:
                    methods[node.name] = []
                methods[node.name].append(node)

        if not obj_def:
            raise Exception(f"No object definition found for {name}")

        # ✅ attach methods
        obj_def.methods = methods

        return obj_def