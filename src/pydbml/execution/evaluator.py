from pydbml.runtime.environment import Environment
from pydbml.execution.resolver import Resolver
from pydbml.expression.evaluator import ExpressionEvaluator

class Evaluator:
    """
    Handles execution logic.
    """

    def __init__(self):
        self.env = Environment()
        self.resolver = Resolver(self.env)
        self.expr_evaluator = ExpressionEvaluator(self.resolver)

    def evaluate(self, code: str):
        code = code.strip()

        if self._is_assignment(code):
            return self._handle_assignment(code)

        return self.expr_evaluator.evaluate(code)

    # --------------------------
    # Assignment
    # --------------------------
    def _handle_assignment(self, code: str):
        lhs, rhs = code.split("=", 1)
        lhs = lhs.strip()
        rhs = rhs.strip()

        # Array assignment
        if "[" in lhs and "]" in lhs:
            return self._handle_array_assignment(lhs, rhs)

        is_global = lhs.startswith("!!")
        name = lhs.replace("!", "")

        value = self.expr_evaluator.evaluate(rhs)

        self.env.set(name, value, is_global=is_global)

        return f"{name} set"

    # --------------------------
    # Array Assignment
    # --------------------------
    def _handle_array_assignment(self, lhs: str, rhs: str):
        is_global = lhs.startswith("!!")

        name_part, index_part = lhs.split("[")
        index = int(index_part.replace("]", "").strip())
        name = name_part.replace("!", "").strip()

        var = self.env.get(name, is_global=is_global)
        array_obj = var.get()

        value = self.expr_evaluator.evaluate(rhs)

        array_obj.set(int(index.value) + 1, value)

        return f"{name}[{index}] set"

    # --------------------------
    # Array Access
    # --------------------------
    def _handle_array_access(self, code: str):
        is_global = code.startswith("!!")

        name_part, index_part = code.split("[")
        index = int(index_part.replace("]", "").strip())
        name = name_part.replace("!", "").strip()

        var = self.env.get(name, is_global=is_global)
        array_obj = var.get()

        return array_obj.get(index)
    
    def _is_assignment(self, code: str) -> bool:
        """
        Detect real assignment (= but not ==, >=, <=, !=)
        """
        return "=" in code and not any(op in code for op in ["==", ">=", "<=", "!="])