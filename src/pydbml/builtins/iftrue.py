from pydbml.types.boolean import Boolean
from pydbml.runtime.error_codes import raise_error


def builtin_iftrue(evaluator, args, node):

    if len(args) != 3:
        raise raise_error(
            "ARG_COUNT",
            "iftrue expects 3 arguments",
            node=node
        )

    # ✅ already evaluated
    cond = args[0]

    if not isinstance(cond, Boolean):
        raise raise_error(
            "TYPE_ERROR",
            "iftrue condition must be BOOLEAN",
            node=node
        )

    if cond.value:
        return args[1]
    else:
        return args[2]


# ✅ IMPORTANT FLAGS
builtin_iftrue._allow_method = False
builtin_iftrue._raw_args = False