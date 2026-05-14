from pydbml.execution.evaluator import Evaluator


class Engine:
    """
    Entry point for executing PyDBML code.
    This should remain thin and delegate work.
    """

    def __init__(self):
        self.evaluator = Evaluator()

    def execute(self, code: str):
        """
        Execute a single line of PyDBML code.
        """
        return self.evaluator.evaluate(code)