from typing import Dict
from pydbml.runtime.variable import Variable
from pydbml.types.base import PyDBMLType

class Environment:
    """
    Runtime environment for PyDBML.
    
    Responsibilities:
        ✔ manage variable scopes (local + global)
        ✔ provide variable lookup and assignment
        ✔ support nested execution contexts
    
    Design:
        - stack-based local scopes
        - separate global namespace
        - case-insensitive variable names
    
    Behavior:
        - lookup: local → global
        - assignment: always current scope unless global
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
            if name in self._global:
                self._global[name].set(value)
            else:
                self._global[name] = Variable(name, value, True)
        else:
            scope = self._local_stack[-1]
            if name in scope:
                scope[name].set(value)
            else:
                scope[name] = Variable(name, value, False)

    # --------------------------
    # Get variable
    # --------------------------
    def get(self, name: str):
        name = name.lower()

        # ✅ search local stack (inner → outer)
        for scope in reversed(self._local_stack):
            if name in scope:
                return scope[name]

        # ✅ fallback to global
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
    # Delete variable
    # --------------------------
    def delete(self, name: str):
        name = name.lower()

        # ✅ search from inner → outer
        for scope in reversed(self._local_stack):
            if name in self._local_stack[-1]:
                del self._local_stack[-1][name]
                return

        # ✅ fallback: global
        if name in self._global:
            del self._global[name]
            return

        raise KeyError(f"Variable '{name}' not defined")

    # --------------------------
    # Push new scope
    # --------------------------
    def push_scope(self):
        self._local_stack.append({})

    # --------------------------
    # Pop scope
    # --------------------------
    def pop_scope(self):
        if len(self._local_stack) <= 1:
            raise RuntimeError("Cannot pop global scope")

        self._local_stack.pop()
