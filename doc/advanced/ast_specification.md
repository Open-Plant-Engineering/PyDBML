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

Semantics:

- Resolve object
- Resolve method
- Execute method

---

### 4.12 ObjectNode

```

ObjectNode:
type\_name: identifier
args: list\[expression]

```

Creates object instance.

---

### 4.13 DotAccessNode

```

DotAccessNode:
target: expression
attribute: identifier

```

Returns attribute or method reference.

---

### 4.14 DotAssignNode

```

DotAssignNode:
target: expression
attribute: identifier
value: expression

```

Assigns object attribute.

---

### 4.15 IndexAccessNode

```

IndexAccessNode:
target: expression
index: expression

```

Retrieves array value.

---

### 4.16 IndexAssignNode

```

IndexAssignNode:
target: expression
index: expression
value: expression

```

Sets array value.

---

### 4.17 ReturnNode

```

ReturnNode:
value: expression

```

Raises ReturnSignal.

---

### 4.18 HandleNode

```

HandleNode:
try\_block: block
handlers: list\[(condition, block)]
else\_block: block

```

Handles errors.

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

## 9. Error Integration

Nodes may:

- raise errors
- propagate errors
- handle errors (HandleNode)

---

## 10. Optimization Potential

AST enables:

- constant folding
- dead code elimination
- partial evaluation

---

## 11. Execution Example

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

## 12. Design Guarantees

AST design guarantees:

- deterministic execution
- clear structure
- extensibility
- compatibility with interpreter and compiler models

---

## 13. Limitations

Current AST does not include:

- type annotations in nodes (runtime only)
- optimization metadata
- static analysis hooks
