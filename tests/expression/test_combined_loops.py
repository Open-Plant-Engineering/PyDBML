from pydbml.core.engine import Engine


def test_indices_with_skip():
    engine = Engine()

    engine.execute("""
    !arr = object array()

    !arr[1] = 10
    !arr[2] = 20
    !arr[3] = 30

    !sum = 0

    do !i indices !arr
      skip if(!i == 1)
      !sum = !sum + !arr[!i]
    enddo
    """)

    result = engine.env.get("sum").get().value
    assert result == 50  # skip index 1


def test_values_with_skip():
    engine = Engine()

    engine.execute("""
    !arr = object array()

    !arr[1] = 10
    !arr[2] = 20
    !arr[3] = 30

    !sum = 0

    do !v values !arr
      skip if(!v == 20)
      !sum = !sum + !v
    enddo
    """)

    result = engine.env.get("sum").get().value
    assert result == 40


def test_nested_indices():
    engine = Engine()

    engine.execute("""
    !arr = object array()
    !arr[1] = 1
    !arr[2] = 2

    !count = 0

    do !i indices !arr
      do !i indices !arr
        !count = !count + 1
      enddo
    enddo
    """)

    result = engine.env.get("count").get().value
    assert result == 4