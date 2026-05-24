from pydbml.core.engine import Engine


def test_internal_function_name_normalization(tmp_path):
    lib = tmp_path / "pdlib"
    lib.mkdir()

    (lib / "Test.pdfnc").write_text("""
define function !!Test() is real
    return 1
endfunction
""")

    (lib / "index.txt").write_text("Test.pdfnc\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    result = engine.execute("!!TEST()")

    assert result.value == 1