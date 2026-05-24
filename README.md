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

## 🛠️ Roadmap

* [ ] Full dictionary support
* [ ] Method chaining (`obj.method().another()`)
* [ ] Improved standard library
* [ ] Sandbox execution mode
* [ ] Performance optimizations

***

## 🤝 Contributing

Contributions are welcome!

See:

```
docs/advanced/contributing.md
```

***

## 📜 License

Add your license here (MIT recommended).

***

## 👨‍💻 Author

Developed by Shivang Kheradiya
