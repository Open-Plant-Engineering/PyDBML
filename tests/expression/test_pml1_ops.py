from pydbml.core.engine import Engine


# --------------------------
# Equal / Not Equal
# --------------------------

def test_eq_true():
    engine = Engine()

    engine.execute("!x = 5")
    engine.execute("!y = 5")

    result = engine.execute("!x EQ !y")
    assert result.value is True


def test_eq_false():
    engine = Engine()

    engine.execute("!x = 5")
    engine.execute("!y = 10")

    result = engine.execute("!x EQ !y")
    assert result.value is False


def test_neq_true():
    engine = Engine()

    engine.execute("!x = 5")
    engine.execute("!y = 10")

    result = engine.execute("!x NEQ !y")
    assert result.value is True


# --------------------------
# Greater / Less
# --------------------------

def test_gt_true():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 5")

    result = engine.execute("!x GT !y")
    assert result.value is True


def test_gt_false():
    engine = Engine()

    engine.execute("!x = 3")
    engine.execute("!y = 5")

    result = engine.execute("!x GT !y")
    assert result.value is False


def test_lt_true():
    engine = Engine()

    engine.execute("!x = 2")
    engine.execute("!y = 5")

    result = engine.execute("!x LT !y")
    assert result.value is True


def test_lt_false():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 5")

    result = engine.execute("!x LT !y")
    assert result.value is False


# --------------------------
# Greater / Less Or Equal
# --------------------------

def test_ge_true_equal():
    engine = Engine()

    engine.execute("!x = 5")
    engine.execute("!y = 5")

    result = engine.execute("!x GE !y")
    assert result.value is True


def test_ge_true_greater():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 5")

    result = engine.execute("!x GE !y")
    assert result.value is True


def test_le_true():
    engine = Engine()

    engine.execute("!x = 3")
    engine.execute("!y = 5")

    result = engine.execute("!x LE !y")
    assert result.value is True


# --------------------------
# Mixed Expressions
# --------------------------

def test_mixed_expression():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 5")
    engine.execute("!z = 10")

    result = engine.execute("!x GT !y AND !x EQ !z")
    assert result.value is True


# --------------------------
# With Arithmetic
# --------------------------

def test_expression_with_arithmetic():
    engine = Engine()

    engine.execute("!x = 10")

    result = engine.execute("(!x + 5) GT 10")
    assert result.value is True


# --------------------------
# Case Insensitivity
# --------------------------

def test_case_insensitive_keywords():
    engine = Engine()

    engine.execute("!x = 5")
    engine.execute("!y = 5")

    result = engine.execute("!x eq !y")  # lowercase
    assert result.value is True

def test_all_styles_equivalent():
    engine = Engine()

    engine.execute("!x = 10")
    engine.execute("!y = 5")

    r1 = engine.execute("!x > !y")
    r2 = engine.execute("!x GT !y")
    r3 = engine.execute("!x.GT(!y)")

    assert r1.value == r2.value == r3.value