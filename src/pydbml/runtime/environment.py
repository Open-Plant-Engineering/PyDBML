from typing import Dict
from pydbml.runtime.variable import Variable


class Environment:
    """
    Runtime environment managing variables.
    """

    def __init__(self):
        self._local: Dict[str, Variable] = {}
        self._global: Dict[str, Variable] = {}

    def set(self, name: str, value, is_global: bool = False) -> None:
        var = Variable(name, value, is_global)

        if is_global:
            self._global[name] = var
        else:
            self._local[name] = var

    def get(self, name: str, is_global: bool = False) -> Variable:
        if is_global:
            if name not in self._global:
                raise KeyError(f"Global variable '{name}' not found")
            return self._global[name]

        if name not in self._local:
            raise KeyError(f"Local variable '{name}' not found")

        return self._local[name]

    def delete(self, name: str, is_global: bool = False) -> None:
        if is_global:
            if name in self._global:
                del self._global[name]
        else:
            if name in self._local:
                del self._local[name]