from pydbml.core.engine import Engine


def test_do_indices_basic():
    engine = Engine()

    engine.execute("""
    !arr = object(array)

    !arr[0] = 10
    !arr[1] = 20
    !arr[2] = 30

    !sum = 0

    do indices !arr
      !sum = !sum + !arr[!i]
    enddo
    """)

    result = engine.env.get("sum").get().value
    assert result == 60


def test_do_indices_length():
    engine = Engine()

    engine.execute("""
    !arr = object(array)

    !arr[0] = 1
    !arr[1] = 2
    !arr[2] = 3

    !count = 0

    do indices !arr
      !count = !count + 1
    enddo
    """)

    result = engine.env.get("count").get().value
    assert result == 3
