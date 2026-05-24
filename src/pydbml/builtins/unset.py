from pydbml.types.boolean import Boolean
from pydbml.types.unset import UNSET

def builtin_unset(evaluator, args, node):

    if len(args) != 1:
        raise raise_error(
            "ARG_COUNT",
            "unset() expects 1 argument",
            node=node
        )

    val = args[0]

    return Boolean(val is UNSET)

builtin_unset._allow_method = True
builtin_unset._raw_args = False
