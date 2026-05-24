from dataclasses import dataclass


@dataclass
class Token:

    def __init__(self, type, value, line=None, column=None):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        if self.line is not None:
            return f"{self.type}({self.value})@{self.line}:{self.column}"
        return f"{self.type}({self.value})"
