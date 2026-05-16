from pydbml.core.engine import Engine


def test_multi_dim_basic():
    engine = Engine()

    engine.execute("""
    !!arr = object array()

    !!arr[1] = object array()
    !!arr[1][1] = 10
    !!arr[1][2] = 20

    !!arr[2] = object array()
    !!arr[2][1] = 30
    !!arr[2][2] = 40

    !a = !!arr[1][2]
    !b = !!arr[2][1]
    """)

    assert engine.env.get("a").get().value == 20
    assert engine.env.get("b").get().value == 30

def test_multi_dim_3d():
    engine = Engine()

    engine.execute("""
    !!arr = object array()

    !!arr[1] = object array()
    !!arr[1][1] = object array()

    !!arr[1][1][1] = 100
    !!arr[1][1][2] = 200

    !x = !!arr[1][1][2]
    """)

    assert engine.env.get("x").get().value == 200

def test_multi_dim_with_variables():
    engine = Engine()

    engine.execute("""
    !!arr = object array()

    !i = 1
    !j = 2

    !!arr[!i] = object array()
    !!arr[!i][!j] = 50

    !x = !!arr[!i][!j]
    """)

    assert engine.env.get("x").get().value == 50

def test_multi_dim_loop():
    engine = Engine()

    engine.execute("""
    !!arr = object array()

    !!arr[1] = object array()
    !!arr[1][1] = 10
    !!arr[1][2] = 20

    !!arr[2] = object array()
    !!arr[2][1] = 30
    !!arr[2][2] = 40

    !!sum = 0

    do !i indices !!arr
        do !j indices !!arr[!i]
            !!sum = !!sum + !!arr[!i][!j]
        enddo
    enddo
    """)

    assert engine.env.get_global("sum").get().value == 100

def test_multi_dim_with_skip_break():
    engine = Engine()

    engine.execute("""
    !!arr = object array()

    !!arr[1] = object array()
    !!arr[1][1] = 10
    !!arr[1][2] = 20

    !!arr[2] = object array()
    !!arr[2][1] = 30
    !!arr[2][2] = 40

    !!sum = 0

    do !i indices !!arr
        do !j indices !!arr[!i]
            skip if(!!arr[!i][!j] == 20)
            break if(!!arr[!i][!j] == 30)
            !!sum = !!sum + !!arr[!i][!j]
        enddo
    enddo
    """)

    assert engine.env.get_global("sum").get().value == 10

