from pydbml.plugins import pydbml_class, pydbml_method, pydbml_function, pydbml_operator

@pydbml_class
class MyClass:

    def __init__(self):
        self.value = 0

    @pydbml_method
    def add(self, x):
        self.value += x
        return self.value

    @pydbml_method
    def get(self):
        return self.value


@pydbml_function
def multiply(a, b):
    return a * b

@pydbml_function
def get_dict():
    return {1: 100, 2: 200}

@pydbml_function
def get_list():
    return [10, 20, 30]

@pydbml_function
def get_nested():
    return {1: [1, 2], 2: [3, 4]}

@pydbml_function
def check():
    return True

@pydbml_function
def get_tuple():
    return (10, 20, 30)

@pydbml_function
def get_nested_tuple():
    return {1: (1, 2), 2: (3, 4)}

@pydbml_function
def get_set():
    return {10, 20, 30}

@pydbml_function
def get_nested_set():
    return {1: {1, 2}, 2: {3, 4}}

@pydbml_function
def get_mixed():
    return [1, {10, 20}, (30, 40)]


@pydbml_class
class Vec:
    def __init__(self, x):
        self.x = x

    @pydbml_method
    @pydbml_operator("+")
    def add(self, other):
        return Vec(self.x + other.x)

    @pydbml_method
    @pydbml_operator(">")
    def gt(self, other):
        return self.x > other.x

    @pydbml_method
    @pydbml_operator("*")
    def mul(self, other):
        return Vec(self.x * other.x)

    @pydbml_method
    @pydbml_operator("<")
    def lt(self, other):
        return self.x < other.x

    # ✅ only method (NOT operator)
    @pydbml_method
    def eq(self, other):
        return self.x == other.x
