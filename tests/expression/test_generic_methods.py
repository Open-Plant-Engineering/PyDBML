from pydbml.core.engine import Engine


# --------------------------
# Arithmetic methods
# --------------------------

def test_add():
    e = Engine()
    e.execute("!x = 10")

    result = e.execute("!x.ADD(5)")
    assert result.value == 15


def test_sub():
    e = Engine()
    e.execute("!x = 10")

    result = e.execute("!x.SUB(3)")
    assert result.value == 7


# --------------------------
# Array methods
# --------------------------

def test_array_set_get():
    e = Engine()

    e.execute("!x = object ARRAY()")
    e.execute("!x.SET(1, 100)")

    result = e.execute("!x.GET(1)")
    assert result.value == 100


# --------------------------
# Length
# --------------------------

def test_length():
    e = Engine()

    e.execute("!x = object ARRAY()")
    e.execute("!x.SET(1, 10)")
    e.execute("!x.SET(2, 20)")

    result = e.execute("!x.LENGTH()")
    assert result.value == 2


# --------------------------
# Chaining
# --------------------------

def test_chaining():
    e = Engine()

    e.execute("!x = 10")

    result = e.execute("!x.ADD(5).GT(10)")
    assert result.value is True