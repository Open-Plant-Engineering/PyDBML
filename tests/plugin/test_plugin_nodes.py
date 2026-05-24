import time
import pytest

from pydbml.execution.signals import ReturnSignal
from pydbml.types.real import Real
from pydbml.types.string import String

# ✅ adjust import based on your project
from pydbml.core.engine import Engine


# --------------------------
# ✅ SIMPLE CUSTOM NODE
# --------------------------
class AddOneNode:
    def __init__(self, value):
        self.value = value


def add_one_handler(evaluator, node):
    val = evaluator.evaluate(node.value)
    return Real(val.value + 1)


def test_plugin_add_one():
    engine = Engine()
    evaluator = engine.evaluator

    evaluator.register_node(AddOneNode, lambda node: add_one_handler(evaluator, node))

    result = evaluator.evaluate(AddOneNode(value=Real(5)))

    assert result.value == 6


# --------------------------
# ✅ STRING MANIPULATION NODE
# --------------------------
class UpperNode:
    def __init__(self, text):
        self.text = text


def upper_handler(evaluator, node):
    val = evaluator.evaluate(node.text)
    return String(val.value.upper())


def test_plugin_uppercase():
    engine = Engine()
    evaluator = engine.evaluator

    evaluator.register_node(UpperNode, lambda node: upper_handler(evaluator, node))

    result = evaluator.evaluate(UpperNode(text=String("hello")))

    assert result.value == "HELLO"


# --------------------------
# ✅ CONTROL-FLOW NODE (RETURN)
# --------------------------
class EarlyReturnNode:
    def __init__(self, val):
        self.val = val


def early_return_handler(evaluator, node):
    value = evaluator.evaluate(node.val)
    raise ReturnSignal(value)


def test_plugin_return_signal():
    engine = Engine()
    evaluator = engine.evaluator

    evaluator.register_node(EarlyReturnNode, lambda node: early_return_handler(evaluator, node))

    try:
        evaluator.evaluate(EarlyReturnNode(val=Real(99)))
    except ReturnSignal as r:
        result = r.value

    assert result.value == 99


# --------------------------
# ✅ MULTI-STEP NODE (BLOCK EXECUTION)
# --------------------------
class SumNode:
    def __init__(self, items):
        self.items = items


def sum_handler(evaluator, node):
    total = 0

    for item in node.items:
        val = evaluator.evaluate(item)
        total += val.value

    return Real(total)


def test_plugin_sum():
    engine = Engine()
    evaluator = engine.evaluator

    evaluator.register_node(SumNode, lambda node: sum_handler(evaluator, node))

    result = evaluator.evaluate(
        SumNode(items=[Real(1), Real(2), Real(3)])
    )

    assert result.value == 6


# --------------------------
# ✅ SIDE EFFECT NODE (SLEEP)
# --------------------------
class SleepNode:
    def __init__(self, duration):
        self.duration = duration


def sleep_handler(evaluator, node):
    val = evaluator.evaluate(node.duration)
    time.sleep(val.value)
    return Real(0)


def test_plugin_sleep():
    engine = Engine()
    evaluator = engine.evaluator

    evaluator.register_node(SleepNode, lambda node: sleep_handler(evaluator, node))

    start = time.time()
    evaluator.evaluate(SleepNode(duration=Real(0.1)))
    end = time.time()

    assert (end - start) >= 0.1


# --------------------------
# ✅ ERROR HANDLING NODE
# --------------------------
class ErrorNode:
    def __init__(self):
        pass


def error_handler(evaluator, node):
    raise Exception("Test error")


def test_plugin_error_propagation():
    engine = Engine()
    evaluator = engine.evaluator

    evaluator.register_node(ErrorNode, lambda node: error_handler(evaluator, node))

    with pytest.raises(Exception):
        evaluator.evaluate(ErrorNode())
