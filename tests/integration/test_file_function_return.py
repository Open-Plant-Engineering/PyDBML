import os
from pydbml.core.engine import Engine


def create_index(lib_path, files):
    index_file = lib_path / "index.txt"
    index_file.write_text("\n".join(files))


# ✅ 1. simple return from file
def test_file_function_simple_return(tmp_path):
    lib = tmp_path / "lib"
    lib.mkdir()

    f = lib / "f.pdfnc"
    f.write_text("""
DEFINE FUNCTION !!f() IS REAL
    RETURN 10
ENDFUNCTION
""")

    create_index(lib, ["f.pdfnc"])

    os.environ["PYDBML_LIB"] = str(lib)

    e = Engine()

    r = e.execute("!!f()")

    assert r.value == 10


# ✅ 2. return inside IF
def test_file_function_return_inside_if(tmp_path):
    lib = tmp_path / "lib"
    lib.mkdir()

    f = lib / "f.pdfnc"
    f.write_text("""
DEFINE FUNCTION !!f(!x IS REAL) IS REAL
    IF (!x > 5) THEN
        RETURN 100
    ENDIF

    RETURN 1
ENDFUNCTION
""")

    create_index(lib, ["f.pdfnc"])

    os.environ["PYDBML_LIB"] = str(lib)

    e = Engine()

    r1 = e.execute("!!f(10)")
    r2 = e.execute("!!f(2)")

    assert r1.value == 100
    assert r2.value == 1


# ✅ 3. return inside DO loop
def test_file_function_return_inside_loop(tmp_path):
    lib = tmp_path / "lib"
    lib.mkdir()

    f = lib / "f.pdfnc"
    f.write_text("""
DEFINE FUNCTION !!f() IS REAL
    DO !i FROM 1 TO 5
        IF (!i == 3) THEN
            RETURN !i
        ENDIF
    ENDDO

    RETURN 0
ENDFUNCTION
""")

    create_index(lib, ["f.pdfnc"])

    os.environ["PYDBML_LIB"] = str(lib)

    e = Engine()

    r = e.execute("!!f()")

    assert r.value == 3


# ✅ 4. return breaks loop early
def test_file_function_return_breaks_loop(tmp_path):
    lib = tmp_path / "lib"
    lib.mkdir()

