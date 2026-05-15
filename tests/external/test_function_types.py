from pydbml.core.engine import Engine


def setup_lib(tmp_path, code, name="TEST"):
    lib = tmp_path / "pdlib"
    lib.mkdir()

    (lib / f"{name}.pdfnc").write_text(code)
    (lib / "index.txt").write_text(f"{name}.pdfnc\n")

    engine = Engine()
    engine.config.add_path(str(lib))

    return engine


# --------------------------
# ✅ Valid case
# --------------------------

def test_valid_types(tmp_path):
    engine = setup_lib(tmp_path, """
define function !!ADD(!x is real, !y is real) is real
    return (!x + !y)
endfunction
""", "ADD")

    result = engine.execute("!!ADD(5, 10)")
    assert result.value == 15


# --------------------------
# ❌ Wrong type
# --------------------------

def test_wrong_param_type(tmp_path):
    engine = setup_lib(tmp_path, """
define function !!ADD(!x is real) is real
    return !x
endfunction
""", "ADD")   # ✅ IMPORTANT FIX

    try:
        engine.execute("!!ADD('abc')")
        assert False
    except TypeError:
        assert True


# --------------------------
# ❌ Wrong return type
# --------------------------

def test_wrong_return_type(tmp_path):
    engine = setup_lib(tmp_path, """
define function !!BAD() is real
    return 'abc'
endfunction
""", "BAD")

    try:
        engine.execute("!!BAD()")
        assert False
    except TypeError:
        assert True


# --------------------------
# ❌ Wrong argument count
# --------------------------

def test_argument_count(tmp_path):
    engine = setup_lib(tmp_path, """
define function !!ADD(!x is real, !y is real) is real
    return (!x + !y)
endfunction
""", "ADD")

    try:
        engine.execute("!!ADD(5)")
        assert False
    except Exception:
        assert True