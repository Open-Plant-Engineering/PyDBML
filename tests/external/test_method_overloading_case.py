from pydbml.core.engine import Engine


def test_method_overloading_case_insensitive(tmp_path):
    lib = tmp_path / "pdlib"
    lib.mkdir()

    (lib / "CALC.pdobj").write_text("""
define object CALC
endobject

define method .add(!x is REAL)
    return !x + 10
endmethod

define method .add(!x is REAL, !y is REAL)
    return !x + !y
endmethod
""")

    (lib / "index.txt").write_text("CALC.pdobj\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    engine.execute("!c = object calc()")

    r1 = engine.execute("!c.add(5)")
    r2 = engine.execute("!c.ADD(5, 7)")
    r3 = engine.execute("!c.AdD(2, 3)")

    assert r1.value == 15
    assert r2.value == 12
    assert r3.value == 5