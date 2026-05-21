import pytest
from pydbml.core.engine import Engine
from pydbml.runtime.exceptions import PyDBMLError


# --------------------------
# ✅ PRINT NUMBER
# --------------------------
def test_print_number(capsys):
    e = Engine()

    code = "$P 5"

    e.execute(code)

    captured = capsys.readouterr()
    assert captured.out.strip() == "5.0"


# --------------------------
# ✅ PRINT STRING
# --------------------------
def test_print_string(capsys):
    e = Engine()

    code = "$P 'hello'"

    e.execute(code)

    captured = capsys.readouterr()
    assert captured.out.strip() == "hello"


# --------------------------
# ✅ PRINT VARIABLE
# --------------------------
def test_print_variable(capsys):
    e = Engine()

    code = """
    !x = 10
    $P $!x
    """

    e.execute(code)

    captured = capsys.readouterr()
    assert captured.out.strip() == "10.0"


# --------------------------
# ✅ PRINT EXPRESSION
# --------------------------
def test_print_expression(capsys):
    e = Engine()

    code = "$P 5 + 3"

    e.execute(code)

    captured = capsys.readouterr()
    assert captured.out.strip() == "8.0"


# --------------------------
# ✅ PRINT IFTRUE RESULT
# --------------------------
def test_print_iftrue(capsys):
    e = Engine()

    code = "$P iftrue(3 == 3, 100, 200)"

    e.execute(code)

    captured = capsys.readouterr()
    assert captured.out.strip() == "100.0"


# --------------------------
# ✅ PRINT ERROR NO EXPRESSION
# --------------------------
def test_print_missing_expr():
    e = Engine()

    code = "$P"

    with pytest.raises(PyDBMLError) as err:
        e.execute(code)

    assert "Expected expression" in str(err.value)
