from pydbml.types.primitives import String, Number, Boolean
from pydbml.types.array import Array


class Resolver:
    """
    Responsible for converting raw input into PyDBML objects.
    """

    def __init__(self, env):
        self.env = env

    def resolve(self, raw: str):
        raw = raw.strip()
        raw_lower = raw.lower()

        # --------------------------
        # Object creation
        # --------------------------
        if raw_lower == "object array()":
            return Array()

        if raw_lower == "object string()":
            return String("")

        if raw_lower == "object real()":
            return Number(0)

        if raw_lower == "object boolean()":
            return Boolean(False)

        # --------------------------
        # String literal
        # --------------------------
        if raw.startswith("'") and raw.endswith("'"):
            return String(raw.strip("'"))

        # --------------------------
        # Boolean
        # --------------------------
        if raw_lower in ("true", "false"):
            return Boolean(raw_lower == "true")

        # --------------------------
        # Number
        # --------------------------
        try:
            return Number(int(raw))
        except ValueError:
            try:
                return Number(float(raw))
            except ValueError:
                pass

        # --------------------------
        # Variable reference
        # --------------------------
        if raw.startswith("!"):
            return self._resolve_variable(raw)

        raise ValueError(f"Unsupported value: {raw}")

    def _resolve_variable(self, name: str):
        is_global = name.startswith("!!")
        clean = name.replace("!", "")
    
        if is_global:
            return self.env.get_global(clean).get()
    
        return self.env.get(clean).get()