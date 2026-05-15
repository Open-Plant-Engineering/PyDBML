from pydbml.core.engine import Engine

def test_object_method(tmp_path):
    lib = tmp_path / "pdlib"
    lib.mkdir(parents=True, exist_ok=True)

    ( lib / "USER.pdobj").write_text("""
define object USER
    member .age is REAL
endobject

define method .USER()
endmethod

define method .getAge() is real
    return !this.age
endmethod
""")

    (lib / "index.txt").write_text("USER.pdobj\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    engine.execute("!u = object USER()")
    engine.execute("!u.age = 25")

    result = engine.execute("!u.getAge()")

    assert result.value == 25


def test_method_overloading(tmp_path):
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

    engine.execute("!c = object CALC()")

    r1 = engine.execute("!c.add(5)")
    r2 = engine.execute("!c.add(5, 7)")

    assert r1.value == 15
    assert r2.value == 12