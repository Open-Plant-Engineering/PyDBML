# Object System Specification

## 1. Overview

PyDBML provides an object system that supports:

- Object creation
- Attribute access
- Attribute assignment
- Method invocation
- Plugin-backed objects
- Python object integration
- User-defined objects

Objects are runtime entities represented internally as instances.

---

## 2. Object Types

PyDBML distinguishes between:

---

### 2.1 Built-in Objects

Objects implemented as core runtime types:

- Real
- String
- Array
- Boolean

---

### 2.2 Plugin Objects

Objects created from Python runtime:

```

PluginObject(obj)

````

### Sources

- Python functions (e.g., `open`)
- Python classes
- External libraries

---

### 2.3 Plugin Classes

Objects created via Python integration:

```python
@pydbml_class
class Custom:
````

***

### 2.4 User-Defined Objects

Objects defined within PyDBML code via object definitions.

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
3. Execute constructor logic:
   * Python function call OR
   * Python class instantiation OR
   * PyDBML object creation
4. Wrap result if needed

***

### 3.3 Type Resolution

Resolution order (final runtime behavior ✅):

```
1. Python functions (e.g., open)
2. Plugin classes
3. Built-in types
4. User-defined object definitions
5. File-loaded objects
```

If not found → error

***

### 3.4 Python Object Creation

If type resolves to a Python function:

```
object open(...)
```

Execution:

```
call Python function → return object → wrap as PluginObject
```

***

## 4. Object Structure

***

### 4.1 ObjectInstance

```
ObjectInstance:
    - definition (metadata)
    - attributes (values)
```

***

### 4.2 Attribute Storage

```
attribute_name → value
```

***

### 4.3 Method Storage

```
method_name → method implementation
```

***

### 4.4 PluginObject Structure

```
PluginObject:
    - obj (underlying Python object)
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
2. Resolve attribute
3. Return value

***

### 5.3 Resolution Rules

For ObjectInstance:

```
1. Attribute map
2. Methods (callable)
3. Error if not found
```

***

### 5.4 PluginObject Access

For Python-backed objects:

```
1. getattr(target, attribute)
2. Case-insensitive fallback
```

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
3. Assign to attribute

***

### 6.3 Type Enforcement

If object defines typed attributes:

```
value must match expected type
```

Else:

```
TYPE_ERROR
```

***

## 7. Method Calls

### 7.1 Syntax

```
!result = !obj.method(arg1, arg2)
```

***

### 7.2 Execution

1. Evaluate target object
2. Evaluate arguments
3. Unwrap PluginObject if needed
4. Resolve method
5. Execute method
6. Convert result to PyDBML type

***

## 8. Method Resolution

### 8.1 Resolution Order (FINAL ✅)

```
1. Built-in methods
2. User-defined object methods
3. Plugin/extension methods
4. Native Python methods (fallback)
```

***

### 8.2 Native Python Method Fallback

If method not found:

1. Check exact match:

```
getattr(target, method_name)
```

2. If not found:

```
search dir(target) for case-insensitive match
```

3. If found → execute

Else:

```
METHOD_NOT_FOUND
```

***

### 8.3 Case Handling

Method names are:

```
case-insensitive
```

Examples:

```
write
WRITE
WrItE
```

All resolve to same method.

***

## 9. Binding Context (`this`)

For ObjectInstance:

```
this → current object
```

Used inside method definitions.

***

For PluginObject:

* Python object itself acts as context

***

## 10. Constructor Execution

### 10.1 Rule

For PyDBML object:

```
method named type_name → constructor
```

***

### 10.2 Execution

1. Match method
2. Bind parameters
3. Execute method
4. Initialize attributes

***

### 10.3 Error Case

```
CONSTRUCTOR_ERROR
```

***

## 11. Plugin Object System

***

### 11.1 Class Registration

```python
@pydbml_class
class ClassName:
```

***

### 11.2 Method Definition

```python
@pydbml_method("NAME")
def method(self, args):
```

***

### 11.3 Operator Support

```python
@pydbml_operator("+")
```

***

### 11.4 Execution

1. Method resolved
2. Bound to instance
3. Arguments converted to Python
4. Method executed
5. Result converted back

***

## 12. Method Cache

### 12.1 Structure

```
class → method_map
```

***

### 12.2 Behavior

* Built once per class
* Stored in evaluator
* Improves lookup performance

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
attributes + methods accessed
```

***

### 13.3 Destruction

* Managed by Python garbage collector

***

## 14. Error Conditions

| Error              | Description          |
| ------------------ | -------------------- |
| ATTRIBUTE\_ERROR   | attribute not found  |
| METHOD\_NOT\_FOUND | method not resolved  |
| TYPE\_ERROR        | invalid assignment   |
| CONSTRUCTOR\_ERROR | constructor mismatch |

***

## 15. Examples

***

### 15.1 Basic Object

```
!obj = object sample()
!obj.value = 10
!x = !obj.value
```

***

### 15.2 Python Object

```
import module builtins

!f = object open('file.txt', 'w')
!f.write('Hello')
!f.close()
```

***

### 15.3 Case-Insensitive Method

```
!f.WRITE('Hello')
!f.Close()
```

***

## 16. Guarantees

The object system guarantees:

* consistent method resolution
* case-insensitive access
* seamless Python integration
* predictable runtime behavior
* efficient method lookup

***

## 17. Limitations

The object system does not support:

* inheritance (currently)
* advanced polymorphism
* static typing of all objects
* restricted Python sandboxing

