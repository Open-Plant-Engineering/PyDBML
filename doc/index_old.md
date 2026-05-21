# PyDBML Language Reference

## 1. Introduction

PyDBML is a domain-specific programming language designed for structured data processing and procedural evaluation.

This document defines the syntax, semantics, and execution model of the language.

This documentation serves as the authoritative specification for PyDBML behavior.

---

## 2. Language Overview

PyDBML is:

- Interpreted
- Dynamically typed
- Expression-based
- Statement-driven
- Extensible via plugin system

Execution occurs in a runtime environment using an abstract syntax tree (AST) evaluator.

---

## 3. Program Structure

A PyDBML program consists of a sequence of statements:

```

statement
statement
statement

```

Statements are executed in order.

---

## 4. Variable System

### 4.1 Local Variables

Local variables are defined using the `!` prefix.

```

!x = 10

```

### 4.2 Global Variables

Global variables use the `!!` prefix:

```

!!g = 20

```

### 4.3 Variable Scope Rules

1. Local scope is searched first
2. Global scope is searched next
3. An undefined variable raises a NAME_ERROR

---

## 5. Expressions

An expression produces a value.

Examples:

```

!x = 5
!y = !x + 2

```

---

### 5.1 Arithmetic Operators

| Operator | Description |
|--------|-------------|
| + | addition |
| - | subtraction |
| * | multiplication |
| / | division |

---

### 5.2 Comparison Operators

```
==  !=  >  <  >=  <=
```

All comparisons return Boolean.

---

### 5.3 Logical Operators

```
AND
OR
NOT
```

Operands must be Boolean.

---

## 6. Control Flow

### 6.1 IF Statement

#### Syntax

```
if (condition) then
    block
elseif (condition) then
    block
else
    block
endif
```

---

#### Semantics

- Conditions are evaluated in order
- First true condition executes its block
- If no condition matches, `else` executes
- Conditions must evaluate to Boolean

---

### 6.2 DO Loop

#### Range Loop

```
do !i from start to end
    block
enddo
```

---

#### Indexed Loop

```
do !i indices !array
    block
enddo
```

---

#### Value Loop

```
do !value values !array
    block
enddo
```

---

#### Infinite Loop

```
do
    block
enddo
```

---

### 6.3 Loop Control

```

break
skipif (condition)

```

---

## 7. Functions

### 7.1 Definition

```
define function !!name(param1, param2) is type
    block
endfunction
```

---

### 7.2 Invocation

```
!x = !!name(10, 20)
```

---

### 7.3 Return

```
return expression
```

---

### 7.4 Return Semantics

- Execution stops immediately
- Value is returned
- Type must match declared return type

---

## 8. Objects

### 8.1 Creation

```
!obj = object type()
```

---

### 8.2 Member Access

```
!x = !obj.value
```

---

### 8.3 Member Assignment

```
!obj.value = 10
```

---

### 8.4 Method Call

```
!x = !obj.method(10)
```

---

## 9. Arrays

### 9.1 Assignment

```
!arr = object array()
!arr[1] = 10
```

---

### 9.2 Access

```
!x = !arr[1]
```

---

### 9.3 Index Rules

- Indices are numeric
- Invalid index raises INDEX_ERROR

---

## 10. Error Handling

### 10.1 Handle Block

```
HANDLE (code1, code2)
    block
ELSEHANDLE ANY
    block
ENDHANDLE
```

---

### 10.2 Behavior

- If error matches condition → handler executes
- Otherwise → fallback handler executes
- If no handler matches → error propagates

---

## 11. Execution Model

Execution occurs in the following stages:

1. Source code parsed into AST
2. AST evaluated recursively
3. Values stored in runtime environment

---

## 12. Runtime Environment

The runtime environment contains:

- Local variable stack
- Global variable store
- Function registry
- Object definitions

---

## 13. Type System

### Built-in Types

- Real
- String
- Boolean
- Array
- ObjectInstance

---

### Type Rules

- All operations performed at runtime
- Type mismatches raise TYPE_ERROR

---

## 14. Evaluation Rules

- Expressions evaluated left-to-right
- Logical operations are short-circuited
- Functions create new scope
- Objects maintain internal state

---

## 15. Example Program

```
!sum = 0

do !i from 1 to 5
    !sum = !sum + !i
enddo

$P !sum
```

---

## 16. Conformance

An implementation of PyDBML must:

- Follow syntax rules defined here
- Enforce runtime semantics
- Produce correct error behavior
```

---