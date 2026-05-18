# pydbml/plugins.py


def pydbml_class(name=None):
    """
    Supports:
    @pydbml_class
    @pydbml_class("custom")
    """
    if callable(name):
        cls = name
        cls._pydbml_class = True
        cls._pydbml_class_name = cls.__name__.lower()
        return cls

    def wrapper(cls):
        cls._pydbml_class = True
        cls._pydbml_class_name = (name or cls.__name__).lower()
        return cls

    return wrapper


def pydbml_method(name=None):
    """
    Supports:
    @pydbml_method
    @pydbml_method("EQ")
    """
    if callable(name):
        func = name
        func._pydbml_method = True
        func._pydbml_method_name = func.__name__.upper()
        return func

    def wrapper(func):
        func._pydbml_method = True
        func._pydbml_method_name = (name or func.__name__).upper()
        return func

    return wrapper


def pydbml_member(name=None):
    """
    Supports:
    @pydbml_member
    @pydbml_member("attr")
    """
    if callable(name):
        func = name
        func._pydbml_member = True
        func._pydbml_member_name = func.__name__.lower()
        return func

    def wrapper(func):
        func._pydbml_member = True
        func._pydbml_member_name = (name or func.__name__).lower()
        return func

    return wrapper


def pydbml_function(name=None):
    """
    Supports:
    @pydbml_function
    @pydbml_function("myfunc")
    """
    if callable(name):
        func = name
        func._pydbml_function = True
        func._pydbml_function_name = func.__name__.lower()
        return func

    def wrapper(func):
        func._pydbml_function = True
        func._pydbml_function_name = (name or func.__name__).lower()
        return func

    return wrapper


def pydbml_operator(symbol):
    """
    Always requires symbol:
    @pydbml_operator("+")
    """
    def wrapper(func):
        func._pydbml_operator = symbol
        return func

    return wrapper


def pydbml_operator(symbol):
    def wrapper(func):
        func._pydbml_operator = True
        
        if not hasattr(func, "_pydbml_operator_names"):
            func._pydbml_operator_names = set()

        func._pydbml_operator_names.add(symbol)
        return func
    return wrapper
