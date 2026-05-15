from pydbml.core.engine import Engine


def test_simple_return(tmp_path):
    lib = tmp_path / "pmllib"
    lib.mkdir()

    # function file
    (lib / "TEST.pdfnc").write_text("""
define function !!TEST() is real
    return 10
endfunction
""")

    # index
    (lib / "index.txt").write_text("TEST.pdfnc\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    result = engine.execute("!!TEST()")

    assert result.value == 10


def test_expression_return(tmp_path):
    lib = tmp_path / "pmllib"
    lib.mkdir()

    (lib / "ADD.pdfnc").write_text("""
define function !!ADD() is real
    return 5 + 5
endfunction
""")

    (lib / "index.txt").write_text("ADD.pdfnc\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    result = engine.execute("!!ADD()")

    assert result.value == 10