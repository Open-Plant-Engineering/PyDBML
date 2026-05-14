from pydbml.types.primitives import Number, String


class ExpressionEvaluator:
    """
    Handles simple binary expressions like:
    !x + 5
    """

    def __init__(self, resolver):
        self.resolver = resolver

    def evaluate(self, expr: str):
        expr = expr.strip()

        # Supported operators
        operators = ["+", "-", "*", "/"]

        for op in operators:
            if op in expr:
                left, right = expr.split(op, 1)
                left_val = self.resolver.resolve(left.strip())
                right_val = self.resolver.resolve(right.strip())

                return self._apply_operator(left_val, right_val, op)

        # no operator → simple value
        return self.resolver.resolve(expr)

    def _apply_operator(self, left, right, op):

        # Number operations
        if isinstance(left, Number) and isinstance(right, Number):
            if op == "+":
                return Number(left.value + right.value)
            elif op == "-":
                return Number(left.value - right.value)
            elif op == "*":
                return Number(left.value * right.value)
            elif op == "/":
                return Number(left.value / right.value)

        # String concatenation
        if isinstance(left, String) and isinstance(right, String):
            if op == "+":
                return String(left.value + right.value)

        raise TypeError(f"Unsupported operation: {left} {op} {right}")