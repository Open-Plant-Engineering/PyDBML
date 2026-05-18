class PyDBMLError(Exception):
    def __init__(self, code1, code2, message=""):
        self.code1 = code1
        self.code2 = code2
        self.message = message

    def __str__(self):
        return f"({self.code1}, {self.code2}) {self.message}"