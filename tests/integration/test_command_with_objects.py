from pydbml.core.engine import Engine


def test_object_interpolation(tmp_path):
    lib = tmp_path / "pdlib"
    lib.mkdir()

    (lib / "USER.pdobj").write_text("""
define object USER
    member .age is REAL
endobject
""")

    (lib / "index.txt").write_text("USER.pdobj\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    engine.execute("!u = object USER()")
    engine.execute("!u.age = 25")

    result = engine.execute("|Age is $!u.age|")

    assert result.value == "Age is 25"