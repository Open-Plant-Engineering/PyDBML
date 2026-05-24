from pydbml.types.boolean import Boolean
from pydbml.ast.nodes import VariableNode
from pydbml.runtime.error_codes import raise_error


def builtin_undefined(evaluator, args, node):

    if len(args) != 1:
        raise raise_error(
            "ARG_COUNT",
            "undefined() expects 1 argument",
            node=node
        )

    arg = args[0]

    # ✅ we expect raw AST node
    if isinstance(arg, VariableNode):
        try:
            if arg.is_global:
                evaluator.env.get_global(arg.name)
            else:
                evaluator.env.get(arg.name)

            return Boolean(False)

        except KeyError:
            return Boolean(True)

    raise raise_error(
        "TYPE_ERROR",
        "undefined() expects variable reference (!x)",
        node=node
    )


# ✅ IMPORTANT FLAG
builtin_undefined._raw_args = True
builtin_undefined._allow_method = True