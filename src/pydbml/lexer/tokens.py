from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str

    def __repr__(self):
        return f"{self.type}({self.value})"