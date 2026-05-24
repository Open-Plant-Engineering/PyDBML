# PyDBML

PyDBML is a domain-specific programming language (DSL) built on top of Python, designed for structured execution, dynamic evaluation, and seamless integration with the Python ecosystem.

It provides a clean syntax with a powerful runtime engine capable of executing logic, managing objects, and interacting with native Python modules.

---

## ✨ Features

- ✅ Simple and expressive syntax
- ✅ Dynamic runtime evaluation
- ✅ Full Python integration (`import module`)
- ✅ Object-oriented execution model
- ✅ Case-insensitive method calls
- ✅ Built-in control flow (IF, DO, HANDLE)
- ✅ Custom function definitions
- ✅ Plugin system for extensibility
- ✅ Structured error handling
- ✅ AST-based execution engine

---

## 🚀 Quick Example

```pydbml
import module builtins

!f = object open('file.txt', 'w')
!f.write('Hello from PyDBML')
!f.close()
````

✅ Directly uses Python `open()` and file methods

***

## 🧠 Language Highlights

### Variables

```
!x = 10        # local variable
!!g = 20       # global variable
```

***

### Control Flow

```pydbml
if (!x > 10) then
    $P |Greater|
else
    $P |Smaller|
endif
```

***

### Loops

```pydbml
do !i from 1 to 3
    $P !i
enddo
```

***

### Functions

```pydbml
define function !!add(!a is real, !b is real) is real
    return !a + !b
endfunction

!result = !!add(5, 3)
```

***

### Python Integration

```pydbml
import module builtins

!f = object open('file.txt', 'w')
!f.write('Hello')
!f.close()
```

***

### Case-Insensitive Methods

```pydbml
!f.WRITE('Hello')
!f.Close()
```

***

## 🧩 Architecture

PyDBML is built with a layered architecture:

```
Source Code
   ↓
Parser → AST
   ↓
Evaluator
   ↓
Runtime Environment
   ↓
Python Integration Layer
```

***

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

* Syntax and grammar
* AST structure
* Evaluation semantics
* Runtime system
* Object system
* Type system
* Error handling
* Plugin system

***

## 🧪 Testing

Run all tests:

```bash
pytest
```

Examples are included in:

```
docs/examples/
```

***

## 📚 Examples Overview

| File                                         | Category           | What it Demonstrates                  |
| -------------------------------------------- | ------------------ | ------------------------------------- |
| example1\_nested\_loops.pydbml               | Loops              | Nested loop execution                 |
| example2\_factorial.pydbml                   | Functions          | Factorial logic using loops/functions |
| example3\_if.pydbml                          | Control Flow       | IF / ELSE branching                   |
| example4\_short\_circuit.pydbml              | Logic              | Short-circuit evaluation (AND/OR)     |
| example5\_array.pydbml                       | Data Structures    | Array creation and indexing           |
| example6\_values\_loop.pydbml                | Loops              | Iterating over array values           |
| example7\_skip.pydbml                        | Loop Control       | `skipif` behavior                     |
| example8\_break.pydbml                       | Loop Control       | Loop termination using `break`        |
| example9\_method.pydbml                      | Objects            | Method invocation                     |
| example10\_handle.pydbml                     | Error Handling     | Basic HANDLE usage                    |
| example11\_scope.pydbml                      | Functions          | Variable scoping                      |
| example14\_nested\_calls.pydbml              | Functions          | Nested function calls                 |
| example15\_complex.pydbml                    | Combined           | Complex multi-feature example         |
| example16\_file\_write.pydbml                | Python Integration | File writing using Python             |
| example17\_file\_read.pydbml                 | Python Integration | File read/write cycle                 |
| example18\_json\_usage.pydbml                | Python Integration | JSON parsing                          |
| example19\_case\_insensitive\_methods.pydbml | Language Feature   | Case-insensitive method calls         |
| example20\_object\_python\_mix.pydbml        | Integration        | Mixing objects with Python            |
| example21\_method\_chaining.pydbml           | Advanced           | Sequential method usage               |
| example22\_handle\_specific\_error.pydbml    | Error Handling     | Specific error handling               |
| example23\_import\_module\_usage.pydbml      | Modules            | Importing Python modules              |

***

## 🔌 Extensibility (Plugin System)

Extend PyDBML using Python:

```python
@pydbml_class
class Custom:
    @pydbml_method("HELLO")
    def hello(self, args):
        return "Hello"
```

***

## ⚠️ Security Note

PyDBML allows direct interaction with Python modules.

This means:

* File system access is allowed
* External modules can be used

👉 Use in controlled environments if needed.

***

## 🤝 Contributing

Contributions are welcome!

See:

```
docs/advanced/contributing.md
```

***

## 👨‍💻 Author

Developed by Shivang Kheradiya
