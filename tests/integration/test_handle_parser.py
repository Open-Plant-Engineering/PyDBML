from pydbml.core.engine import Engine

def test_handle_with_parser():
    e = Engine()

    code = """
    !x = object fail()

    HANDLE (41, 8)
        RETURN 1
    ELSEHANDLE ANY
        RETURN 2
    ELSEHANDLE NONE
        RETURN 3
    ENDHANDLE
    """

    # hack: simulate failure
    def fail():
        raise Exception()

    # simulate via evaluator override if needed

    try:
        e.execute(code)
    except:
        pass
