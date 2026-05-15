from pydbml.core.engine import Engine
import os


def test_external_function(tmp_path):
    # ✅ create temp pmllib folder
    lib = tmp_path / "pmllib"
    lib.mkdir()

    # ✅ create function file
    (lib / "HELLO.pdfnc").write_text("1 + 2")

    # ✅ create index
    import json
    with open(lib / "index.json", "w") as f:
        json.dump({"HELLO": "HELLO.pdfnc"}, f)

    # ✅ run
    engine = Engine()
    engine.config.add_path(str(lib))

    result = engine.execute("!!HELLO()")

    assert result.value == 3