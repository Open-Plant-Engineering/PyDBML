from pydbml.core.engine import Engine


# --------------------------
# Comparison Methods
# --------------------------

def test_eq_true():
    engine = Engine()

    engine.execute("!x = 5")
    engine.execute("!y = 5")

    result = engine.execute("!x.EQ(!y)")
    assert result.value is True


def test_eq_false():
    engine = Engine()

    engine.execute("!x = 5")
    engine.execute("!y = 10")

    result = engine.execute("!x.EQ(!y)")
    assert result.value is False


def test_neq():
    engine = Engine()

    engine.execute("!x = 5")
    engine.execute("!y = 10")

    result = engine.execute("!x.NEQ(!y)")
    assert result.value is True


def test_gt():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 5")

    result = engine.execute("!x.GT(!y)")
    assert result.value is True


def test_lt():
    engine = Engine()

    engine.execute("!x = 2")
    engine.execute("!y = 5")

    result = engine.execute("!x.LT(!y)")
    assert result.value is True


def test_geq():
    engine = Engine()

    engine.execute("!x = 5")
    engine.execute("!y = 5")

    result = engine.execute("!x.GEQ(!y)")
    assert result.value is True


def test_leq():
    engine = Engine()

    engine.execute("!x = 3")
    engine.execute("!y = 5")

    result = engine.execute("!x.LEQ(!y)")
    assert result.value is True


# --------------------------
# Logical Methods
# --------------------------

def test_and():
    engine = Engine()

    engine.execute("!t = true")
    engine.execute("!f = false")

    result = engine.execute("!t.AND(!f)")
    assert result.value is False


def test_or():
    engine = Engine()

    engine.execute("!t = true")
    engine.execute("!f = false")

    result = engine.execute("!t.OR(!f)")
    assert result.value is True


def test_not():
    engine = Engine()

    engine.execute("!t = true")

    result = engine.execute("!t.NOT()")
    assert result.value is False


# --------------------------
# Mixed with expressions
# --------------------------

def test_chain_with_variables():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 5")

    result = engine.execute("!x.GT(!y).AND(true)")
    assert result.value is True


# --------------------------
# With indexing + dot
# --------------------------

def test_method_on_index():
    engine = Engine()

    engine.execute("!x = object ARRAY()")
    engine.execute("!x[1] = 10")

    result = engine.execute("!x[1].GT(5)")
    assert result.value is True