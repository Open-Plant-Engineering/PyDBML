from pydbml.core.engine import Engine


def test_indices_with_skip():
    engine = Engine()

    engine.execute("""
    !arr = object(array)

    !arr[0] = 10
    !arr[1] = 20
    !arr[2] = 30

    !sum = 0

    do indices !arr
      skip if(!i == 1)
      !sum = !sum + !arr[!i]
    enddo
    """)

    result = engine.env.get("sum").get().value
    assert result == 40  # skip index 1


def test_values_with_skip():
    engine = Engine()

    engine.execute("""
    !arr = object(array)

    !arr[0] = 10
    !arr[1] = 20
    !arr[2] = 30

    !sum = 0

    do values !arr
      skip if(!v == 20)
      !sum = !sum + !v
    enddo
    """)

    result = engine.env.get("sum").get().value
    assert result == 40


def test_nested_indices():
    engine = Engine()

    engine.execute("""
    !arr = object(array)
    !arr[0] = 1
    !arr[1] = 2

    !count = 0

    do indices !arr
      do indices !arr
        !count = !count + 1
      enddo
    enddo
    """)

    result = engine.env.get("count").get().value
    assert result == 4