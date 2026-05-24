
# Statements

## 1. Definition

Statements define executable instructions in a PyDBML program.

A program consists of a sequence of statements executed in order.

---

## 2. Assignment

```

!x = expression

```

### Behavior

- Evaluates the expression
- Stores the result in the variable
- Returns the assigned value

---

## 3. Print

```

$P expression

```

### Behavior

- Evaluates the expression
- Outputs the result to console or standard output

---

## 4. Import Statement

```

import |path|
import module module\_name

```

### Behavior

- File import (`|path|`) loads PyDBML plugins or scripts
- Module import loads Python modules into the runtime
- Imported elements become available for use in expressions and statements

---

## 5. Return Statement

```

return expression

```

### Behavior

- Evaluates the expression
- Immediately terminates the current function
- Returns the value to the caller
- Implemented using `ReturnSignal`

---

## 6. Break Statement

```

break

```

### Behavior

- Immediately exits the nearest enclosing loop
- Implemented using `BreakSignal`

---

## 7. Skip Statement

```

skipif (condition)

```

### Behavior

- Evaluates condition
- If true → skips remaining statements in current loop iteration
- Moves to next iteration
- Implemented using `ContinueSignal`

---

## 8. Expression Statement

```

expression

```

### Behavior

- Evaluates the expression
- Discards the result unless explicitly assigned

### Common Use Cases

- Method calls:

```

!f.write('Hello')

```

- Object creation:

```

object open('file.txt', 'w')

```

---

## 9. Flow Control Statements

Complex control flow constructs are defined in separate sections:

- IF statement
- DO loop

---

## 10. Execution Order

Statements are executed sequentially:

```

statement1
statement2
statement3

```

### Guarantees

- Strict top-to-bottom execution
- No implicit reordering
- Deterministic behavior

---

## 11. Interaction with Runtime

Statements interact with the runtime environment:

- Assignment → updates variables
- Function calls → create new scopes
- Object creation → instantiates runtime objects
- Method calls → execute dynamic behavior (including Python methods)

---

## 12. Error Behavior

- Errors during statement execution:
  - interrupt execution
  - propagate upward
- Can be handled via `HANDLE` blocks

---

## 13. Notes

- All statements are evaluated by the runtime evaluator
- Statements may trigger control signals (`return`, `break`, `skip`)
- Expressions within statements are evaluated according to expression rules
