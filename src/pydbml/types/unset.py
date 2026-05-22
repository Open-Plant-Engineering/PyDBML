from .base import PyDBMLType

class Unset(PyDBMLType):
    def __init__(self):
        super().__init__(None)

    def validate(self):
        pass

    def __repr__(self):
        return "<UNSET>"

    def __str__(self):
        return "unset"


# ✅ Singleton
UNSET = Unset()