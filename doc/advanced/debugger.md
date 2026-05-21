# Debugger Specification

## 1. Overview

The PyDBML debugger provides runtime inspection and control of program execution.

The debugger operates within the evaluator and allows:

- step-by-step execution
- breakpoint control
- variable inspection
- execution flow tracing

The debugger is synchronous and single-threaded.

---

## 2. Debugger Model

### 2.1 Integration

The debugger is integrated into the evaluator.

Each AST node triggers a debug hook:

```

evaluate(node) → \_trace(node)

```

---

### 2.2 Execution States

Execution can be in one of the following states:

- running
- paused
- stepping
- stepping over
- stepping out

---

## 3. Breakpoints

---

### 3.1 Definition

A breakpoint is associated with a source code line.

```

line → breakpoint

```

---

### 3.2 Types

#### Unconditional Breakpoint

```

pause when execution reaches line

```

---

#### Conditional Breakpoint

```

pause when condition evaluates to true

```

Example:

```

b 10 if !x > 5

```

---

### 3.3 Storage

Breakpoints are stored as:

```

line\_number → condition\_ast

```

---

### 3.4 Evaluation

When execution reaches a node:

1. Check if node has line metadata
2. If line matches breakpoint:
   - evaluate condition (if any)
   - pause execution if condition true

---

## 4. Execution Control

---

### 4.1 Continue

```

c / continue

```

- resumes execution
- disables stepping mode

---

### 4.2 Step Into

```

s / step

```

- executes next node
- pauses again after execution

---

### 4.3 Step Over

```

n / next

```

- executes current node
- skips stepping into deeper calls
- pauses at same depth

---

### 4.4 Step Out

```

o / out

```

- continues execution until exiting current scope
- pauses when returning to previous stack level

---

## 5. Execution Depth

Debugger tracks:

```

call\_stack depth

```

Used for:

- step over control
- step out control

---

## 6. Variable Inspection

---

### 6.1 Print Variables

```

p

```

Displays:

- local variables
- global variables

---

### 6.2 Print Specific Variable

```

p x

```

Displays:

```

x = value

```

---

## 7. Watch System

---

### 7.1 Add Watch

```

watch x

```

Adds variable to watch list.

---

### 7.2 Remove Watch

```

unwatch x

```

---

### 7.3 Behavior

- watched variables are printed on each pause
- values resolved from environment

---

## 8. Stack Inspection

---

### 8.1 Command

```

bt / stack

```

---

### 8.2 Output

Displays:

- current call stack
- node types
- line positions

---

## 9. Debug State

---

### 9.1 Snapshot

At each pause, debugger generates state:

```

{
line,
column,
node,
depth,
locals,
globals,
watch,
stack
}

```

---

### 9.2 Purpose

State is used for:

- UI integration
- debugging tools
- logging

---

## 10. Pause Behavior

Execution pauses when:

- breakpoint triggered
- step mode enabled
- step over condition met
- step out condition met

---

## 11. Control Loop

During pause:

Debugger enters command loop:

```

(wait for command)
execute command
resume execution

```

---

## 12. Command Set

| Command | Description |
|--------|------------|
| c / continue | resume execution |
| s / step     | step into |
| n / next     | step over |
| o / out      | step out |
| p            | print variables |
| p x          | print variable |
| watch x      | add watch |
| unwatch x    | remove watch |
| bt / stack   | show stack |
| b line       | set breakpoint |
| rb line      | remove breakpoint |
| q / quit     | terminate execution |

---

## 13. Interaction Model

Commands may be:

- interactive (console input)
- programmatic (via debug controller)

---

## 14. Debug Controller

The debugger may delegate control to:

```

DebugController

```

Used for:

- UI-based debugging
- external control systems

---

## 15. Execution Guarantees

Debugger guarantees:

- consistent pause points
- deterministic stepping behavior
- accurate variable inspection
- non-destructive execution state

---

## 16. Limitations

The debugger does not support:

- multi-threaded debugging
- asynchronous breakpoints
- time-travel debugging
- reverse execution

---

## 17. Example

```

!x = 5
!y = 10

b 2

```

Execution:

1. line 1 executes
2. line 2 reached → breakpoint
3. debugger pauses

---

## 18. Integration

Debugger operates entirely inside evaluator.

No separate runtime is required.

---

## 19. Error Interaction

Debugger does not intercept control signals:

```

ReturnSignal
BreakSignal
ContinueSignal

```

Errors may still propagate normally.

---

## 20. Summary

The PyDBML debugger:

- integrates with AST evaluation
- provides fine-grained execution control
- enables runtime inspection
- supports extensible control mechanisms
