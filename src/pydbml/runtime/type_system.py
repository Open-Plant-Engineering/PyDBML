from pydbml.types.real import Real
from pydbml.types.string import String
from pydbml.types.boolean import Boolean
from pydbml.types.array import Array


TYPE_MAP = {
    "REAL": Real,
    "STRING": String,
    "BOOLEAN": Boolean,
    "ARRAY": Array,
}


def check_type(value, expected_type):
    # ✅ normalize once
    if isinstance(expected_type, str):
        expected_type = expected_type.upper()
    else:
        raise TypeError(f"Invalid type specifier: {expected_type}")

    # ✅ unknown type
    if expected_type not in TYPE_MAP:
        raise TypeError(f"Unknown type: {expected_type}")

    expected_cls = TYPE_MAP[expected_type]

    # ✅ allow None (important for runtime)
    if value is None:
        return True

    return isinstance(value, expected_cls)