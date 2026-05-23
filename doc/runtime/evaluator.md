
# Evaluator Specification

## 1. Overview

The evaluator is the core execution engine of PyDBML.

It processes AST nodes and produces runtime values.

---

## 2. Evaluation Entry Point

```

evaluate(node)

```

### Behavior

- Receives AST node
- Dispatches based on node type
- Returns evaluated result

---

## 3. Dispatch Mechanism

Evaluator uses:

```

node\_type → handler function

```

Example:

```

AssignNode → \_eval\_assign
CallNode → \_eval\_method\_call
ObjectNode → \_eval\_object

```

---

## 4. Execution Flow

1. Receive AST node
2. Identify node type
3. Call handler
4. Evaluate children recursively
5. Return value

---

## 5. Call Stack

Evaluator maintains:

```

call\_stack → list of nodes

```

Used for:

- debugging
- error reporting

---

## 6. Control Signals

Evaluator must propagate:

- ReturnSignal
- BreakSignal
- ContinueSignal
- GoLabelSignal

### Rule

```

DO NOT catch control signals

```

---

## 7. Error Handling

Evaluator wraps unexpected errors:

```

Python error → PyDBMLError

```

---

## 8. Method Dispatch

Method calls follow:

```

1. builtins
2. DSL object methods
3. plugin methods
4. Python methods (fallback)

```

---

## 9. PluginObject Handling

If value is:

```

PluginObject → unwrap before method call

```

---

## 10. Type Conversion

Evaluator converts:

- PyDBML → Python (before call)
- Python → PyDBML (after call)

---

## 11. Method Cache

```

class → method\_map

```

Improves repeated lookup performance.

---

## 12. Guarantees

Evaluator ensures:

- deterministic execution
- safe propagation
- consistent method resolution