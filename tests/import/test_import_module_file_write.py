import os
from pydbml.core.engine import Engine


def test_import_module_file_write(tmp_path):
    """
    ✅ End-to-end test:
    - import module builtins
    - create file using open()
    - write content
    - verify file content
    """

    engine = Engine()

    file_path = tmp_path / "test_output.txt"

    # ✅ convert to string for DSL
    file_str = str(file_path).replace("\\", "\\\\")  # Windows safety

    code = f"""
    import module |builtins|

    !f = object open('{file_str}', 'w')
    !f.write('Hello from PyDBML')
    !f.close()
    """

    engine.execute(code)

    # ✅ verify file content
    with open(file_path, "r") as f:
        content = f.read()

    assert content == "Hello from PyDBML"
