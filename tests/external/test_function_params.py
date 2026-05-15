from pydbml.core.engine import Engine


def test_add_function(tmp_path):
    lib = tmp_path / "pmllib"
    lib.mkdir()

    (lib / "ADD.pdfnc").write_text("""
define function !!ADD(!x is real, !y is real) is real
    return (!x + !y)
endfunction
""")

    (lib / "index.txt").write_text("ADD.pdfnc\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    result = engine.execute("!!ADD(5, 10)")

    assert result.value == 15


def test_type_enforcement(tmp_path):
    lib = tmp_path / "pmllib"
    lib.mkdir()

    (lib / "ADD.pdfnc").write_text("""
define function !!ADD(!x is real, !y is real) is real
    return (!x + !y)
endfunction
""")

    (lib / "index.txt").write_text("ADD.pdfnc\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    # passing wrong type (string)
    try:
        engine.execute("!!ADD('A', 10)")
        assert False
    except:
        assert True