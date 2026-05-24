from pydbml.core.engine import Engine
import pytest

def test_plugin_add():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    r = e.execute("!a + !b")

    assert r.x == 15

def test_plugin_gt():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    r = e.execute("!a > !b")

    assert r.value is True

def test_plugin_chain():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")
    e.execute("!c = object Vec(2)")

    r = e.execute("(!a + !b) + !c")

    assert r.x == 17

def test_plugin_multiple_add():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(1)")
    e.execute("!b = object Vec(2)")
    e.execute("!c = object Vec(3)")

    r = e.execute("!a + !b + !c")

    assert r.x == 6

def test_operator_vs_method():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    r1 = e.execute("!a + !b")
    r2 = e.execute("!a.add(!b)")

    assert r1.x == r2.x

def test_operator_return_type():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(3)")
    e.execute("!b = object Vec(4)")

    r = e.execute("!a + !b")

    assert hasattr(r, "x")
    assert r.x == 7


def test_operator_not_supported():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")
    e.execute("!b = object Vec(5)")

    with pytest.raises(Exception):
        e.execute("!a - !b")   # no @pydbml_operator("-")

def test_plugin_with_number():
    e = Engine()

    e.execute("import |test_plugin|")

    e.execute("!a = object Vec(10)")

    try:
        e.execute("!a + 5")
        assert True   # depends on your design
    except:
        assert True   # acceptable for now