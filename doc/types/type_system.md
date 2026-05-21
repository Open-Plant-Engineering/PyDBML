# Type System Specification

## 1. Overview

PyDBML uses a runtime type system.

All values have an associated type that determines:

- allowed operations
- method availability
- assignment validity
- behavior during evaluation

Types are enforced at runtime.

---

## 2. Core Types

The following primitive types exist:

| Type | Description |
|------|-------------|
| Real | Numeric values (integer and floating point) |
| String | Textual data |
| Boolean | Logical values (true/false) |
| Array | Indexed collection |
| ObjectInstance | Structured object with attributes and methods |

---

## 3. Internal Representation

Each value is represented as a runtime object:

```

value → instance of PyDBMLType

```

Examples:

```

5       → Real
"abc"   → String
true    → Boolean

```

---

## 4. Type Identity

Type identity is determined by:

```

type(value) → class type

```

Example:

```

type(Real(5)) → Real

```

---

## 5. Type Equality

Two values are compatible if:

```

same type class
OR allowed coercion applies

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
- Result is stored without conversion
- No implicit type change unless explicitly allowed

---

### 6.2 Function Parameters

```

define function !!f(a, b) is real

```

Rules:

- Argument types must match expected parameter types
- If mismatch → TYPE_ERROR

---

### 6.3 Return Type

Functions must return declared type:

```

return value

```

If mismatch:

```

RETURN\_TYPE error

```

---

## 7. Type Conversion (Coercion)

---

### 7.1 Explicit Conversion

Only supported via:

```

plugin logic OR evaluator conversion

```

---

### 7.2 Implicit Conversion

Limited cases allowed:

| From | To | Behavior |
|------|-----|----------|
| int → Real | automatic |
| float → Real | automatic |
| Real → Python numeric | during operator execution |

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

Valid only for:

```

Real + Real → Real

```

Invalid combinations → TYPE_ERROR

---

### 8.2 Comparison Operations

Valid combinations:

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

Operands must be Boolean.

---

## 9. String Behavior

Strings:

- support length operations (plugin)
- support concatenation via operator

Example:

```

"hello" + "world"

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

- Index must be numeric (Real)
- Index converted to integer
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

## 11. Object Type

---

### 11.1 Structure

```

attributes
methods

````

---

### 11.2 Type Behavior

- attributes validated if defined statically
- methods resolved dynamically
- values stored as runtime objects

---

## 12. Plugin Types

---

### 12.1 Definition

Plugins define new types using:

```python
@pydbml_class
````

***

### 12.2 Rules

* plugin class defines behavior
* methods exposed via decorators
* operators mapped to functions

***

### 12.3 Conversion

All plugin results must be converted to PyDBML types.

***

## 13. Type Checking

***

### 13.1 Runtime Check

Function:

```
check_type(value, expected_type)
```

***

### 13.2 Behavior

Returns:

```
true → compatible
false → TYPE_ERROR
```

***

## 14. Type Errors

***

### 14.1 Occurrence

Type errors occur when:

* invalid operation
* invalid assignment
* incompatible function arguments
* invalid return value

***

### 14.2 Behavior

```
TYPE_ERROR raised immediately
execution halted (unless handled)
```

***

## 15. Evaluation Interaction

Types participate in evaluation:

```
evaluate(expression) → value(type)
```

Operators depend on type:

```
Real → arithmetic
String → concatenation
Object → method access
```

***

## 16. Type Stability

Types do not change dynamically:

```
!x = 5
!x = "abc"    (allowed assignment, but replaces value)
```

Variable type is not fixed — value type changes per assignment.

***

## 17. Type Safety Guarantees

The system guarantees:

* operations validated before execution
* invalid combinations prevented
* consistent behavior across runtime

***

## 18. Edge Cases

***

### Mixing Types

```
5 + "abc" → TYPE_ERROR
```

***

### Boolean in Arithmetic

```
true + 1 → TYPE_ERROR
```

***

### Null / None

If exists:

```
treated as special value
limited operations allowed
```

***

## 19. Type Extension

Types can be extended using plugins:

```
methods
operators
new types
```

***

## 20. Limitations

The type system does not include:

* static typing
* compile-time validation
* generics
* inheritance hierarchy (limited support)

***

## 21. Example

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

## 22. Summary

The PyDBML type system:

* is runtime-based
* ensures type correctness during execution
* supports extensibility
* enforces safe operations
