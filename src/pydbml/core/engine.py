from pydbml.execution.ast_evaluator import ASTEvaluator
from pydbml.parser.parser import Parser
from pydbml.runtime.environment import Environment
from pydbml.utils.debug import debug
from pydbml.runtime.config import RuntimeConfig
from pydbml.runtime.resolver import ResourceResolver


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

    def execute(self, code: str):
        """
        Execute a single line of PyDBML code.
        """
        parser = Parser(code)
        
        debug("CODE", code)
        ast = parser.parse()
        debug("AST", ast)

        result = None
        if isinstance(ast, list):
            for stmt in ast:
                result = self.evaluator.evaluate(stmt)
        else:
            result = self.evaluator.evaluate(ast)

        return result
        