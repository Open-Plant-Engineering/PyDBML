from pydbml.types.primitives import Number, Boolean


class MethodRegistry:

    _methods = {}

    @classmethod
    def register(cls, name):
        def decorator(func):
            cls._methods[name.upper()] = func
            return func
        return decorator

    @classmethod
    def call(cls, name, target, args):
        name = name.upper()

        if name not in cls._methods:
            raise Exception(f"Unknown method: {name}")

        return cls._methods[name](target, args)

@MethodRegistry.register("EQ")
def eq(target, args):
    return Boolean(target.value == args[0].value)


@MethodRegistry.register("NEQ")
def neq(target, args):
    return Boolean(target.value != args[0].value)


@MethodRegistry.register("GT")
def gt(target, args):
    return Boolean(target.value > args[0].value)


@MethodRegistry.register("LT")
def lt(target, args):
    return Boolean(target.value < args[0].value)


@MethodRegistry.register("GEQ")
def geq(target, args):
    return Boolean(target.value >= args[0].value)


@MethodRegistry.register("LEQ")
def leq(target, args):
    return Boolean(target.value <= args[0].value)

@MethodRegistry.register("AND")
def and_func(target, args):
    return Boolean(target.value and args[0].value)


@MethodRegistry.register("OR")
def or_func(target, args):
    return Boolean(target.value or args[0].value)


@MethodRegistry.register("NOT")
def not_func(target, args):
    return Boolean(not target.value)

@MethodRegistry.register("ADD")
def add(target, args):
    return Number(target.value + args[0].value)


@MethodRegistry.register("SUB")
def sub(target, args):
    return Number(target.value - args[0].value)


@MethodRegistry.register("MUL")
def mul(target, args):
    return Number(target.value * args[0].value)


@MethodRegistry.register("DIV")
def div(target, args):
    return Number(target.value / args[0].value)

@MethodRegistry.register("GET")
def get(target, args):
    return target.get(int(args[0].value))


@MethodRegistry.register("SET")
def set_(target, args):
    index = int(args[0].value)
    value = args[1]
    target.set(index, value)
    return value

@MethodRegistry.register("LENGTH")
def length(target, args):
    return Number(len(target.value))
