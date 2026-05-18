import os
from pydbml.core.engine import Engine


def test_env_plugin_class(tmp_path):
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()

    # ✅ plugin file
    f = plugin_dir / "vec.py"
    f.write_text("""
from pydbml.plugins import pydbml_class, pydbml_method

@pydbml_class
class Vec:
    def __init__(self, x):
        self.x = x

    @pydbml_method
    def get(self):
        return self.x
""")

    os.environ["PYDBML_PLUGIN_PATH"] = str(plugin_dir)

    e = Engine()

    e.execute("!v = object Vec(10)")
    r = e.execute("!v.get()")

    assert r.value == 10

def test_env_plugin_operator(tmp_path):
    import os
    from pydbml.core.engine import Engine

    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()

    f = plugin_dir / "vec.py"
    f.write_text("""
from pydbml.plugins import pydbml_class, pydbml_operator

@pydbml_class
class Vec:
    def __init__(self, x):
        self.x = x

    @pydbml_operator("+")
    def add(self, other):
        return Vec(self.x + other.x)
""")

    os.environ["PYDBML_PLUGIN_PATH"] = str(plugin_dir)

    e = Engine()

    e.execute("!a = object Vec(5)")
    e.execute("!b = object Vec(3)")

    r = e.execute("!a + !b")

    assert r.x == 8


def test_env_plugin_function(tmp_path):
    import os
    from pydbml.core.engine import Engine

    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()

    f = plugin_dir / "math.py"
    f.write_text("""
from pydbml.plugins import pydbml_function

@pydbml_function
def add(a, b):
    return a + b
""")

    os.environ["PYDBML_PLUGIN_PATH"] = str(plugin_dir)

    e = Engine()

    r = e.execute("!!add(2, 3)")

    assert r.value == 5


def test_multiple_plugins(tmp_path):
    import os
    from pydbml.core.engine import Engine

    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()

    # file 1
    (plugin_dir / "a.py").write_text("""
from pydbml.plugins import pydbml_function

@pydbml_function
def f1():
    return 1
""")

    # file 2
    (plugin_dir / "b.py").write_text("""
from pydbml.plugins import pydbml_function

@pydbml_function
def f2():
    return 2
""")

    os.environ["PYDBML_PLUGIN_PATH"] = str(plugin_dir)

    e = Engine()

    r1 = e.execute("!!f1()")
    r2 = e.execute("!!f2()")

    assert r1.value == 1
    assert r2.value == 2

def test_invalid_plugin_file(tmp_path):
    import os
    from pydbml.core.engine import Engine

    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()

    # invalid file (no decorators)
    (plugin_dir / "bad.py").write_text("""
class Dummy:
    pass
""")

    os.environ["PYDBML_PLUGIN_PATH"] = str(plugin_dir)

    # ✅ should not crash
    e = Engine()

    assert True
