
# Expressions

## 1. Definition

An expression produces a value.

Expressions may consist of:

- Literals
- Variables
- Operations
- Function calls

---

## 2. Literals

### 2.1 Number

```
5
10.5
```

### 2.2 String

```
|hello|
'world'
```

### 2.3 Boolean

```
true
false
```

---

## 3. Variables

Variables are referenced using:

```
!x
!!global
```

---

## 4. Arithmetic Operators

| Operator | Description |
|----------|------------|
| +        | addition   |
| -        | subtraction|
| *        | multiplication |
| /        | division   |

---

## 5. Comparison Operators

```
==   !=   >   <   >=   <=
```

All return Boolean.

---

## 6. Logical Operators

```
AND
OR
NOT
```

---

## 7. Function Expression

```
iftrue(condition, value1, value2)
```

If condition is true → returns value1  
Else → returns value2  

---

## 8. Evaluation Order

Expressions are evaluated according to operator precedence:

1. NOT
2. * /
3. + -
4. Comparisons
5. AND
6. OR