from pydbml.types.primitives import Number, String, Boolean
from pydbml.types.array import Array


TYPE_MAP = {
    "REAL": Number,
    "STRING": String,
    "BOOLEAN": Boolean,
    "ARRAY": Array,
}


def check_type(value, expected_type):
    expected_type = expected_type.upper()

    if expected_type not in TYPE_MAP:
        raise Exception(f"Unknown type: {expected_type}")

    return isinstance(value, TYPE_MAP[expected_type])