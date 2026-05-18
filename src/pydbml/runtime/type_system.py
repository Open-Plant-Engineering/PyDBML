from pydbml.types.number import Number
from pydbml.types.string import String
from pydbml.types.boolean import Boolean
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