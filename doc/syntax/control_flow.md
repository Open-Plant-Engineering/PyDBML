
# Control Flow

## 1. IF Statement

### Syntax

```

if (condition) then
statements
elseif (condition) then
statements
else
statements
endif

```

---

### Behavior

- Conditions are evaluated sequentially (top to bottom)
- The first condition that evaluates to `true` is executed
- Remaining conditions are skipped after a match
- If no condition matches, the `else` block is executed (if present)

---

### Evaluation Rules

- Each condition is evaluated only once
- Evaluation stops immediately after the first `true` condition
- Expressions inside conditions follow standard evaluation rules

---

### Example

```

if (!x > 10) then
!y = 1
elseif (!x > 5) then
!y = 2
else
!y = 3
endif

```

---

## 2. DO Loop

Loops execute a block of statements repeatedly based on the defined mode.

---

### 2.1 Range Loop

```

do !i from start to end
statements
enddo

```

---

### Behavior

- `start` and `end` are evaluated once before loop execution
- Variable `!i` is initialized with `start`
- Loop runs until termination condition is met
- Step defaults to `+1` unless specified (if supported)

---

### 2.2 Index Loop

```

do !i indices !arr
statements
enddo

```

---

### Behavior

- Iterates over indices of the array
- `!i` receives index values (`0 → length-1`)
- Array is evaluated once before iteration

---

### 2.3 Value Loop

```

do !v values !arr
statements
enddo

```

---

### Behavior

- Iterates over values of the array
- `!v` receives each element value
- Useful for direct data processing

---

### 2.4 Infinite Loop

```

do
statements
enddo

```

---

### Behavior

- Executes indefinitely
- Must be terminated explicitly using `break`

---

## 3. Loop Control

---

### 3.1 Break

```

break

```

---

### Behavior

- Immediately exits the nearest enclosing loop
- Implemented internally using `BreakSignal`
- No further iterations are executed

---

### 3.2 Conditional Break

```

break if (condition)

```

---

### Behavior

- Evaluates condition inside loop
- If `true` → loop terminates immediately
- If `false` → loop continues

---

### 3.3 Skip

```

skipif (condition)

```

---

### Behavior

- Evaluates condition at current iteration
- If `true`:
  - Remaining statements in current iteration are skipped
  - Control moves to next iteration
- If `false`:
  - Execution continues normally

- Implemented internally using a control signal (`ContinueSignal`)

---

## 4. Execution Semantics

---

### Order of Execution Inside Loop

For each iteration:

1. Evaluate loop condition (if applicable)
2. Execute statements sequentially
3. Apply control signals:
   - `break` → exit loop
   - `skipif` → move to next iteration
4. Proceed to next iteration

---

## 5. Interaction with Other Constructs

---

### 5.1 Functions

- Loops inside functions follow function scope rules
- `break` affects only the loop, not the function

---

### 5.2 Error Handling

- Errors inside loops:
  - interrupt loop execution
  - propagate unless handled via `HANDLE`

---

### 5.3 Method Calls and Python Integration

- Loop bodies may contain:
  - object creation
  - method calls
  - Python function calls

Example:

```

import module builtins

do !i from 1 to 3
!f = object open('file.txt', 'a')
!f.write('Line')
!f.close()
enddo

```

---

## 6. Control Signals

Control flow constructs are implemented using signals:

| Signal | Trigger |
|--------|--------|
| BreakSignal | break |
| ContinueSignal | skipif |
| ReturnSignal | return |
| GoLabelSignal | label jump |

---

### Behavior

- Signals interrupt normal execution flow
- Signals propagate until handled by evaluator
- Signals are NOT errors

---

## 7. Guarantees

Control flow execution guarantees:

- deterministic evaluation
- predictable branching behavior
- strict loop boundaries
- consistent interaction with runtime and Python calls

---

## 8. Limitations

- No parallel loop execution
- No advanced loop constructs (e.g., generators, iterators)
- No built-in asynchronous control flow
