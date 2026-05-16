from pydbml.core.engine import Engine


def test_object_method_case_insensitive(tmp_path):
    lib = tmp_path / "pdlib"
    lib.mkdir()

    (lib / "USER.pdobj").write_text("""
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

    engine.execute("!u = object user()")
    engine.execute("!u.age = 25")

    r1 = engine.execute("!u.getage()")
    r2 = engine.execute("!u.GETAGE()")
    r3 = engine.execute("!u.getAge()")

    assert r1.value == 25
    assert r2.value == 25
    assert r3.value == 25