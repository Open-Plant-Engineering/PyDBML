import os
import pytest
from pydbml.core.engine import Engine

engine = Engine()


# ✅ dynamically resolve docs/examples path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
EXAMPLES_DIR = os.path.join(BASE_DIR, "doc", "examples")


def run_file(filename):
    path = os.path.join(EXAMPLES_DIR, filename)

    with open(path, "r") as f:
        code = f.read()

    engine.execute(code)


# --------------------------------------------------
# ✅ EXECUTION TESTS (no expected failure)
# --------------------------------------------------

@pytest.mark.parametrize("file", [
    "example1_nested_loops.pydbml",
    "example2_factorial.pydbml",
    "example3_if.pydbml",
    "example4_short_circuit.pydbml",
    "example5_array.pydbml",
    "example6_values_loop.pydbml",
    "example7_skip.pydbml",
    "example8_break.pydbml",
    "example9_method.pydbml",
    "example10_handle.pydbml",
    "example11_scope.pydbml",
    "example14_nested_calls.pydbml",
    "example15_complex.pydbml",
    "example16_file_write.pydbml",
    "example17_file_read.pydbml",
    "example18_json_usage.pydbml",
    "example19_case_insensitive_methods.pydbml",
    "example20_object_python_mix.pydbml",
    "example21_method_chaining.pydbml",
    "example22_handle_specific_error.pydbml",
    "example23_import_module_usage.pydbml",
])
def test_examples_success(file):
    run_file(file)


# --------------------------------------------------
# ✅ ERROR TESTS (expected failures)
# --------------------------------------------------

@pytest.mark.parametrize("file", [
    "example12_index_error.pydbml",
    "example13_method_not_found.pydbml",
])
def test_examples_failure(file):
    with pytest.raises(Exception):
        run_file(file)