from pydbml.core.engine import Engine
import pytest
from pydbml.runtime.exceptions import PyDBMLError

def test_valid_member_type(tmp_path):
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
    result = engine.execute("!u.age = 25")

    assert result.value == 25

def test_invalid_member_type(tmp_path):
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

    with pytest.raises(PyDBMLError) as exc:
        engine.execute("!u.age = 'wrong'")

    assert exc.value.code1 == 10
    assert exc.value.code2 == 1


def test_unknown_member(tmp_path):
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

    with pytest.raises(PyDBMLError) as exc:
        engine.execute("!u.name = 'Tom'")

    assert exc.value.code1 == 20
    assert exc.value.code2 == 1
