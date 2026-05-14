from pydbml.runtime.environment import Environment
from pydbml.types.array import Array
from pydbml.types.primitives import String, Number, Boolean

class Evaluator:
    """
    Handles execution logic (temporary until parser is introduced).
    """

    def __init__(self):
        self.env = Environment()

    def evaluate(self, code: str):
        code = code.strip()

        # Assignment
        if "=" in code:
            return self._handle_assignment(code)

        # Variable access
        return self._handle_lookup(code)

    # --------------------------
    # Assignment
    # --------------------------
    def _handle_assignment(self, code: str):
        lhs, rhs = code.split("=", 1)
        lhs = lhs.strip()
        rhs = rhs.strip()

        # ✅ Detect array assignment
        if "[" in lhs and "]" in lhs:
            return self._handle_array_assignment(lhs, rhs)

        is_global = lhs.startswith("!!")
        name = lhs.replace("!", "")

        value = self._parse_value(rhs)

        self.env.set(name, value, is_global=is_global)

        return f"{name} set"

    # --------------------------
    # Lookup
    # --------------------------
    def _handle_lookup(self, code: str):
        is_global = code.startswith("!!")
        name = code.replace("!", "")

        var = self.env.get(name, is_global=is_global)
        return var.get()

    # --------------------------
    # Value Parsing (TEMP)
    # --------------------------
    def _parse_value(self, raw: str):

        raw = raw.strip()

        raw_lower = raw.lower()

        # ✅ PML-style object creation
        if raw_lower == "object array()":
            return Array()

        if raw_lower == "object string()":
            return String("")

        if raw_lower == "object real()":
            return Number(0)

        if raw_lower == "object boolean()":
            return Boolean(False)

        # string
        if raw.startswith("'") and raw.endswith("'"):
            return String(raw.strip("'"))

        # boolean
        if raw_lower in ("true", "false"):
            return Boolean(raw_lower == "true")

        # number
        try:
            return Number(int(raw))
        except ValueError:
            try:
                return Number(float(raw))
            except ValueError:
                if raw.startswith("!"):
                    return self._resolve_variable(raw)

                raise ValueError(f"Unsupported value: {raw}")
            
    def _resolve_variable(self, name: str):
        is_global = name.startswith("!!")
        clean = name.replace("!", "")

        var = self.env.get(clean, is_global=is_global)
        return var.get()
    
    def _handle_array_assignment(self, lhs: str, rhs: str):
        """
        Handles: !x[1] = value
        """
    
        is_global = lhs.startswith("!!")
    
        # extract name and index
        name_part, index_part = lhs.split("[")
        index = int(index_part.replace("]", "").strip())
        name = name_part.replace("!", "").strip()
    
        var = self.env.get(name, is_global=is_global)
        array_obj = var.get()
    
        if not hasattr(array_obj, "set"):
            raise TypeError(f"{name} is not an array")
    
        value = self._parse_value(rhs)
    
        array_obj.set(index, value)
    
        return f"{name}[{index}] set"