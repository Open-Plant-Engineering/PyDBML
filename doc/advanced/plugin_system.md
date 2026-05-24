
# Plugin System

## 1. Overview

PyDBML supports extension via Python plugins.

---

## 2. Class Definition

```python
@pydbml_class
class MyClass:
    pass
````

***

## 3. Method Definition

```python
@pydbml_method("METHOD")
def method(self, args):
    ...
```

***

## 4. Operator Definition

```python
@pydbml_operator("+")
def add(self, other):
```

***

## 5. Behavior

* Methods exposed to DSL
* Operators mapped to Python functions

***

## 6. Registration

Plugins are registered during import.

***

## 7. Execution Flow

1. Method resolved
2. Arguments converted
3. Python method executed
4. Result returned

***

## 8. Example

```python
@pydbml_class
class Math:
    @pydbml_method("ADD")
    def add(self, args):
        return args[0] + args[1]
```

````

---

# ✅ ✅ ✅ 5. advanced/standard_library.md

```md
# Standard Library

## 1. Overview

PyDBML provides built-in functions and utilities.

---

## 2. Built-in Functions

### iftrue

````

iftrue(condition, value1, value2)

```

---

## 3. Built-in Operations

- arithmetic operations
- logical operations
- comparisons

---

## 4. Arrays

- indexing
- iteration

---

## 5. Python Integration

Standard library usage can be extended via:

```

import module builtins

```

---

## 6. Future Additions

- string utilities
- math functions
- file helpers