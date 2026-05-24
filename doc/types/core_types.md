
# Core Types

## 1. Overview

PyDBML provides a set of core runtime types used during evaluation.

All values in the system are instances of these types or are derived from them.

---

## 2. Real

Represents numeric values.

### Examples

```

5
10.5
-3

```

### Behavior

- Supports arithmetic operations: `+`, `-`, `*`, `/`
- Can represent integers and floating-point numbers
- Automatically converted to Python `int` or `float` during integration

---

## 3. String

Represents textual data.

### Examples

```

|hello|
'world'

```

### Behavior

- Supports concatenation using `+`
- Can be passed directly to Python methods
- Internally mapped to Python `str`

---

## 4. Boolean

Represents logical truth values.

### Values

```

true
false

```

### Behavior

- Used in conditional expressions
- Supports logical operators:
  - `AND`
  - `OR`
  - `NOT`
- Internally mapped to Python `bool`

---

## 5. Array

Represents an indexed collection of values.

### Example

```

!arr = \[1, 2, 3]

```

### Behavior

- Access elements using index:

```

!arr\[0]

```

- Supports iteration:
  - `values`
  - `indices`
- Internally mapped to Python `list`

---

## 6. ObjectInstance

Represents user-defined PyDBML objects.

### Behavior

- Created using `object` keyword
- Contains:
  - attributes
  - methods
- Methods are defined within object definitions

---

### Example

```

!obj = object MyType()

```

---

## 7. PluginObject (Python Integration)

Represents wrapped Python objects.

### Definition

```

PluginObject(obj)

```

---

### Behavior

- Wraps native Python objects (e.g., file handles, library objects)
- Used for interoperability between PyDBML and Python
- Supports:
  - method calls
  - attribute access
  - dynamic behavior

---

### Example

```

import module builtins

!f = object open('file.txt', 'w')

```

Here:

```

open() → returns Python object
→ wrapped as PluginObject

```

---

## 8. Type Conversion

PyDBML automatically converts between its types and Python types.

---

### 8.1 PyDBML → Python

| PyDBML Type | Python Type |
|------------|------------|
| Real        | int / float |
| String      | str |
| Boolean     | bool |
| Array       | list |
| ObjectInstance | custom object |
| PluginObject | native Python object |

---

### 8.2 Python → PyDBML

- Primitive values → converted to equivalent type
- Complex objects → wrapped as `PluginObject`

---

## 9. Type Behavior in Expressions

All types can participate in expressions:

```

!x = 5 + 3
!y = |a| + |b|
!z = true AND false

```

### Rules

- Operators determine valid type combinations
- Invalid type combinations result in:

```

TYPE\_ERROR

```

---

## 10. Method Support

Types support method calls depending on their implementation:

```

!obj.method()

```

### Resolution

- PyDBML method (ObjectInstance)
- Plugin method
- Python method (for PluginObject)

---

## 11. Python Integration

Core types work seamlessly with Python:

```

import module builtins

!f = object open('file.txt', 'w')
!f.write('Hello')

```

---

## 12. Design Guarantees

Core types guarantee:

- consistent runtime representation
- seamless Python interoperability
- predictable behavior in expressions
- dynamic extensibility

---

## 13. Limitations

- No static type enforcement for variables
- Limited built-in methods per type
- Python object safety depends on runtime restrictions
