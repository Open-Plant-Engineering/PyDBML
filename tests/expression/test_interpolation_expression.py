from pydbml.core.engine import Engine

def test_expression_interpolation():
    engine = Engine()

    result = engine.execute("|$!(5 + 3)|")

    assert result.value == "8"

def test_expression_with_variable():
    engine = Engine()

    engine.execute("!x = 10")

    result = engine.execute("|Value = $!(x + 5)|")

    assert result.value == "Value = 15"

def test_expression_boolean():
    engine = Engine()

    engine.execute("!x = 10")

    result = engine.execute("|$!(x > 5)|")

    assert result.value == "True"

def test_expression_object(tmp_path):
    lib = tmp_path / "pdlib"
    lib.mkdir()

    (lib / "USER.pdobj").write_text("""
define object USER
    member .age is REAL
endobject
""")

    (lib / "index.txt").write_text("USER.pdobj\n")

    engine = Engine()
    engine.config.add_path(str(lib))   # ✅ MISSING LINE

    engine.execute("!u = object USER()")
    engine.execute("!u.age = 25")

    result = engine.execute("|$!(u.age + 5)|")

    assert result.value == "30"

