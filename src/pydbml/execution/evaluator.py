from pydbml.runtime.environment import Environment
from pydbml.execution.resolver import Resolver


class Evaluator:
    """
    Handles execution logic.
    """

    def __init__(self):
        self.env = Environment()
        self.resolver = Resolver(self.env)

    def evaluate(self, code: str):
        code = code.strip()

        if "=" in code:
            return self._handle_assignment(code)

        return self._handle_lookup(code)

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

        value = self.resolver.resolve(rhs)

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

        value = self.resolver.resolve(rhs)

        array_obj.set(index, value)

        return f"{name}[{index}] set"

    # --------------------------
    # Lookup
    # --------------------------
    def _handle_lookup(self, code: str):
        # Array access
        if "[" in code and "]" in code:
            return self._handle_array_access(code)

        is_global = code.startswith("!!")
        name = code.replace("!", "")

        var = self.env.get(name, is_global=is_global)
        return var.get()

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