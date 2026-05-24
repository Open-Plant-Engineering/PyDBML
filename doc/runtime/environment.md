
# Runtime Environment

## 1. Overview

The runtime environment is responsible for managing execution state during program evaluation.

It provides storage, scope management, and access to registered functions, modules, and objects.

---

## 2. Structure

The runtime environment consists of:

- Local variable stack (scoped variables)
- Global variable storage
- Function registry
- Class and object registry
- Module registry (Python modules)

---

## 3. Variable Storage

Variables are stored as:

```

name → value

```

### Value Types

Values may be:

- PyDBML primitives:
  - Real
  - String
  - Boolean
- Arrays
- ObjectInstance (PyDBML objects)
- PluginObject (wrapped Python objects)

---

## 4. Scope Stack

### Behavior

- Each function call creates a new scope
- Scope is pushed on function entry
- Scope is popped on return

```

global\_scope
└─ function\_scope
└─ nested\_scope

```

### Rules

- Variable lookup searches from innermost to outermost scope
- Assignment updates:
  - local scope (default)
  - global scope (if marked global)

---

## 5. Variable Resolution

When resolving a variable:

1. Check current scope
2. Traverse outer scopes
3. Check global scope

If not found → error

---

## 6. Function Registry

Functions are stored as:

```

name → function definition or callable

```

Supports:

- PyDBML-defined functions
- Python functions (via module import)

---

## 7. Object and Class Registry

The runtime maintains registries for:

- PyDBML object definitions
- Plugin classes
- Python classes (from module import)

These are used during:

```

ObjectNode → object creation

```

---

## 8. Module Registry

Python modules are stored as:

```

module\_name → module\_reference

```

### Behavior

- Loaded via `import module`
- Stored for reuse
- Exposes:
  - classes
  - functions

---

## 9. Python Object Integration

PyDBML integrates Python objects using a wrapper.

### PluginObject

Python objects are wrapped as:

```

PluginObject(obj)

```

### Behavior

- Acts as a bridge between PyDBML and Python
- Used for:
  - file objects
  - external libraries
  - custom Python classes

---

## 10. Method Execution

Method calls follow this resolution:

1. Built-in methods
2. PyDBML object methods
3. Plugin/extension methods
4. Native Python methods

### Case Handling

- PyDBML treats method names as case-insensitive
- Python methods are resolved using:
  - direct match
  - case-insensitive fallback

---

## 11. Type Conversion

The runtime automatically converts between PyDBML and Python types.

### PyDBML → Python

| PyDBML Type | Python Equivalent |
|------------|-------------------|
| Real        | int / float       |
| String      | str               |
| Boolean     | bool              |
| Array       | list              |

### Python → PyDBML

- Primitive values → converted to corresponding PyDBML type
- Objects → wrapped as `PluginObject`

---

## 12. Execution Flow

At runtime:

1. AST node is evaluated
2. Values are resolved from environment
3. Operations are executed
4. Results are stored or returned

---

## 13. Lifecycle of Execution

```

Program Start
↓
Initialize global environment
↓
Evaluate statements sequentially
↓
Manage scopes during function calls
↓
Return final state

```

---

## 14. Error Handling

Runtime supports:

- Raising errors
- Propagating errors
- Handling errors via `HandleNode`

---

## 15. Design Guarantees

The runtime environment ensures:

- deterministic execution
- consistent variable resolution
- safe integration with Python runtime
- extensibility via plugins and modules

---

## 16. Limitations

- No static typing enforcement
- Limited sandboxing for Python execution
- No native concurrency support
