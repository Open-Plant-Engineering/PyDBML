# Error System Specification

## 1. Overview

The PyDBML error system defines how runtime errors are:

- generated
- propagated
- handled
- reported

Errors are first-class execution events and may interrupt normal control flow.

---

## 2. Error Categories

Errors in PyDBML fall into two categories:

### 2.1 Runtime Errors

Errors caused by program execution:

- TYPE_ERROR
- NAME_ERROR
- OPERATOR_ERROR
- ARG_COUNT
- RETURN_TYPE
- INDEX_ERROR
- ATTRIBUTE_ERROR
- METHOD_NOT_FOUND
- CONSTRUCTOR_ERROR

---

### 2.2 Internal Errors

Errors not caused by program logic:

- INTERNAL

These represent interpreter failures or unexpected conditions.

---

## 3. Error Representation

Each error is represented as an object:

```

PyDBMLError:
code1     → primary error code
code2     → secondary error code (optional)
message   → descriptive text
node      → AST node (optional)
stack     → execution stack trace

```

---

## 4. Error Generation

Errors may be generated in several ways:

---

### 4.1 Explicit Error Raising

```

raise\_error(code, message, node)

```

---

### 4.2 Implicit Runtime Errors

Generated automatically:

```

!x + "abc" → TYPE\_ERROR

```

---

### 4.3 Variable Resolution Error

```

!x not defined → NAME\_ERROR

```

---

### 4.4 Invalid Operation

```

invalid operator → OPERATOR\_ERROR

```

---

## 5. Error Propagation

### 5.1 Default Behavior

Errors propagate upward through the call stack:

```

current execution → caller → caller → ...

```

If not handled, execution terminates.

---

### 5.2 Stack Trace

Each error captures the execution stack:

```

node1 → node2 → node3

```

Used for debugging and diagnostics.

---

## 6. Error Handling

---

### 6.1 Handle Block Syntax

```

HANDLE (code1, code2)
block
ELSEHANDLE condition
block
ENDHANDLE

```

---

### 6.2 Execution Model

1. Execute try block
2. If error occurs:
   - Match against handlers
   - Execute matching block
3. Stop error propagation

---

### 6.3 Matching Rules

Handlers match errors using:

#### Exact Match

```

(code1, code2)

```

#### Wildcard Match

```

ANY

```

---

### 6.4 Matching Priority

Order of evaluation:

```

1. Specific match (code1, code2)
2. ANY handler
3. Propagate if no match

```

---

## 7. Error Handling Example

```

HANDLE (TYPE\_ERROR, \*)
return 0
ELSEHANDLE ANY
return -1
ENDHANDLE

```

---

## 8. Control Signals vs Errors

PyDBML distinguishes between:

---

### 8.1 Control Signals

Used for flow control:

| Signal | Purpose |
|--------|--------|
| ReturnSignal | function return |
| BreakSignal  | loop break |
| ContinueSignal | loop continue |
| GoLabelSignal | jump execution |

---

### 8.2 Key Difference

```

Control signals are NOT errors

```

They:

- must not be caught by HANDLE blocks
- propagate differently

---

## 9. Error Handling Isolation

Handle blocks only catch:

```

PyDBMLError

```

They must not intercept:

```

ReturnSignal
BreakSignal
ContinueSignal

```

---

## 10. Error Wrapping

Python exceptions may be converted into PyDBML errors:

---

### 10.1 Conversion Rules

| Python Error | PyDBML Error |
|-------------|-------------|
| TypeError | TYPE_ERROR |
| KeyError | NAME_ERROR |
| ValueError | TYPE_ERROR |

---

### 10.2 Behavior

If unexpected:

```

wrap → INTERNAL error

```

---

## 11. Error in Functions

---

### 11.1 Unhandled Error

If error occurs in function:

```

error propagates to caller

```

---

### 11.2 Handled Error

If caught in HANDLE block:

```

function returns normally

```

---

## 12. Error in Loops

---

### 12.1 Behavior

If error occurs inside loop:

```

loop execution stops
error propagates

```

Unless caught explicitly.

---

## 13. Error in Object Methods

---

### 13.1 Behavior

Errors inside method:

```

propagate to caller

```

Unless handled within method body.

---

## 14. Evaluation Safety

### 14.1 Guarantees

The engine ensures:

- errors do not corrupt environment state
- scope cleanup occurs correctly
- control signals remain intact

---

## 15. Debugging Support

Errors contain:

- source location (line, column)
- AST node reference
- execution stack

This enables:

- precise diagnostics
- debugging tools

---

## 16. Fatal Errors

If error reaches top-level:

```

execution terminates
error is reported

```

---

## 17. Example

```

!x = "abc"
!y = 5

!z = !x + !y

```

Result:

```

TYPE\_ERROR

```

---

## 18. Edge Cases

---

### Division by Zero

```

1 / 0 → TYPE\_ERROR or runtime error

```

---

### Invalid Index

```

!arr\["abc"] → INDEX\_ERROR

```

---

### Missing Method

```

!x.unknown() → METHOD\_NOT\_FOUND

```

---

## 19. Design Guarantees

The error system guarantees:

- deterministic behavior
- predictable propagation
- safe execution boundaries
- precise error reporting

---

## 20. Limitations

The error system does not include:

- compile-time errors
- warnings
- static type enforcement
