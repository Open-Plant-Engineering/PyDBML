import pytest
from pydbml.types.number import Number
from pydbml.types.string import String
from pydbml.types.boolean import Boolean


def test_string_valid():
    s = String("hello")
    s.validate()


def test_string_invalid():
    with pytest.raises(TypeError):
        String(123).validate()


def test_number_valid():
    Number(10).validate()
    Number(3.14).validate()


def test_number_invalid():
    with pytest.raises(TypeError):
        Number("abc").validate()


def test_boolean_valid():
    Boolean(True).validate()


def test_boolean_invalid():
    with pytest.raises(TypeError):
        Boolean("true").validate()