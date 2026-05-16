from pydbml.core.engine import Engine


def test_method_case_insensitive(tmp_path):
    lib = tmp_path / "pdlib"
    lib.mkdir()

    (lib / "calc.pdobj").write_text("""
define object CALC
endobject

define method .AddOne(!x is real) is real
    return !x + 1
endmethod
""")

    (lib / "index.txt").write_text("calc.pdobj\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    engine.execute("!c = object calc()")

    r1 = engine.execute("!c.addone(1)")
    r2 = engine.execute("!c.ADDONE(2)")
    r3 = engine.execute("!c.AddOne(3)")

    assert r1.value == 2
    assert r2.value == 3
    assert r3.value == 4