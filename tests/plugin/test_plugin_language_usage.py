import pytest
from pydbml.core.engine import Engine
from pydbml.types.real import Real


# --------------------------
# ✅ Plugin logic
# --------------------------
def add_one_handler(evaluator, node):
    val = evaluator.evaluate(node.args[0])
    return Real(val.value + 1)


# --------------------------
# ✅ TEST: plugin as function
# --------------------------
def test_addone_in_language():
    engine = Engine()
    evaluator = engine.evaluator

    # ✅ register as FUNCTION name
    evaluator.registry.functions["addone"] = lambda x: x + 1

    result = engine.execute("""
        !x = addone(5)
        $p $!x
    """)

    # no assertion needed if print works

from pydbml.ast.nodes import FunctionCallNode, NumberNode


class AddOneNode:
    def __init__(self, value):
        self.value = value


def add_one_handler(evaluator, node):
    val = evaluator.evaluate(node.value)
    return Real(val.value + 1)


def test_plugin_in_ast_flow():
    engine = Engine()
    evaluator = engine.evaluator

    evaluator.register_node(AddOneNode, lambda node: add_one_handler(evaluator, node))

    # ✅ simulate AST from parser
    ast = [
        AddOneNode(NumberNode(5))
    ]

    result = evaluator.evaluate(ast)

    assert result.value == 6

def test_plugin_inside_expression():
    engine = Engine()
    evaluator = engine.evaluator

    evaluator.register_node(AddOneNode, lambda node: add_one_handler(evaluator, node))

    ast = [
        AddOneNode(NumberNode(10)),
        AddOneNode(NumberNode(20))
    ]

    result = evaluator.evaluate(ast)

    assert result.value == 21


from pydbml.ast.nodes import IfNode, BooleanNode


def test_plugin_in_if():
    engine = Engine()
    evaluator = engine.evaluator

    evaluator.register_node(AddOneNode, lambda node: add_one_handler(evaluator, node))

    ast = IfNode(
        condition=BooleanNode(True),
        then_branch=[AddOneNode(NumberNode(5))],
        else_branch=None,
        is_expression=False
    )

    result = evaluator.evaluate(ast)

    assert result.value == 6

from pydbml.ast.nodes import DoNode, NumberNode


def test_plugin_in_loop():
    engine = Engine()
    evaluator = engine.evaluator

    evaluator.register_node(AddOneNode, lambda node: add_one_handler(evaluator, node))

    ast = DoNode(
        var="i",
        start=NumberNode(1),
        end=NumberNode(3),
        step=None,
        body=[AddOneNode(NumberNode(5))]
    )

    result = evaluator.evaluate(ast)

    assert result is None


