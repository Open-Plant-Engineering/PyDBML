# Object System Specification

## 1. Overview

PyDBML provides an object system that supports:

- Object creation
- Attribute access
- Attribute assignment
- Method invocation
- Plugin-backed objects
- User-defined objects

Objects are runtime entities represented internally as instances.

---

## 2. Object Types

PyDBML distinguishes between:

### 2.1 Built-in Objects

Objects implemented using Python classes, such as:

- Real
- String
- Array

---

### 2.2 Plugin Objects

Objects created through Python plugins:

```python
@pydbml_class
class Custom:
````

***

### 2.3 User-Defined Objects

Objects defined within PyDBML code via AST definitions.

***

## 3. Object Creation

### 3.1 Syntax

```
!obj = object type_name(args)
```

***

### 3.2 Semantics

Object creation proceeds as follows:

1. Evaluate all argument expressions
2. Resolve object type
3. Create instance
4. Invoke constructor (if defined)

***

### 3.3 Type Resolution

Resolution order:

```
1. Plugin classes
2. Built-in types
3. User-defined object definitions
4. External file loader
```

If type is not found → error.

***

## 4. Object Structure

An object consists of:

```
ObjectInstance:
    - definition (metadata)
    - value (attribute storage)
```

***

### 4.1 Attribute Storage

Attributes are stored as:

```
attribute_name → value
```

***

### 4.2 Method Storage

Methods are associated with the object definition:

```
method_name → method implementation
```

***

## 5. Attribute Access

### 5.1 Syntax

```
!x = !obj.attribute
```

***

### 5.2 Execution

1. Evaluate object
2. Lookup attribute
3. Return value

***

### 5.3 Resolution Rules

For object instances:

```
1. Object attribute map
2. Object methods (callable)
3. Error if not found
```

***

### 5.4 Plugin Objects

For plugin objects:

* Attributes resolved via Python `getattr`
* Case-insensitive matching may apply

***

## 6. Attribute Assignment

### 6.1 Syntax

```
!obj.attribute = value
```

***

### 6.2 Execution

1. Evaluate object
2. Evaluate value
3. Validate attribute exists (if typed object)
4. Assign value

***

### 6.3 Type Enforcement

If object has declared attribute types:

```
value must match expected type
```

Else → TYPE\_ERROR

***

## 7. Method Calls

### 7.1 Syntax

```
!result = !obj.method(arg1, arg2)
```

***

### 7.2 Execution

1. Evaluate object
2. Resolve method name
3. Evaluate arguments
4. Bind method context (`this`)
5. Execute method
6. Return result

***

## 8. Method Resolution

### 8.1 Resolution Order

For a method call:

```
1. User-defined object methods
2. Plugin methods
3. Built-in type methods
4. Error if not found
```

***

### 8.2 Case Handling

Method names are typically:

```
normalized to lowercase
compared using uppercase mapping internally
```

***

## 9. Binding Context (`this`)

During method execution:

```
this → current object instance
```

Accessible within method body.

***

## 10. Constructor Execution

### 10.1 Constructor Rule

If an object defines a method with the same name:

```
type_name(...)
```

Then this method acts as constructor.

***

### 10.2 Execution

1. Match constructor signature
2. Bind arguments
3. Execute method
4. Initialize object state

***

### 10.3 Error Case

If arguments do not match constructor:

```
CONSTRUCTOR_ERROR
```

***

## 11. Plugin Object System

### 11.1 Definition

Plugin classes are registered via:

```python
@pydbml_class
class ClassName:
```

***

### 11.2 Methods

Defined using:

```python
@pydbml_method("NAME")
def method(self, args):
```

***

### 11.3 Operators

Defined using:

```python
@pydbml_operator("+")
```

***

### 11.4 Execution

Plugin methods:

1. Bound to instance
2. Called with Python arguments
3. Result converted back to PyDBML type

***

## 12. Method Cache

### 12.1 Purpose

Method cache improves performance.

```
class → method_map
```

***

### 12.2 Behavior

* Built once per class
* Stored in evaluator
* Reused across calls

***

## 13. Object Lifecycle

***

### 13.1 Creation

```
object → instance created
```

***

### 13.2 Usage

```
methods + attributes accessed
```

***

### 13.3 Destruction

Objects are managed by runtime memory (Python GC).

***

## 14. Error Conditions

| Error              | Description              |
| ------------------ | ------------------------ |
| ATTRIBUTE\_ERROR   | attribute does not exist |
| METHOD\_NOT\_FOUND | method not found         |
| TYPE\_ERROR        | invalid assignment       |
| CONSTRUCTOR\_ERROR | invalid constructor      |

***

## 15. Example

```
!obj = object sample()

!obj.value = 10

!x = !obj.value
```

***

## 16. Method Example

```
!x = !num.add(5)
```

Execution:

1. Resolve num
2. Resolve method add
3. Call method
4. Return result

***

## 17. Guarantees

The object system guarantees:

* consistent method resolution
* strict attribute handling
* predictable object behavior
* runtime type validation

***

## 18. Limitations

The object system does not support:

* inheritance (current)
* polymorphism (limited)
* static typing
