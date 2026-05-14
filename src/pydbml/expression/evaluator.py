from pydbml.types.primitives import Number, String


class ExpressionEvaluator:
    """
    Handles expressions with operator precedence.
    """

    def __init__(self, resolver):
        self.resolver = resolver

    def evaluate(self, expr: str):
        expr = expr.strip()

        # Handle parentheses first
        if self._is_wrapped(expr):
            return self.evaluate(expr[1:-1].strip())

        # 1️⃣ LOW precedence (right split) → + -
        for op in ["+", "-"]:
            index = self._find_operator(expr, op)
            if index != -1:
                left = expr[:index]
                right = expr[index + 1 :]

                left_val = self.evaluate(left)
                right_val = self.evaluate(right)

                return self._apply_operator(left_val, right_val, op)

        # 2️⃣ HIGH precedence → * /
        for op in ["*", "/"]:
            index = self._find_operator(expr, op)
            if index != -1:
                left = expr[:index]
                right = expr[index + 1 :]

                left_val = self.evaluate(left)
                right_val = self.evaluate(right)

                return self._apply_operator(left_val, right_val, op)

        # 3️⃣ Base case (value or variable)
        return self.resolver.resolve(expr)

    def _find_operator(self, expr: str, operator: str) -> int:
        """
        Find operator position, ignoring parentheses.
        Right-to-left scan ensures correct grouping.
        """

        depth = 0

        for i in range(len(expr) - 1, -1, -1):
            char = expr[i]

            if char == ")":
                depth += 1
            elif char == "(":
                depth -= 1
            elif char == operator and depth == 0:
                return i

        return -1

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

        # String concat
        if isinstance(left, String) and isinstance(right, String):
            if op == "+":
                return String(left.value + right.value)

        raise TypeError(f"Unsupported operation: {left} {op} {right}")
    
    def _is_wrapped(self, expr: str) -> bool:
        """
        Check if the entire expression is wrapped in a single pair of parentheses.
        """
    
        if not (expr.startswith("(") and expr.endswith(")")):
            return False
    
        depth = 0
    
        for i, char in enumerate(expr):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
    
            # If we reach depth 0 before the end → NOT fully wrapped
            if depth == 0 and i != len(expr) - 1:
                return False
    
        return True
    