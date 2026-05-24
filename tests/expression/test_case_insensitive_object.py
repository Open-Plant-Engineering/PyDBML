from pydbml.core.engine import Engine


def test_object_case_insensitive(tmp_path):
    lib = tmp_path / "pdlib"
    lib.mkdir()

    (lib / "User.pdobj").write_text("""
define object USER
endobject
""")

    (lib / "index.txt").write_text("User.pdobj\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    engine.execute("!u1 = object user()")
    engine.execute("!u2 = object USER()")
    engine.execute("!u3 = object UsEr()")

    assert engine.env.get("u1") is not None
    assert engine.env.get("u2") is not None
    assert engine.env.get("u3") is not None