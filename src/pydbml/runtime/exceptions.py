class PyDBMLError(Exception):
    def __init__(self, code1, code2, message="", node=None, stack=None):
        self.code1 = code1
        self.code2 = code2
        self.message = message

        # ✅ new debugging info
        self.node = node
        self.stack = stack or []

        super().__init__(message)

    def __str__(self):
        lines = []

        # ✅ PRIMARY SYSTEM (unchanged)
        lines.append(f"({self.code1}, {self.code2}) {self.message}")

        # ✅ ADD DEBUG CONTEXT (non-breaking)
        if self.node and hasattr(self.node, "token") and self.node.token:
            t = self.node.token
            lines.append(f"Line {t.line}, Column {t.column}")

        # ✅ TRACEBACK (optional)
        if self.stack:
            lines.append("\nTraceback:")
            for n in reversed(self.stack):
                if hasattr(n, "token") and n.token:
                    lines.append(f"  Line {n.token.line}")

        return "\n".join(lines)