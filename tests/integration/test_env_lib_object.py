import os
from pydbml.core.engine import Engine


def test_object_from_lib(tmp_path):
    lib = tmp_path / "lib"
    lib.mkdir()

    # ✅ object file
    f = lib / "person.pdobj"
    f.write_text("""
DEFINE OBJECT person
    member.name IS STRING
ENDOBJECT
""")

    # ✅ index mapping (IMPORTANT for your resolver)
    index = lib / "index.txt"
    index.write_text("person.pdobj")

    os.environ["PYDBML_LIB"] = str(lib)

    e = Engine()

    e.execute("!p = object person()")
    r = e.execute("!p.name")

    assert r is None