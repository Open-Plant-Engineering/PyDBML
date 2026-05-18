from pydbml.core.engine import Engine
from pydbml.execution.ast_evaluator import PyDBMLError
from pydbml.execution.ast_evaluator import ASTEvaluator
from pydbml.ast.nodes import HandleNode, ReturnNode, NumberNode
from pydbml.execution.return_signal import ReturnSignal


def test_handle_basic_manual():

    engine = Engine()
    evaluator = engine.evaluator

    # ✅ simulate failure
    def fail_node():
        raise PyDBMLError(41, 8)

    handle_node = HandleNode(
        try_block=[fail_node],
        handlers=[
            ((41, 8), [ReturnNode(NumberNode(1))]),
            ("ANY", [ReturnNode(NumberNode(2))])
        ],
        else_block=[ReturnNode(NumberNode(3))]
    )

    try:
        result = evaluator.evaluate(handle_node)
    except ReturnSignal as r:
        result = r.value

    assert result.value == 1