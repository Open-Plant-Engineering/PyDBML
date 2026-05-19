# pydbml/plugins.py


def pydbml_class(*names):
    """
    Supports:
    @pydbml_class
    @pydbml_class("custom","Custom2")
    """
    def wrapper(cls):
        cls._pydbml_class = True

        if not hasattr(cls, "_pydbml_class_names"):
            cls._pydbml_class_names = set()

        if not names:
            cls._pydbml_class_names.add(cls.__name__.lower())
        else:
            for name in names:
                cls._pydbml_class_names.add(name.lower())

        return cls

    # ✅ support @pydbml_class without ()
    if len(names) == 1 and callable(names[0]):
        cls = names[0]
        names = ()
        return wrapper(cls)

    return wrapper


def pydbml_method(*names):
    """
    Supports:
    @pydbml_method
    @pydbml_method("EQ")
    """
    def wrapper(func):
        func._pydbml_method = True

        if not hasattr(func, "_pydbml_method_names"):
            func._pydbml_method_names = set()

        if not names:
            func._pydbml_method_names.add(func.__name__.upper())
        else:
            for name in names:
                func._pydbml_method_names.add(name.upper())
        return func

    if len(names) == 1 and callable(names[0]):
        func = names[0]
        names = ()
        return wrapper(func)

    return wrapper


def pydbml_member(*names):
    """
    Supports:
    @pydbml_member
    @pydbml_member("attr")
    """
    def wrapper(func):
        func._pydbml_member = True

        if not hasattr(func, "_pydbml_member_names"):
            func._pydbml_member_names = set()

        if not names:
            func._pydbml_member_names.add(func.__name__.lower())
        else:
            for name in names:
                func._pydbml_member_names.add(name.lower())

        return func

    if len(names) == 1 and callable(names[0]):
        func = names[0]
        names = ()
        return wrapper(func)

    return wrapper


def pydbml_function(*names):
    """
    Supports:
    @pydbml_function
    @pydbml_function("myfunc")
    """
    def wrapper(func):
        func._pydbml_function = True

        if not hasattr(func, "_pydbml_function_names"):
            func._pydbml_function_names = set()

        if not names:
            func._pydbml_function_names.add(func.__name__.lower())
        else:
            for name in names:
                func._pydbml_function_names.add(name.lower())

        return func

    if len(names) == 1 and callable(names[0]):
        func = names[0]
        names = ()
        return wrapper(func)

    return wrapper


def pydbml_operator(*symbols):
    """
    Always requires symbol:
    @pydbml_operator("+","&")
    """
    def wrapper(func):
        func._pydbml_operator = True
        
        if not hasattr(func, "_pydbml_operator_names"):
            func._pydbml_operator_names = set()

        for symbol in symbols:
            func._pydbml_operator_names.add(symbol)
        return func
    return wrapper

def pydbml_extend(*names):
    """
    Supports:
    @pydbml_extend
    @pydbml_extend("number", "string","real","array")
    """
    def wrapper(cls):
        cls._pydbml_extend = True

        if not hasattr(cls, "_pydbml_extend_names"):
            cls._pydbml_extend_names = set()

        # ✅ default: use class name
        if not names:
            cls._pydbml_extend_names.add(cls.__name__.lower())
        else:
            for name in names:
                cls._pydbml_extend_names.add(name.lower())

        return cls

    # ✅ support @pydbml_extend without ()
    if len(names) == 1 and callable(names[0]):
        cls = names[0]
        names = ()
        return wrapper(cls)

    return wrapper
