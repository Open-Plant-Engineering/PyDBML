from pydbml.core.engine import Engine
from pydbml.runtime.exceptions import PyDBMLError

def test_plugin_error_handle():

    e = Engine()

    # inject fake plugin function
    def fail():
        raise PyDBMLError(41, 8)

    e.evaluator.registry.functions["fail"] = fail

    code = """
    !!fail()

    HANDLE (41, 8)
        RETURN 111
    ELSEHANDLE ANY
        RETURN 999
    ENDHANDLE
    """

    r = e.execute(code)

    assert r.value == 111