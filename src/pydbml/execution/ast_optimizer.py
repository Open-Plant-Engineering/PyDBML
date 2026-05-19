from pydbml.ast.nodes import BinaryOpNode, NumberNode


class ASTOptimizer:

    def optimize(self, node):
        if node is None:
            return None

        # ✅ optimize list
        if isinstance(node, list):
            return [self.optimize(n) for n in node]

        # ✅ binary operations
        if isinstance(node, BinaryOpNode):
            left = self.optimize(node.left)
            right = self.optimize(node.right)

            # ✅ constant folding
            if isinstance(left, NumberNode) and isinstance(right, NumberNode):

                if node.op == "+":
                    return NumberNode(left.value + right.value)
                if node.op == "-":
                    return NumberNode(left.value - right.value)
                if node.op == "*":
                    return NumberNode(left.value * right.value)
                if node.op == "/":
                    return NumberNode(left.value / right.value)

            # ✅ replace children
            node.left = left
            node.right = right

            return node

        return self._optimize_node_fields(node)

    def _optimize_node_fields(self, node):

        # ✅ CRITICAL FIX: only process objects with __dict__
        if not hasattr(node, "__dict__"):
            return node

        for attr, val in vars(node).items():   # ✅ ONLY real fields

            # ✅ optimize list safely
            if isinstance(val, list):
                new_list = []
                for v in val:
                    new_list.append(self.optimize(v))
                setattr(node, attr, new_list)

            # ✅ handle tuples safely
            elif isinstance(val, tuple):
                new_tuple = tuple(self.optimize(v) for v in val)
                setattr(node, attr, new_tuple)

            # ✅ optimize nested AST nodes only
            elif hasattr(val, "__dict__"):
                setattr(node, attr, self.optimize(val))

        return node