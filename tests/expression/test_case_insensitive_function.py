from pydbml.core.engine import Engine


def test_function_case_insensitive(tmp_path):
    lib = tmp_path / "pdlib"
    lib.mkdir()

    # ✅ create function file
    (lib / "Add.pdfnc").write_text("""
define function !!Add(!x is real, !y is real) is real
    return !x + !y
endfunction
""")

    # ✅ register file
    (lib / "index.txt").write_text("Add.pdfnc\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    r1 = engine.execute("!!add(1, 2)")
    r2 = engine.execute("!!ADD(2, 3)")
    r3 = engine.execute("!!AdD(3, 4)")

    assert r1.value == 3
    assert r2.value == 5
    assert r3.value == 7