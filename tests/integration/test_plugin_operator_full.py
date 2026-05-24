from pydbml.core.engine import Engine
import pytest

def test_plugin_add_operator():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    r = e.execute("!a + !b")

    assert r.x == 15

def test_plugin_add_method():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    r = e.execute("!a.add(!b)")

    assert r.x == 15

def test_plugin_gt_operator():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    r = e.execute("!a > !b")

    assert r.value is True

def test_plugin_gt_keyword():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    r = e.execute("!a GT !b")

    assert r.value is True

def test_plugin_gt_method():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    r = e.execute("!a.gt(!b)")

    assert r.value is True

def test_operator_vs_method_consistency():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    r1 = e.execute("!a + !b")
    r2 = e.execute("!a.add(!b)")

    assert r1.x == r2.x

def test_operator_chaining():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")
    e.execute("!c = object Vec(2)")

    r = e.execute("(!a + !b) + !c")

    assert r.x == 17

def test_multiple_operator_chain():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(1)")
    e.execute("!b = object Vec(2)")
    e.execute("!c = object Vec(3)")

    r = e.execute("!a + !b + !c")

    assert r.x == 6

def test_missing_eq_operator_fails():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(10)")

    with pytest.raises(Exception):
        e.execute("!a == !b")

def test_eq_method_only():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(10)")

    r = e.execute("!a.eq(!b)")

    assert r.value is True

def test_uppercase_method_call():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    r = e.execute("!a.ADD(!b)")

    assert r.x == 15

def test_add():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    assert e.execute("!a + !b").x == 15
    assert e.execute("!a.add(!b)").x == 15

def test_mul():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(4)")
    e.execute("!b = object Vec(5)")

    assert e.execute("!a * !b").x == 20
    assert e.execute("!a.mul(!b)").x == 20


def test_gt():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    assert e.execute("!a > !b").value is True
    assert e.execute("!a GT !b").value is True
    assert e.execute("!a.gt(!b)").value is True


def test_lt():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(3)")
    e.execute("!b = object Vec(5)")

    assert e.execute("!a < !b").value is True
    assert e.execute("!a LT !b").value is True
    assert e.execute("!a.lt(!b)").value is True

def test_eq_method_only():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(10)")

    assert e.execute("!a.eq(!b)").value is True

def test_eq_operator_not_defined():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(10)")

    with pytest.raises(Exception):
        e.execute("!a == !b")


def test_leq_not_defined():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    with pytest.raises(Exception):
        e.execute("!a <= !b")
    
def test_chain_add():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(1)")
    e.execute("!b = object Vec(2)")
    e.execute("!c = object Vec(3)")

    assert e.execute("!a + !b + !c").x == 6


def test_nested_chain():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")
    e.execute("!c = object Vec(2)")

    assert e.execute("(!a + !b) * !c").x == 30

def test_uppercase_method():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    assert e.execute("!a.ADD(!b)").x == 15

def test_operator_vs_method_consistency():
    e = Engine()
    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(7)")
    e.execute("!b = object Vec(3)")

    r1 = e.execute("!a + !b")
    r2 = e.execute("!a.add(!b)")

    assert r1.x == r2.x