# Execution Model

## 1. Overview

PyDBML is executed using a runtime evaluator that processes an Abstract Syntax Tree (AST).

Execution consists of:

1. Parsing source code into AST
2. Evaluating AST nodes recursively
3. Managing runtime state through an environment

---

## 2. Execution Pipeline

A PyDBML program is executed as follows:

```

source code
↓
parser
↓
abstract syntax tree (AST)
↓
evaluator
↓
runtime values

```

---

## 3. Evaluation Strategy

### 3.1 Node-Based Evaluation

Each AST node is evaluated independently.

```

evaluate(node) → value

```

Evaluation is:

- recursive
- depth-first
- single-threaded

---

### 3.2 Statement Execution

Statements are executed sequentially:

```

statement1
statement2
statement3

```

Execution order is strictly top-to-bottom.

---

## 4. Runtime Environment

### 4.1 Structure

The environment consists of:

- local scope (stack)
- global scope (map)
- function registry
- object definitions

---

### 4.2 Variable Storage

Variables are stored as:

```

name → runtime value

```

Local variables are stored in a stack of scopes.

---

### 4.3 Scope Resolution

Variable lookup follows:

```

1. current local scope
2. parent local scopes
3. global scope
4. error if not found

```

---

## 5. Expression Evaluation

### 5.1 Evaluation Order

Expressions are evaluated left-to-right.

```

!x = 5 + 3 \* 2

```

is evaluated according to operator precedence rules.

---

### 5.2 Short-Circuit Evaluation

Logical expressions:

```

AND
OR

```

are evaluated lazily.

#### Example:

```

false AND expr → expr not evaluated
true OR expr → expr not evaluated

```

---

## 6. Assignment Semantics

```

!x = expression

```

Steps:

1. Evaluate expression
2. Store result in environment
3. Return assigned value

---

## 7. Control Flow Semantics

---

### 7.1 IF Execution

```

if (cond) then ... elseif ... else ...

```

Execution steps:

1. Evaluate first condition
2. If true → execute block → exit
3. Else evaluate next condition
4. Continue until a true condition is found
5. If none match → execute else (if present)

---

### 7.2 Loop Execution

---

#### Range Loop

```

do !i from a to b

```

Execution:

1. Evaluate a, b
2. Initialize counter i = a
3. Loop until termination condition
4. Increment per iteration

---

#### Values Loop

```

do !v values !arr

```

Execution:

- Iterate over values of array
- Assign each value to !v

---

#### Indices Loop

```

do !i indices !arr

```

Execution:

- Iterate over indices of array
- Assign index to !i

---

#### Infinite Loop

```

do
...
enddo

```

Executes indefinitely until terminated.

---

### 7.3 Loop Control

---

#### Break

```

break

```

Effect:

- Immediately exits loop

Implemented via control signal.

---

#### Skip

```

skipif(condition)

```

Effect:

- Skips current iteration if condition true

---

## 8. Function Execution

---

### 8.1 Function Call

```

!!func(a, b)

```

Execution steps:

1. Evaluate arguments
2. Create new scope
3. Bind parameters to arguments
4. Execute function body
5. Return value

---

### 8.2 Scope Behavior

Each function call creates a new local scope.

```

call → push scope
return → pop scope

```

---

### 8.3 Return Semantics

```

return value

```

Execution:

- Stops function execution immediately
- Returns value to caller
- Implemented via control signal

---

## 9. Object Execution

---

### 9.1 Object Creation

```

object type(args)

```

Execution:

1. Resolve type
2. Create instance
3. Execute constructor if defined

---

### 9.2 Method Call

```

!obj.method(...)

```

Execution:

1. Evaluate object
2. Resolve method
3. Bind `this`
4. Execute method body
5. Return result

---

## 10. Error Handling Semantics

---

### 10.1 Error Propagation

Errors propagate upward unless handled.

---

### 10.2 Handle Block

```

HANDLE (...) ... ELSEHANDLE ...

```

Execution:

1. Execute try block
2. If error occurs → match handler
3. Execute matching handler
4. Stop propagation

---

## 11. Control Signals

Certain control flows are implemented as signals:

| Signal | Purpose |
|--------|--------|
| ReturnSignal | function return |
| BreakSignal | loop exit |
| ContinueSignal | skip iteration |
| GoLabelSignal | jump execution |

Signals interrupt normal execution.

---

## 12. Evaluation Guarantees

The execution model guarantees:

- deterministic execution order
- consistent variable resolution
- strict scope boundaries
- predictable control flow

---

## 13. Non-Goals

The execution model does not support:

- concurrency
- parallel execution
- compile-time evaluation

---

## 14. Example Execution

```

!x = 5
!y = 10
!z = !x + !y

```

Execution:

1. Evaluate 5 → assign to x
2. Evaluate 10 → assign to y
3. Evaluate x + y → 15
4. Assign 15 → z
