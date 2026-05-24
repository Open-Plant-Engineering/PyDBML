from pydbml.core.engine import Engine


def test_skip_if_basic():
    engine = Engine()

    engine.execute("""
    !sum = 0

    do !i from 1 to 5
      skip if(!i == 3)
      !sum = !sum + 1
    enddo
    """)

    result = engine.env.get("sum").get().value
    assert result == 4  # skipped 3


def test_skip_if_multiple_skips():
    engine = Engine()

    engine.execute("""
    !count = 0

    do !i from 1 to 5
      skip if(!i > 3)
      !count = !count + 1
    enddo
    """)

    result = engine.env.get("count").get().value
    assert result == 3  # 1,2,3 only


def test_skip_if_with_break():
    engine = Engine()

    engine.execute("""
    !x = 0

    do
      !x = !x + 1
      skip if(!x == 2)
      break if(!x > 3)
    enddo
    """)

    result = engine.env.get("x").get().value
    assert result == 4
