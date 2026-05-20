from pydbml.types.real import Real
from pydbml.types.string import String
from pydbml.types.array import Array
from pydbml.types.object import ObjectInstance


def get_class_from_type(var_type: str):
    if var_type == "number":
        return Real

    if var_type == "string":
        return String

    if var_type == "array":
        return Array

    if var_type == "object":
        return ObjectInstance

    return None

def get_methods_from_class(cls, evaluator):
    if cls is None:
        return []

    # ✅ ensure cache is built
    if cls not in evaluator._method_cache:
        evaluator._build_cache(cls)

    method_map = evaluator._method_cache.get(cls, {})

    # ✅ return method names (lowercase)
    return [name.lower() for name in method_map.keys()]

