
# Expressions

## 1. Definition

An expression produces a value.

Expressions are the fundamental building blocks of computation in PyDBML.

Expressions may consist of:

- Literals
- Variables
- Arithmetic and logical operations
- Function calls
- Method calls
- Object creation
- Attribute and index access

---

## 2. Literals

### 2.1 Number

```

5
10.5

```

Represents numeric values.

---

### 2.2 String

```

|hello|
'world'

```

Represents string values.

---

### 2.3 Boolean

```

true
false

```

Represents logical truth values.

---

## 3. Variables

Variables are referenced using:

```

!x         → local variable
!!global   → global variable

```

### Behavior

- Variables evaluate to their stored runtime value
- Undefined variables raise:

```

NAME\_ERROR

```

---

## 4. Arithmetic Operators

| Operator | Description |
|----------|------------|
| +        | addition |
| -        | subtraction |
| *        | multiplication |
| /        | division |

---

### Example

```

!x = 5 + 3 \* 2

```

Result:

```

11

```

---

## 5. Comparison Operators

```

\==   !=   >   <   >=   <=

```

### Behavior

- Compare two expressions
- Return Boolean result

---

## 6. Logical Operators

```

AND
OR
NOT

```

### Behavior

- Operate on Boolean expressions
- Follow short-circuit evaluation rules

---

## 7. Function Expression

Functions can be used inside expressions:

```

iftrue(condition, value1, value2)

```

### Behavior

- If condition is true → returns `value1`
- Else → returns `value2`

---

## 8. Object Creation Expression

Objects can be created as expressions:

```

object type\_name(args)

```

### Example

```

import module builtins

!f = object open('file.txt', 'w')

```

### Behavior

- Returns an object instance
- Can return:
  - PyDBML object
  - Python object (wrapped internally)

---

## 9. Method Call Expression

Method calls are expressions and return values:

```

!obj.method(args)

```

### Example

```

!f.write('Hello')

```

---

### Behavior

- Target is evaluated first
- Arguments are evaluated next
- Method is resolved and executed
- Result is returned as expression value

---

### Case Insensitivity

Method names are case-insensitive:

```

!f.write()
!f.WRITE()
!f.WrItE()

```

All are equivalent.

---

## 10. Attribute Access Expression

```

!obj.attribute

```

### Behavior

- Retrieves attribute value
- Works for:
  - PyDBML objects
  - Python objects

---

## 11. Index Access Expression

```

!arr\[index]

```

### Behavior

- Evaluates array and index
- Returns element at index

---

## 12. Evaluation Order

Expressions are evaluated according to operator precedence:

1. NOT
2. * / 
3. + -  
4. Comparisons  
5. AND  
6. OR  

---

### Parentheses

Parentheses override precedence:

```

(5 + 3) \* 2 → 16

```

---

## 13. Evaluation Strategy

- Expressions are evaluated recursively (depth-first)
- Left operand is evaluated before right operand
- Function and method arguments are evaluated before invocation

---

## 14. Python Integration in Expressions

Expressions may directly invoke Python functionality:

### Example

```

import module builtins

!f = object open('file.txt', 'w')
!f.write('Hello')

```

### Behavior

- Python functions can be called via `object` keyword
- Python methods are resolved at runtime
- Results are automatically converted to PyDBML values

---

## 15. Type Conversion

Expressions automatically convert between types:

### PyDBML → Python

| PyDBML Type | Python Type |
|------------|------------|
| Real        | int/float |
| String      | str |
| Boolean     | bool |

### Python → PyDBML

- Primitive values → converted
- Objects → wrapped internally

---

## 16. Error Behavior

Expression evaluation may raise errors:

| Scenario | Error |
|--------|------|
| Invalid operation | TYPE_ERROR |
| Division by zero | TYPE_ERROR |
| Undefined variable | NAME_ERROR |
| Invalid method | METHOD_NOT_FOUND |

---

## 17. Examples

### Arithmetic

```

5 + 3 \* 2 → 11

```

### Logical

```

true AND false → false

```

### Function

```

iftrue(5 > 3, 1, 0) → 1

```

### Object + Method

```

import module builtins

!f = object open('file.txt', 'w')
!f.write('Hello')

```

---

## 18. Guarantees

Expressions guarantee:

- deterministic evaluation
- predictable operator precedence
- consistent method resolution
- seamless integration with Python runtime

---

## 19. Limitations

- No compile-time evaluation
- No constant folding optimization (runtime only)
- No static type checking
