import pytest
from pydbml.types.array import Array
from pydbml.types.primitives import String, Number


def test_array_valid():
    arr = Array([String("a"), Number(1)])
    arr.validate()


def test_array_invalid_raw_python():
    with pytest.raises(TypeError):
        Array([1, 2, 3]).validate()
