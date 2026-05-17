from pydbml.plugins import pydbml_class, pydbml_method, pydbml_function

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