from pydbml.core.engine import Engine

def setup_lib(tmp_path, code, name="TEST"):
    lib = tmp_path / "pdlib"
    lib.mkdir()

    (lib / f"{name}.pdfnc").write_text(code)
    (lib / "index.txt").write_text(f"{name}.pdfnc\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    return engine

def test_scope_isolation(tmp_path):
    engine = setup_lib(tmp_path, """
define function !!TEST(!x is real) is real
    !x = 5
    return !x
endfunction
""", "TEST")

    engine.execute("!x = 10")

    result = engine.execute("!!TEST(1)")

    assert result.value == 5

    # ✅ global should not change
    result2 = engine.execute("!x")
    assert result2.value == 10

def test_shadowing(tmp_path):
    engine = setup_lib(tmp_path, """
define function !!TEST(!x is real) is real
    return !x
endfunction
""", "TEST")

    engine.execute("!x = 100")

    result = engine.execute("!!TEST(5)")
    assert result.value == 5

    result2 = engine.execute("!x")
    assert result2.value == 100

def test_nested_calls(tmp_path):
    lib = tmp_path / "pdlib"
    lib.mkdir()

    (lib / "A.pdfnc").write_text("""
define function !!A(!x is real) is real
    return !!B(!x)
endfunction
""")

    (lib / "B.pdfnc").write_text("""
define function !!B(!y is real) is real
    return !y + 1
endfunction
""")

    (lib / "index.txt").write_text("A.pdfnc\nB.pdfnc\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    result = engine.execute("!!A(5)")
    assert result.value == 6