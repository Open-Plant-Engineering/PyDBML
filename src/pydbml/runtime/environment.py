from typing import Dict
from pydbml.runtime.variable import Variable
from pydbml.types.base import PyDBMLType
from pydbml.utils.debug import debug

class Environment:
    """
    Runtime environment with proper scope handling.
    """

    def __init__(self):
        self._local: Dict[str, Variable] = {}
        self._global: Dict[str, Variable] = {}

    # --------------------------
    # Set Variable
    # --------------------------
    def set(self, name: str, value: PyDBMLType, is_global: bool = False):
        name = name.lower()
        var = Variable(name, value, is_global)

        if is_global:
            self._global[name] = var
        else:
            self._local[name] = var
        debug("ENV SET", f"{name} = {value}")

    # --------------------------
    # Get Variable (IMPORTANT)
    # --------------------------
    def get(self, name: str) -> Variable:
        """
        Lookup order:
        1. Local
        2. Global
        """
        name = name.lower()
        debug("ENV GET", f"{name} -> {self._local.get(name) or self._global.get(name)}")
        if name in self._local:
            return self._local[name]

        if name in self._global:
            return self._global[name]

        raise KeyError(f"Variable '{name}' not defined")

    # --------------------------
    # Explicit Global Access
    # --------------------------
    def get_global(self, name: str) -> Variable:
        name = name.lower()
        if name not in self._global:
            raise KeyError(f"Global variable '{name}' not found")

        return self._global[name]

    # --------------------------
    # Delete Variable
    # --------------------------
    def delete(self, name: str, is_global: bool = False):
        if is_global:
            if name in self._global:
                del self._global[name]
        else:
            if name in self._local:
                del self._local[name]