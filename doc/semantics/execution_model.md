# Execution Model

## 1. Overview

PyDBML is executed using a runtime evaluator that processes an Abstract Syntax Tree (AST).

Execution consists of:

1. Parsing source code into AST
2. Evaluating AST nodes recursively
3. Managing runtime state through an environment
4. Interacting with Python runtime (modules, functions, objects)

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

Each AST node is evaluated independently:

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
- module registry (Python modules)
- class/function registry (Python + plugins)

---

### 4.2 Variable Storage

Variables are stored as:

```

name → runtime value

```

Values may include:

- PyDBML primitives (Real, String, Boolean)
- Array
- ObjectInstance
- PluginObject (wrapped Python objects)

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

Expressions are evaluated left-to-right with respect to operator precedence.

```

!x = 5 + 3 \* 2

```

Execution:

```

3 \* 2 → 6
5 + 6 → 11

```

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

Execution:

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

Execution:

1. Evaluate condition
2. If true → execute block → exit
3. Else evaluate next condition
4. Continue until match
5. Execute else block if provided

---

### 7.2 Loop Execution

---

#### Range Loop

```

do !i from a to b

```

Execution:

1. Evaluate a, b
2. Initialize counter
3. Execute loop body
4. Update per iteration

---

#### Values Loop

```

do !v values !arr

```

- Iterates over array values

---

#### Indices Loop

```

do !i indices !arr

```

- Iterates over array indices

---

#### Infinite Loop

```

do
...
enddo

```

Executes until interrupted.

---

### 7.3 Loop Control

#### Break

```

break

```

- Immediately exits loop

---

#### Skip

```

skipif(condition)

```

- Skips current iteration

---

## 8. Function Execution

---

### 8.1 Function Call

```

!!func(a, b)

```

Execution:

1. Evaluate arguments
2. Create new scope
3. Bind parameters
4. Execute body
5. Return value

---

### 8.2 Scope Behavior

```

call → push scope
return → pop scope

```

---

### 8.3 Return Semantics

```

return value

```

- Stops execution immediately
- Returns value using `ReturnSignal`

---

## 9. Object Execution

---

### 9.1 Object Creation

```

object type(args)

```

### Resolution Order

1. Python functions (e.g., open)
2. Plugin classes
3. PyDBML object definitions
4. File-loaded objects

### Execution

1. Resolve type
2. Evaluate arguments
3. Convert arguments to Python if needed
4. Create instance or call function
5. Wrap Python objects as `PluginObject`

---

### 9.2 Method Call

```

!obj.method(...)

```

### Execution Steps

1. Evaluate object
2. Evaluate arguments
3. Unwrap Python object if needed
4. Resolve method
5. Execute method
6. Convert result to PyDBML type

---

### Method Resolution Order

1. Built-in methods
2. PyDBML object methods
3. Plugin methods
4. Native Python methods (fallback)

---

### Case-Insensitive Behavior

Method calls are case-insensitive:

```

write, WRITE, WrItE → same method

```

---

### Native Python Method Execution

If method not found in PyDBML layers:

1. Attempt direct match (`hasattr`)
2. Attempt case-insensitive match
3. Invoke via Python reflection

---

## 10. Module Execution

### 10.1 Importing Modules

```

import module module\_name

```

Execution:

1. Load Python module
2. Register functions and classes
3. Store module in registry

---

### 10.2 Usage

```

import module builtins

!f = object open('file.txt', 'w')

```

---

## 11. Error Handling Semantics

---

### 11.1 Error Propagation

Errors propagate upward unless handled.

---

### 11.2 Handle Block

```

HANDLE (...) ... ELSEHANDLE ...

```

Execution:

1. Execute block
2. On error → match handler
3. Execute handler
4. Stop propagation

---

## 12. Control Signals

Certain control flows are implemented as signals:

| Signal | Purpose |
|--------|--------|
| ReturnSignal | function return |
| BreakSignal | loop exit |
| ContinueSignal | skip iteration |
| GoLabelSignal | jump execution |

Signals interrupt normal execution.

---

## 13. Python Integration Execution

PyDBML supports seamless Python interaction.

### Supported Operations

- Import Python modules
- Call Python functions
- Instantiate Python objects
- Invoke Python methods

### Execution Flow Example

```

ObjectNode(open)
→ Python function call

CallNode(write)
→ Python method invocation

```

---

## 14. Evaluation Guarantees

The execution model guarantees:

- deterministic execution order
- consistent variable resolution
- strict scope boundaries
- predictable control flow
- safe Python integration

---

## 15. Non-Goals

The execution model does not support:

- concurrency
- parallel execution
- compile-time evaluation

---

## 16. Example Execution

```

import module builtins

!x = 5
!y = 10
!z = !x + !y

```

Execution:

1. Import module → register runtime objects
2. Assign 5 to x
3. Assign 10 to y
4. Evaluate x + y → 15
5. Assign 15 to z
