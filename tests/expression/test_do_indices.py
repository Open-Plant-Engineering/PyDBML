from pydbml.core.engine import Engine


def test_do_indices_basic():
    engine = Engine()

    engine.execute("""
    !arr = object array()

    !arr[1] = 10
    !arr[2] = 20
    !arr[3] = 30

    !sum = 0

    do !i indices !arr
      !sum = !sum + !arr[!i]
    enddo
    """)

    result = engine.env.get("sum").get().value
    assert result == 60


def test_do_indices_length():
    engine = Engine()

    engine.execute("""
    !arr = object array()

    !arr[1] = 1
    !arr[2] = 2
    !arr[3] = 3

    !count = 0

    do !i indices !arr
      !count = !count + 1
    enddo
    """)

    result = engine.env.get("count").get().value
    assert result == 3
