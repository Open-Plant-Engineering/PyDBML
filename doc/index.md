
# PyDBML Language Reference

## 1. Introduction

PyDBML is a domain-specific programming language designed for structured data processing, procedural logic, and extensible runtime execution.

It provides a clean syntax combined with a powerful execution engine capable of integrating with external systems and Python runtime components.

This document defines the syntax, semantics, and execution behavior of the PyDBML language.

This specification is authoritative.

---

## 2. Design Goals

PyDBML is designed with the following goals:

- Simplicity of syntax
- Strong runtime evaluation
- Structured control flow
- Extensibility via plugins
- Deterministic execution behavior
- Seamless integration with Python runtime

---

## 3. Language Characteristics

PyDBML is:

- Interpreted
- Dynamically typed
- Expression-oriented
- Statement-driven
- Case-insensitive for identifiers and method calls

---

## 4. Program Structure

A program consists of a sequence of statements evaluated in order:

```

statement
statement
statement

```

Execution starts from the first statement and proceeds sequentially.

---

## 5. Imports

PyDBML supports two types of imports:

### 5.1 File / Plugin Import

Used to load PyDBML plugins or files.

```

import |path/to/file|

```

### 5.2 Python Module Import

Used to import native Python modules.

```

import module module\_name

```

#### Example

```

import module builtins

```

### Behavior

- All functions and classes from the module are registered
- They become available for object creation and function calls
- Module names are case-insensitive

---

## 6. Object Creation

Objects are created using the `object` keyword:

```

!x = object type\_name(...)

```

### Supported Sources

PyDBML supports object creation from:

- Built-in types
- User-defined objects
- Plugin classes
- Python classes
- Python functions (treated as constructors)

### Example

```

import module builtins

!f = object open('file.txt', 'w')

```

### Behavior

- If `type_name` refers to a Python function, it is invoked
- If it refers to a Python class, an instance is created
- Arguments are automatically converted between PyDBML and Python types

---

## 7. Method Calls

Methods are invoked using dot notation:

```

!x.method\_name(args)

```

### Case Insensitivity

Method calls are case-insensitive:

```

!f.write()
!f.WRITE()
!f.WrItE()

```

All are equivalent.

### Resolution Order

When calling a method, PyDBML resolves it in the following order:

1. Built-in methods
2. PyDBML object methods
3. Plugin / extension methods
4. Native Python methods

### Python Method Support

If a method is not found in PyDBML:

- PyDBML attempts to call the corresponding Python method
- Matching is performed case-insensitively

### Example

```

import module builtins

!f = object open('file.txt', 'w')
!f.WRITE('Hello')
!f.Close()

```

---

## 8. Python Interoperability

PyDBML provides seamless interoperability with Python.

### Features

- Import Python modules
- Call Python functions
- Instantiate Python classes
- Invoke Python object methods

### Example

```

import module builtins

!f = object open('file.txt', 'w')
!f.write('Hello World')
!f.close()

```

### Type Conversion

PyDBML automatically converts values:

| PyDBML Type | Python Type |
|------------|------------|
| Real        | float/int  |
| String      | str        |
| Boolean     | bool       |
| Array       | list       |

Return values from Python are converted back into PyDBML types.

---

## 9. Documentation Structure

This specification is divided into:

- Syntax definition (`syntax/`)
- Semantic rules (`semantics/`)
- Type system (`types/`)
- Runtime system (`runtime/`)
- Examples (`examples/`)

Each section defines behavior formally.

---