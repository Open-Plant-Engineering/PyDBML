# Abstract Syntax Tree (AST) Specification

## 1. Overview

The PyDBML execution model is based on an Abstract Syntax Tree (AST).

The AST represents the structured form of parsed source code and serves as the input to the evaluator.

Each AST node represents a syntactic construct.

---

## 2. AST Fundamentals

### 2.1 Definition

An AST is a tree of nodes:

```

node → contains children → forms tree

```

Example program:

```

!x = 5 + 3

```

AST:

```

AssignNode
├── name: x
└── value: BinaryOpNode
├── left: NumberNode(5)
├── op: "+"
└── right: NumberNode(3)

```

---

### 2.2 Node Evaluation Contract

Each node supports:

```

evaluate(node) → value

```

Nodes must:

- evaluate children
- perform operation
- return result

---

## 3. Core AST Node Categories

---

### 3.1 Expression Nodes

| Node | Description |
|------|------------|
| NumberNode | numeric literal |
| StringNode | string literal |
| BooleanNode | boolean literal |
| VariableNode | variable reference |
| BinaryOpNode | binary operation |
| LogicalOpNode | AND / OR |
| NotNode | unary NOT |
| FunctionCallNode | function call |
| CallNode | method call |
| ObjectNode | object creation |
| IndexAccessNode | array access |
| DotAccessNode | object attribute access |

---

### 3.2 Statement Nodes

| Node | Description |
|------|------------|
| AssignNode | variable assignment |
| PrintNode | print statement |
| ReturnNode | return statement |
| BreakNode | loop break |
| SkipIfNode | conditional skip |
| DoNode | loop |
| IfNode | conditional |
| FunctionDefNode | function definition |
| MethodDefNode | method definition |
| ObjectDefNode | object definition |
| ImportNode | module or file import |

---

### 3.3 Control Nodes

| Node | Description |
|------|------------|
| BreakIfNode | conditional break |
| LabelNode | label definition |
| GoLabelNode | jump to label |
| HandleNode | error handling |

---

## 4. Node Definitions

---

### 4.1 AssignNode

```

AssignNode:
name: identifier
value: expression node
is\_global: boolean

```

Semantics:

1. Evaluate value
2. Store in environment
3. Return result

---

### 4.2 NumberNode

```

NumberNode:
value: numeric

```

Returns:

```

Real(value)

```

---

### 4.3 StringNode

```

StringNode:
value: string

```

Returns:

```

String(value)

```

---

### 4.4 VariableNode

```

VariableNode:
name: identifier
is\_global: boolean

```

Semantics:

1. Lookup variable
2. Return stored value

---

### 4.5 BinaryOpNode

```

BinaryOpNode:
left: expression
op: operator
right: expression

```

Semantics:

1. Evaluate left
2. Evaluate right
3. Apply operator
4. Return result

---

### 4.6 LogicalOpNode

```

LogicalOpNode:
left: expression
op: AND | OR
right: expression

```

Semantics:

Short-circuit evaluation.

---

### 4.7 IfNode

```

IfNode:
condition: expression
then\_branch: block
elif\_blocks: list\[(condition, block)]
else\_branch: block

```

Execution:

- Evaluate condition sequence
- Execute first matching block

---

### 4.8 DoNode

```

DoNode:
mode: range | indices | values | infinite
var: identifier
iterable / start / end / step
body: block

```

Controls loop behavior.

---

### 4.9 FunctionDefNode

```

FunctionDefNode:
name: identifier
params: list\[(name, type)]
body: block
return\_type: type

```

Registered in function registry.

---

### 4.10 FunctionCallNode

```

FunctionCallNode:
name: identifier
args: list\[expression]

```

Invokes function.

---

### 4.11 CallNode (Method Call)

```

CallNode:
target: expression
method: identifier
args: list\[expression]

```

### Semantics

1. Evaluate target
2. Resolve method using resolution order
3. Execute method

### Method Resolution Order

1. Built-in methods
2. PyDBML object methods
3. Plugin/extension methods
4. Native Python methods

### Case Insensitivity

Method names are treated case-insensitively:

```

!x.write()
!x.WRITE()
!x.WrItE()

```

All resolve to the same method.

---

### 4.12 ObjectNode

```

ObjectNode:
type\_name: identifier
args: list\[expression]

```

Creates object instance.

### Extended Behavior

Object creation supports:

- PyDBML object definitions
- Plugin classes
- Python classes
- Python functions (treated as constructors)
- Module-backed objects

---

### 4.13 ImportNode

```

ImportNode:
path: string
is\_module: boolean

```

### Semantics

- If `is_module = False`
  → load file/plugin module

- If `is_module = True`
  → import Python module

### Module Import Behavior

- Module is loaded into runtime registry
- Classes are registered for object creation
- Functions are registered for invocation

---

### 4.14 DotAccessNode

```

DotAccessNode:
target: expression
attribute: identifier

```

Returns attribute or method reference.

Supports:

- PyDBML objects
- Plugin objects
- Python objects (via reflection)

---

### 4.15 DotAssignNode

```

DotAssignNode:
target: expression
attribute: identifier
value: expression

```

Assigns object attribute.

---

### 4.16 IndexAccessNode

```

IndexAccessNode:
target: expression
index: expression

```

Retrieves array value.

---

### 4.17 IndexAssignNode

```

IndexAssignNode:
target: expression
index: expression
value: expression

```

Sets array value.

---

### 4.18 ReturnNode

```

ReturnNode:
value: expression

```

Raises ReturnSignal.

---

### 4.19 HandleNode

```

HandleNode:
try\_block: block
handlers: list\[(condition, block)]
else\_block: block

```

Handles runtime errors.

---

## 5. AST Construction

Parser converts tokens into AST nodes using:

```

recursive-descent parsing

```

Each grammar rule maps to a specific node type.

---

## 6. Evaluation Tree Traversal

Traversal is:

```

depth-first
recursive

```

Example:

```

BinaryOpNode
├ left
└ right

```

Left evaluated before right.

---

## 7. Node Interaction

Nodes interact through:

```

evaluate(child)
→ result passed to parent

```

---

## 8. Control Flow Representation

Control structures are expressed as nodes:

```

IfNode → condition + blocks
DoNode → loop control
ReturnNode → exit signal

```

---

## 9. Python Interoperability in AST

The AST supports direct interaction with Python runtime.

### Key Concepts

- Python objects are wrapped internally (e.g., `PluginObject`)
- Method calls are dispatched dynamically
- Native Python methods are invoked via fallback resolution

### Example Flow

```

ObjectNode(open)
→ Python function call
→ returns file object
→ MethodCallNode(write)
→ invokes Python method

```

---

## 10. Error Integration

Nodes may:

- raise errors
- propagate errors
- handle errors (HandleNode)

---

## 11. Optimization Potential

AST enables:

- constant folding
- dead code elimination
- partial evaluation

---

## 12. Execution Example

Program:

```

!x = 5 + 3

```

AST:

```

AssignNode
└ BinaryOpNode

```

Execution:

1. Evaluate BinaryOpNode → 8  
2. Assign to x

---

## 13. Design Guarantees

AST design guarantees:

- deterministic execution
- clear structure
- extensibility
- seamless Python integration
- compatibility with interpreter and compiler models

---

## 14. Limitations

Current AST does not include:

- static type enforcement
- compile-time optimization metadata
- advanced static analysis hooks
