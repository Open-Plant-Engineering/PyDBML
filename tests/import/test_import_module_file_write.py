import os
import pytest
from pydbml.core.engine import Engine


# --------------------------
# ✅ BASIC FILE WRITE (CORE TEST)
# --------------------------
def test_import_module_file_write(tmp_path):
    engine = Engine()

    file_path = tmp_path / "test_output.txt"
    file_str = str(file_path).replace("\\", "\\\\")

    code = f"""
    import module builtins

    !f = object open('{file_str}', 'w')
    !f.write('Hello from PyDBML')
    !f.close()
    """

    engine.execute(code)

    with open(file_path, "r") as f:
        content = f.read()

    assert content == "Hello from PyDBML"


# --------------------------
# ✅ METHOD CASE INSENSITIVITY
# --------------------------
def test_method_case_insensitive(tmp_path):
    engine = Engine()

    file_path = tmp_path / "case_test.txt"
    file_str = str(file_path).replace("\\", "\\\\")

    code = f"""
    import module builtins

    !f = object open('{file_str}', 'w')
    !f.WRITE('Upper Case Works')
    !f.Close()
    """

    engine.execute(code)

    with open(file_path, "r") as f:
        content = f.read()

    assert content == "Upper Case Works"


# --------------------------
# ✅ MIXED CASE
# --------------------------
def test_method_mixed_case(tmp_path):
    engine = Engine()

    file_path = tmp_path / "mixed_test.txt"
    file_str = str(file_path).replace("\\", "\\\\")

    code = f"""
    import module builtins

    !f = object open('{file_str}', 'w')
    !f.wRiTe('Mixed Case Works')
    !f.cLoSe()
    """

    engine.execute(code)

    with open(file_path, "r") as f:
        content = f.read()

    assert content == "Mixed Case Works"


# --------------------------
# ✅ FUNCTION CASE INSENSITIVE
# --------------------------
def test_function_case_insensitive(tmp_path):
    engine = Engine()

    file_path = tmp_path / "func_case.txt"
    file_str = str(file_path).replace("\\", "\\\\")

    code = f"""
    import module builtins

    !f = object OPEN('{file_str}', 'w')
    !f.write('Function Case Works')
    !f.close()
    """

    engine.execute(code)

    with open(file_path, "r") as f:
        content = f.read()

    assert content == "Function Case Works"


# --------------------------
# ✅ READ BACK TEST
# --------------------------
def test_file_read(tmp_path):
    engine = Engine()

    file_path = tmp_path / "read_test.txt"
    file_str = str(file_path).replace("\\", "\\\\")

    code = f"""
    import module builtins

    !f = object open('{file_str}', 'w')
    !f.write('Read Test')
    !f.close()

    !f2 = object open('{file_str}', 'r')
    !data = !f2.read()
    !f2.close()
    """

    engine.execute(code)

    with open(file_path, "r") as f:
        content = f.read()

    assert content == "Read Test"


# --------------------------
# ✅ EDGE CASE: NON-EXIST METHOD
# --------------------------
def test_invalid_method_error(tmp_path):
    engine = Engine()

    file_path = tmp_path / "error_test.txt"
    file_str = str(file_path).replace("\\", "\\\\")

    code = f"""
    import module builtins

    !f = object open('{file_str}', 'w')
    !f.notAMethod()
    """

    with pytest.raises(Exception):
        engine.execute(code)
