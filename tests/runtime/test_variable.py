import pytest
from pydbml.runtime.environment import Environment
from pydbml.types.primitives import String


def test_local_variable_set_get():
    env = Environment()

    env.set("x", String("Tommy"))
    var = env.get("x")

    assert var.get().value == "Tommy"


def test_global_variable():
    env = Environment()

    env.set("x", String("Global Tommy"), is_global=True)

    var = env.get_global("x")
    assert var.get().value == "Global Tommy"


def test_variable_delete():
    env = Environment()

    env.set("x", String("Tommy"))
    env.delete("x")

    with pytest.raises(KeyError):
        env.get("x")


def test_uninitialized_variable():
    env = Environment()

    env.set("x", None)
    var = env.get("x")

    with pytest.raises(ValueError):
        var.get()
