from pydbml.core.engine import Engine


def test_do_range_with_global_bounds():
    engine = Engine()

    engine.execute("""
    !!start = 2
    !!end = 5
    !!sum = 0

    do !i from !!start to !!end
        !!sum = !!sum + !i
    enddo
    """)

    assert engine.env.get_global("sum").get().value == 14

def test_do_range_with_global_step():
    engine = Engine()

    engine.execute("""
    !!start = 1
    !!end = 7
    !!step = 2
    !!sum = 0

    do !i from !!start to !!end by !!step
        !!sum = !!sum + !i
    enddo
    """)

    assert engine.env.get_global("sum").get().value == 16  # 1+3+5+7

def test_do_skip_if_with_global():
    engine = Engine()

    engine.execute("""
    !!skip_val = 3
    !!sum = 0

    do !i from 1 to 5
        skip if(!i == !!skip_val)
        !!sum = !!sum + !i
    enddo
    """)

    assert engine.env.get_global("sum").get().value == 12  # 1+2+4+5

def test_do_break_if_with_global():
    engine = Engine()

    engine.execute("""
    !!limit = 3
    !!sum = 0

    do !i from 1 to 10
        break if(!i > !!limit)
        !!sum = !!sum + !i
    enddo
    """)

    assert engine.env.get_global("sum").get().value == 6  # 1+2+3

def test_do_skip_and_break_with_globals():
    engine = Engine()

    engine.execute("""
    !!skip_val = 2
    !!limit = 4
    !!sum = 0

    do !i from 1 to 10
        skip if(!i == !!skip_val)
        break if(!i > !!limit)
        !!sum = !!sum + !i
    enddo
    """)

    assert engine.env.get_global("sum").get().value == 8  # 1+3+4

def test_values_loop_global_array():
    engine = Engine()

    engine.execute("""
    !!arr = object array()
    !!arr[1] = 10
    !!arr[2] = 20
    !!arr[3] = 30

    !!sum = 0

    do !v values !!arr
        !!sum = !!sum + !v
    enddo
    """)

    assert engine.env.get_global("sum").get().value == 60

def test_values_loop_skip_if_global():
    engine = Engine()

    engine.execute("""
    !!arr = object array()
    !!arr[1] = 10
    !!arr[2] = 20
    !!arr[3] = 30

    !!skip_val = 20
    !!sum = 0

    do !v values !!arr
        skip if(!v == !!skip_val)
        !!sum = !!sum + !v
    enddo
    """)

    assert engine.env.get_global("sum").get().value == 40

def test_indices_loop_global_array():
    engine = Engine()

    engine.execute("""
    !!arr = object array()
    !!arr[1] = 5
    !!arr[2] = 10
    !!arr[3] = 15

    !!sum = 0

    do !i indices !!arr
        !!sum = !!sum + !i
    enddo
    """)

    assert engine.env.get_global("sum").get().value == 6

def test_indices_loop_break_if_global():
    engine = Engine()

    engine.execute("""
    !!arr = object array()
    !!arr[1] = 5
    !!arr[2] = 10
    !!arr[3] = 15

    !!limit = 2
    !!sum = 0

    do !i indices !!arr
        break if(!i > !!limit)
        !!sum = !!sum + !i
    enddo
    """)

    assert engine.env.get_global("sum").get().value == 3

def test_modify_global_inside_loop():
    engine = Engine()

    engine.execute("""
    !!g = 0

    do !i from 1 to 5
        !!g = !!g + !i
    enddo
    """)

    assert engine.env.get_global("g").get().value == 15

def test_global_bound_static_behavior():
    engine = Engine()

    engine.execute("""
    !!g = 3
    !!count = 0

    do !i from 1 to !!g
        !!g = !!g + 1
        !!count = !!count + 1
    enddo
    """)

    assert engine.env.get_global("count").get().value == 3


