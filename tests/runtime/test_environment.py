import pytest
from pydbml.runtime.environment import Environment
from pydbml.types.real import Real


def test_set_and_get_variable():
    env = Environment()

    env.set("x", Real(10))
    value = env.get("x")

    assert value.get().value == 10


def test_get_undefined_variable():
    env = Environment()

    with pytest.raises(KeyError):
        env.get("y")