from pydbml.core.engine import Engine


def test_do_values_basic():
    engine = Engine()

    engine.execute("""
    !arr = object(array)

    !arr[0] = 5
    !arr[1] = 10
    !arr[2] = 15

    !sum = 0

    do values !arr
      !sum = !sum + !v
    enddo
    """)

    result = engine.env.get("sum").get().value
    assert result == 30


def test_do_values_modify():
    engine = Engine()

    engine.execute("""
    !arr = object(array)

    !arr[0] = 1
    !arr[1] = 2
    !arr[2] = 3

    !sum = 0

    do values !arr
      !sum = !sum + (!v * 2)
    enddo
    """)

    result = engine.env.get("sum").get().value
    assert result == 12