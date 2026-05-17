# pydbml/plugins.py

def pydbml_class(cls):
    cls._pydbml_class = True
    return cls


def pydbml_method(func):
    func._pydbml_method = True
    return func


def pydbml_member(func):
    func._pydbml_member = True
    return func


def pydbml_function(func):
    func._pydbml_function = True
    return func


def pydbml_operator(symbol):
    def wrapper(func):
        func._pydbml_operator = symbol
        return func
    return wrapper
