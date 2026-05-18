from pydbml.types.real import Real
from pydbml.types.string import String
from pydbml.types.boolean import Boolean

COMPARISON_OPS = [">=", "<=", "==", "!=", ">", "<"]

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
        
        # 0️⃣ Comparison operators (highest priority for splitting)
        for op in COMPARISON_OPS:
            index = self._find_operator(expr, op)

            if index != -1:
                left = expr[:index]
                right = expr[index + len(op):]

                left_val = self.evaluate(left)
                right_val = self.evaluate(right)

                return self._apply_comparison(left_val, right_val, op)

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
        Find operator position (supports multi-char operators),
        ignoring parentheses.
        """
    
        depth = 0
        op_len = len(operator)
    
        for i in range(len(expr) - op_len, -1, -1):
            char = expr[i]
    
            if char == ")":
                depth += 1
            elif char == "(":
                depth -= 1
    
            # Only match if at correct depth
            if depth == 0 and expr[i : i + op_len] == operator:
                return i
    
        return -1

    def _apply_operator(self, left, right, op):

        # Number operations
        if isinstance(left, Real) and isinstance(right, Real):
            if op == "+":
                return Real(left.value + right.value)
            elif op == "-":
                return Real(left.value - right.value)
            elif op == "*":
                return Real(left.value * right.value)
            elif op == "/":
                return Real(left.value / right.value)

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
    def _apply_comparison(self, left, right, op):
        left_val = left.value
        right_val = right.value

        if op == ">":
            return Boolean(left_val > right_val)
        elif op == "<":
            return Boolean(left_val < right_val)
        elif op == ">=":
            return Boolean(left_val >= right_val)
        elif op == "<=":
            return Boolean(left_val <= right_val)
        elif op == "==":
            return Boolean(left_val == right_val)
        elif op == "!=":
            return Boolean(left_val != right_val)

        raise TypeError(f"Unsupported comparison: {left} {op} {right}")

