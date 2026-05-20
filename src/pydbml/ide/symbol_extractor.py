from pydbml.ast.nodes import AssignNode, FunctionDefNode, ObjectNode, NumberNode, StringNode


def extract_symbols(ast):
    variables = {}
    functions = set()
    objects = set()

    for node in ast:
        if isinstance(node, AssignNode):
            name = node.name

            # ✅ detect type
            if isinstance(node.value, ObjectNode):
                var_type = "object"
                objects.add(name)

            elif isinstance(node.value, NumberNode):
                var_type = "number"

            elif isinstance(node.value, StringNode):
                var_type = "string"

            else:
                var_type = "unknown"

            variables[name] = var_type

        elif isinstance(node, FunctionDefNode):
            functions.add(node.name)

    return {
        "variables": variables,   # ✅ changed
        "functions": list(functions),
        "objects": list(objects)
    }

import re

def extract_symbols_safe(code: str):
    import re

    variables = {}
    functions = set()
    objects = set()

    var_matches = re.findall(r"!([a-zA-Z_][a-zA-Z0-9_]*)", code)
    func_matches = re.findall(r"!!([a-zA-Z_][a-zA-Z0-9_]*)", code)

    obj_matches = re.findall(
        r"!([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*object",
        code,
        re.IGNORECASE
    )

    # ✅ detect number assignments
    num_matches = re.findall(
        r"!([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([0-9]+(\.[0-9]+)?)",
        code
    )

    # ✅ detect string assignments
    str_matches = re.findall(
        r"!([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\".*?\"",
        code
    )

    # default unknown
    for var in var_matches:
        variables[var] = "unknown"

    # override types
    for match in num_matches:
        variables[match[0]] = "number"

    for match in str_matches:
        variables[match[0]] = "string"

    # objects override
    for obj in obj_matches:
        variables[obj] = "object"
        objects.add(obj)

    for func in func_matches:
        functions.add(func)

    return {
        "variables": variables,
        "functions": list(functions),
        "objects": list(objects)
    }