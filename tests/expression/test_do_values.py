from pydbml.core.engine import Engine


def test_do_values_basic():
    engine = Engine()

    engine.execute("""
    !arr = object(array)

    !arr[1] = 5
    !arr[2] = 10
    !arr[3] = 15

    !sum = 0

    do !v values !arr
      !sum = !sum + !v
    enddo
    """)

    result = engine.env.get("sum").get().value
    assert result == 30


def test_do_values_modify():
    engine = Engine()

    engine.execute("""
    !arr = object(array)

    !arr[1] = 1
    !arr[2] = 2
    !arr[3] = 3

    !sum = 0

    do !v values !arr
      !sum = !sum + (!v * 2)
    enddo
    """)

    result = engine.env.get("sum").get().value
    assert result == 12