from typing import Dict
from pydbml.runtime.variable import Variable
from pydbml.types.base import PyDBMLType
from pydbml.utils.debug import debug

class Environment:
    """
    Runtime environment with proper scope handling.
    """

    def __init__(self):
        # ✅ stack of local scopes
        self._local_stack = [{}]

        # ✅ global scope
        self._global = {}

    # --------------------------
    # Set variable
    # --------------------------
    def set(self, name: str, value, is_global: bool = False):
        name = name.lower()
        if is_global:
            self._global[name] = Variable(name, value, True)
        else:
            # ✅ always set in current scope
            self._local_stack[-1][name] = Variable(name, value, False)
        debug("ENV SET", f"{name} = {value}")

    # --------------------------
    # Get variable
    # --------------------------
    def get(self, name: str):
        name = name.lower()

        # ✅ search local stack (inner → outer)
        for scope in reversed(self._local_stack):
            if name in scope:
                debug("ENV GET", f"{name} (local) → {scope[name]}")
                return scope[name]

        # ✅ fallback to global
        if name in self._global:
            debug("ENV GET", f"{name} (global) → {self._global[name]}")
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
    # Delete variable
    # --------------------------
    def delete(self, name: str):
        name = name.lower()

        # ✅ search from inner → outer
        # for scope in reversed(self._local_stack):
        # currently we are just deleting from current scope
        if name in self._local_stack[-1]:
            del self._local_stack[-1][name]
            debug("ENV DELETE", f"{name} removed from local scope")
            return

        # ✅ fallback: global
        if name in self._global:
            del self._global[name]
            debug("ENV DELETE", f"{name} removed from global scope")
            return

        raise KeyError(f"Variable '{name}' not defined")

    # --------------------------
    # Push new scope
    # --------------------------
    def push_scope(self):
        self._local_stack.append({})
        debug("ENV", "PUSH SCOPE")

    # --------------------------
    # Pop scope
    # --------------------------
    def pop_scope(self):
        if len(self._local_stack) <= 1:
            raise RuntimeError("Cannot pop global scope")

        self._local_stack.pop()
        debug("ENV", "POP SCOPE")
