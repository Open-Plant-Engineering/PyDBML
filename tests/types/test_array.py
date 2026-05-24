from pydbml.types.array import Array
from pydbml.types.real import Real
from pydbml.types.string import String


def test_array_valid():
    arr = Array()

    arr.set(1, String("a"))
    arr.set(2, Real(1))

    assert arr.get(1).value == "a"
    assert arr.get(2).value == 1

def test_empty_array():
    arr = Array()
    assert str(arr) == "<ARRAY>"