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
