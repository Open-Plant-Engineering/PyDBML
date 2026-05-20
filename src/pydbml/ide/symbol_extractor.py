from pydbml.ast.nodes import AssignNode, FunctionDefNode, ObjectNode


def extract_symbols(ast):
    variables = set()
    functions = set()
    objects = set()

    for node in ast:
        # ✅ variables (both !x and !!x)
        if isinstance(node, AssignNode):
            variables.add(node.name)

            # ✅ detect object assignment
            if isinstance(node.value, ObjectNode):
                objects.add(node.name)

        # ✅ function definitions
        elif isinstance(node, FunctionDefNode):
            functions.add(node.name)

    return {
        "variables": list(variables),
        "functions": list(functions),
        "objects": list(objects)
    }

import re
def extract_symbols_safe(code: str):
    import re

    variables = set()
    functions = set()
    objects = set()

    var_matches = re.findall(r"!([a-zA-Z_][a-zA-Z0-9_]*)", code)
    func_matches = re.findall(r"!!([a-zA-Z_][a-zA-Z0-9_]*)", code)

    # ✅ basic heuristic
    obj_matches = re.findall(r"!([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*object", code, re.IGNORECASE)

    variables.update(var_matches)
    functions.update(func_matches)
    objects.update(obj_matches)

    return {
        "variables": list(variables),
        "functions": list(functions),
        "objects": list(objects)
    }