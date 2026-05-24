# Type System Specification

## 1. Overview

PyDBML uses a runtime type system.

All values have an associated type that determines:

- allowed operations
- method availability
- assignment validity
- behavior during evaluation

Types are enforced dynamically during execution.

PyDBML also supports integration with Python types through a bridging mechanism.

---

## 2. Core Types

The following primary types exist:

| Type | Description |
|------|------------|
| Real | Numeric values (integer and floating point) |
| String | Textual data |
| Boolean | Logical values (true/false) |
| Array | Indexed collection |
| ObjectInstance | User-defined structured object |
| PluginObject | Wrapped Python object |

---

## 3. Internal Representation

Each value is represented as a runtime object:

```

value → instance of PyDBML type class

```

Examples:

```

5        → Real
'abc'    → String
true     → Boolean

```

Python-derived values:

```

file handle → PluginObject

```

---

## 4. Type Identity

Type identity is determined by:

```

type(value) → runtime type class

```

Example:

```

type(Real(5)) → Real

```

---

## 5. Type Equality

Two values are considered compatible if:

```

same type
OR
allowed conversion applies

```

---

## 6. Type Enforcement

---

### 6.1 Assignment

```

!x = expression

```

Rules:

- Expression is evaluated first
- Result is stored directly
- Variable type is not fixed and can change dynamically

---

### 6.2 Function Parameters

```

define function !!f(a, b) is real

```

Rules:

- Arguments are evaluated before binding
- Expected types are validated at runtime
- Type mismatch → TYPE_ERROR

---

### 6.3 Return Type

```

return value

```

Rules:

- Returned value must match declared type
- Mismatch → RETURN_TYPE error

---

## 7. Type Conversion (Coercion)

---

### 7.1 Automatic Conversion

Limited implicit conversions are supported:

| From | To | Behavior |
|------|----|---------|
| int → Real | automatic |
| float → Real | automatic |
| PyDBML → Python | automatic during method/function call |

---

### 7.2 Python Conversion

When calling Python:

- PyDBML values → converted to Python equivalents
- Python results → converted back:

| Python Type | PyDBML Type |
|-------------|------------|
| int / float | Real |
| str | String |
| bool | Boolean |
| list | Array |
| object | PluginObject |

---

### 7.3 Disallowed Conversion

```

String + Real → TYPE\_ERROR
Boolean + Real → TYPE\_ERROR

```

---

## 8. Operation Rules

---

### 8.1 Arithmetic Operations

Valid:

```

Real + Real → Real

```

Invalid → TYPE_ERROR

---

### 8.2 Comparison Operations

Valid:

```

Real vs Real
String vs String
Boolean vs Boolean

```

Return:

```

Boolean

```

---

### 8.3 Logical Operations

```

AND, OR, NOT

```

Rules:

- Operands must be Boolean
- Short-circuit evaluation applies

---

## 9. String Behavior

Strings:

- support concatenation via `+`
- are immutable
- map directly to Python `str`

Example:

```

|hello| + |world|

```

---

## 10. Array Type

---

### 10.1 Structure

```

index → value

```

---

### 10.2 Index Rules

- Index must be Real
- Converted to integer
- Invalid index → INDEX_ERROR

---

### 10.3 Assignment

```

!arr\[1] = 10

```

---

### 10.4 Retrieval

```

!x = !arr\[1]

```

---

## 11. Object Types

---

### 11.1 ObjectInstance

Represents PyDBML-defined objects:

```

attributes
methods

```

---

### 11.2 PluginObject

Represents Python-backed objects:

```

PluginObject:
obj → underlying Python object

````

---

### Behavior

- Supports method calls
- Supports attribute access via reflection
- Used for all Python integrations

---

## 12. Plugin Types

---

### 12.1 Definition

Plugin types are defined in Python:

```python
@pydbml_class
class Custom:
````

***

### 12.2 Behavior

* Methods exposed via decorators
* Operators mapped via Python functions
* Used as runtime types inside PyDBML

***

### 12.3 Execution

* Arguments converted to Python
* Method executed
* Result converted back to PyDBML

***

## 13. Type Checking

***

### 13.1 Runtime Check

```
check_type(value, expected_type)
```

***

### 13.2 Behavior

```
match → valid
mismatch → TYPE_ERROR
```

***

## 14. Type Errors

***

### 14.1 Occurrence

Type errors occur when:

* invalid operations
* invalid assignments
* incompatible function arguments
* invalid return values
* wrong method usage

***

### 14.2 Behavior

```
TYPE_ERROR raised immediately
execution interrupted
```

***

## 15. Evaluation Interaction

Types participate directly in evaluation:

```
evaluate(expression) → value(type)
```

Operators depend on type:

```
Real    → arithmetic
String  → concatenation
Array   → indexing
Object  → method access
```

***

## 16. Type Stability

Variable types are dynamic:

```
!x = 5
!x = 'abc'
```

Result:

* value replaced
* type updated dynamically

***

## 17. Python Integration

The type system supports seamless Python interoperability.

***

### Behavior

* Python objects are wrapped as PluginObject
* Python methods can operate directly on converted values
* Returned values are normalized

***

### Example

```
import module builtins

!f = object open('file.txt', 'w')
!f.write('Hello')
```

***

## 18. Type Safety Guarantees

The system guarantees:

* runtime validation before operations
* prevention of invalid type combinations
* consistent behavior across execution
* safe integration with Python types

***

## 19. Edge Cases

***

### Mixing Types

```
5 + 'abc' → TYPE_ERROR
```

***

### Boolean in Arithmetic

```
true + 1 → TYPE_ERROR
```

***

### Python Object Handling

```
file.write(...) → allowed
file + 1 → TYPE_ERROR
```

***

## 20. Type Extension

Types can be extended via:

* plugins
* Python integration
* custom objects

***

## 21. Limitations

The type system does not include:

* static typing
* compile-time validation
* generics
* inheritance hierarchy (limited)

***

## 22. Example

```
!x = 5
!y = 10
!z = !x + !y
```

Execution:

```
Real + Real → Real
```

***

## 23. Summary

The PyDBML type system:

* is dynamic and runtime-based
* enforces correctness during execution
* supports extensibility via plugins
* enables seamless integration with Python

