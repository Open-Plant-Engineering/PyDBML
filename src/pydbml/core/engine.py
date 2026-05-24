from pydbml.execution.ast_evaluator import ASTEvaluator
from pydbml.parser.parser import Parser
from pydbml.runtime.environment import Environment
from pydbml.utils.debug import debug
from pydbml.runtime.config import RuntimeConfig
from pydbml.runtime.resolver import ResourceResolver
import os, importlib.util
from pydbml.execution.signals import GoLabelSignal, ReturnSignal
from pydbml.ast.nodes import LabelNode, DoNode, IfNode, HandleNode

class Engine:
    """
    Entry point for executing PyDBML code.
    This should remain thin and delegate work.
    """

    def __init__(self):
        self.env = Environment()
        self.config = RuntimeConfig()
        self.resolver = ResourceResolver(self.config)
        self.evaluator = ASTEvaluator(self.env, self.resolver)
        self._load_plugins()

    def execute(self, code: str):
        """
        Execute a single line of PyDBML code.
        """
        parser = Parser(code)
        
        debug("CODE", code)
        ast = parser.parse()
        debug("AST", ast)

        label_map = self._collect_labels(ast)

        i = 0
        depth = 0
        result = None

        try:
        
            if not isinstance(ast, list):
                ast = [ast]

            while i < len(ast):
                stmt = ast[i]

                try:
                    result = self.evaluator.evaluate(stmt)
                    i += 1

                except GoLabelSignal as g:
                
                    if g.label not in label_map:
                        raise Exception(f"Label '{g.label}' not found")

                    target = label_map[g.label]

                    # ✅ depth validation (VERY IMPORTANT)
                    if target["depth"] > depth:
                        raise Exception(f"Invalid jump into inner block: {g.label}")

                    # ✅ perform jump
                    ast = target["nodes"]
                    i = target["index"] + 1
                    depth = target["depth"]

            return result

        except ReturnSignal as r:
            return r.value

    def _load_plugins(self):
        paths = os.getenv("PYDBML_PLUGIN_PATH", "")

        for path in paths.split(os.pathsep):
            if not path or not os.path.exists(path):
                continue

            for file in os.listdir(path):
                if file.endswith(".py") and not file.startswith("_"):
                    full_path = os.path.join(path, file)

                    spec = importlib.util.spec_from_file_location(file[:-3], full_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # ✅ THIS IS CRITICAL
                    self.evaluator.registry.register_module(module)

    def _collect_labels(self, nodes, depth=0, label_map=None):
        if label_map is None:
            label_map = {}

        for idx, stmt in enumerate(nodes):

            if isinstance(stmt, LabelNode):
                if stmt.name in label_map:
                    raise Exception(f"Duplicate label '{stmt.name}'")

                label_map[stmt.name] = {
                    "nodes": nodes,
                    "index": idx,
                    "depth": depth
                }

            # traverse nested
            if hasattr(stmt, "body") and isinstance(stmt.body, list):
                self._collect_labels(stmt.body, depth + 1, label_map)

            if isinstance(stmt, IfNode):
                if isinstance(stmt.then_branch, list):
                    self._collect_labels(stmt.then_branch, depth + 1, label_map)
                if isinstance(stmt.else_branch, list):
                    self._collect_labels(stmt.else_branch, depth + 1, label_map)

            if isinstance(stmt, HandleNode):
                for _, block in stmt.handlers:
                    self._collect_labels(block, depth + 1, label_map)
                if stmt.else_block:
                    self._collect_labels(stmt.else_block, depth + 1, label_map)

        return label_map
