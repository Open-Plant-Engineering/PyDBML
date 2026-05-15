from pydbml.core.engine import Engine
import os


def test_external_function(tmp_path):
    # ✅ create pmllib folder
    lib = tmp_path / "pmllib"
    lib.mkdir()

    # ✅ create function file
    (lib / "HELLO.pdfnc").write_text("""
    define function !!HELLO() is REAL
        return 1 + 2
    endfunction
    """)

    # ✅ create index.txt (NEW FORMAT ✅)
    (lib / "index.txt").write_text("HELLO.pdfnc\n")

    # ✅ init engine
    engine = Engine()
    engine.config.add_path(str(lib))

    # ✅ execute
    result = engine.execute("!!HELLO()")

    assert result.value == 3