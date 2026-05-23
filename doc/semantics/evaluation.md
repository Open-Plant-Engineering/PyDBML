
# Evaluation Semantics

## 1. Evaluation Model

PyDBML follows a recursive evaluation model:

- Expressions are evaluated recursively (depth-first)
- Statements are executed sequentially (top-to-bottom)

### Execution Flow

```

program → statements → expressions → values

```

Each AST node:

```

evaluate(node) → value

```

---

## 2. Scope Resolution

Variables are resolved using lexical scope rules.

### Resolution Order

1. Local (current scope)
2. Enclosing scopes (if any)
3. Global scope
4. Error if not found

### Behavior

- Local variables shadow global variables
- Global variables are accessible unless overridden
- Undefined variables raise:

```

NAME\_ERROR

```

---

## 3. Expression Evaluation

Expressions are evaluated recursively.

### Example

```

!x = 5 + 3 \* 2

```

Evaluation order:

```

3 \* 2 → 6
5 + 6 → 11

```

---

## 4. Short Circuit Evaluation

Logical operators are evaluated lazily:

```

AND
OR

```

### Rules

- `A AND B` → B evaluated only if A is true
- `A OR B` → B evaluated only if A is false

This ensures:

- performance optimization
- safe evaluation (avoid unnecessary errors)

---

## 5. Function Execution

Function calls follow this model:

### Steps

1. Create new local scope
2. Bind parameters to arguments
3. Execute function body
4. Return value via `ReturnNode`
5. Destroy local scope

### Behavior

- Functions isolate variable scope
- Return exits execution immediately using `ReturnSignal`

---

## 6. Object Creation Semantics

Objects are created via:

```

object type\_name(...)

```

### Resolution Order

1. Python functions (treated as constructors)
2. Plugin classes
3. PyDBML object definitions
4. File-loaded objects

### Behavior

- Arguments are evaluated before invocation
- Arguments are converted between PyDBML and Python types
- Returned objects may be:
  - ObjectInstance (PyDBML)
  - PluginObject (Python)

---

## 7. Method Call Semantics

Method calls use:

```

target.method(args)

```

### Evaluation Steps

1. Evaluate target
2. Evaluate arguments
3. Resolve method
4. Execute method

---

### Method Resolution Order

1. Built-in methods
2. PyDBML object methods
3. Plugin/extension methods
4. Native Python methods

---

### Case Insensitivity

Method names are case-insensitive:

```

write, WRITE, WrItE → same method

```

---

### Python Method Execution

If method is not found in PyDBML layers:

- Evaluate using Python reflection
- Use case-insensitive lookup fallback
- Invoke method dynamically

---

## 8. Native Python Integration

PyDBML supports direct execution of Python constructs.

### Features

- Import Python modules
- Call Python functions
- Instantiate Python objects
- Invoke Python methods

### Example

```

import module builtins

!f = object open('file.txt', 'w')
!f.write('Hello')
!f.close()

```

---

### Execution Flow

```

ObjectNode(open) → Python function call
CallNode(write) → Python method invocation

```

---

## 9. Type Conversion

The evaluator performs automatic type conversion.

### PyDBML → Python

| PyDBML Type | Python Type |
|------------|------------|
| Real        | int/float  |
| String      | str        |
| Boolean     | bool       |
| Array       | list       |

### Python → PyDBML

- Primitive → converted to PyDBML type
- Object → wrapped as `PluginObject`

---

## 10. Control Flow Signals

Evaluation uses control signals for flow:

| Signal | Purpose |
|--------|--------|
| ReturnSignal | function return |
| BreakSignal  | loop exit |
| ContinueSignal | loop continuation |
| GoLabelSignal | jump execution |

### Behavior

- Signals interrupt evaluation immediately
- Signals propagate upward until handled

---

## 11. Error Propagation

Errors during evaluation:

1. Immediately interrupt evaluation
2. Propagate upward through call stack
3. Can be intercepted via `HANDLE`

---

## 12. Execution Order Guarantees

PyDBML guarantees:

- left-to-right evaluation of expressions
- deterministic execution order
- no implicit reordering

---

## 13. Evaluation Safety

The evaluator ensures:

- consistent type handling
- safe execution boundaries
- correct scope cleanup
- safe Python method invocation

---

## 14. Example Execution

Program:

```

import module builtins

!f = object open('file.txt', 'w')
!f.write('Hello')
!f.close()

```

Execution:

1. Import module → register functions/classes
2. Evaluate `open(...)` → Python function call
3. Return file object → wrapped
4. Resolve `write` → native Python method
5. Execute → returns result
6. Resolve `close` → native method
7. Execute → close file

---

## 15. Design Guarantees

The evaluation model guarantees:

- deterministic execution
- consistent method resolution
- seamless Python interoperability
- predictable control flow

---

## 16. Limitations

- No compile-time evaluation
- Limited optimization
- Python execution is not sandboxed
