import os
from pydbml.core.engine import Engine


def test_function_from_lib(tmp_path):
    lib = tmp_path / "lib"
    lib.mkdir()

    f = lib / "sum.pdfnc"
    f.write_text("""
DEFINE FUNCTION !!sum(!a IS REAL, !b IS REAL) IS REAL
    RETURN !a + !b
ENDFUNCTION
""")

    index = lib / "index.txt"
    index.write_text("sum.pdfnc")

    os.environ["PYDBML_LIB"] = str(lib)

    e = Engine()

    r = e.execute("!!sum(2,3)")

    assert r.value == 5