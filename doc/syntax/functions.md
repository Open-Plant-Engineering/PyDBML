
# Functions

## 1. Definition

Functions are user-defined blocks of reusable logic.

### Syntax

```

define function !!name(param1 is TYPE, param2 is TYPE) is RETURN\_TYPE
statements
endfunction

```

---

## 2. Invocation

Functions are invoked using:

```

!x = !!name(10, 20)

```

### Behavior

- Function name must be global (`!!`)
- Arguments are evaluated before invocation
- Result of function is returned as expression value

---

## 3. Parameters

Parameters are defined with names and types:

```

param\_name is TYPE

```

### Example

```

define function !!add(!a is REAL, !b is REAL) is REAL
return !a + !b
endfunction

```

---

### Behavior

- Arguments are evaluated before binding
- Values are assigned to parameters in order
- Parameter count must match argument count

If mismatch:

```

ARG\_COUNT error

```

---

## 4. Return

```

return expression

```

---

### Behavior

- Immediately stops function execution
- Returns evaluated value to caller
- Implemented using `ReturnSignal`

---

## 5. Execution Model

When a function is called:

1. Evaluate arguments
2. Create new local scope
3. Bind parameters to evaluated values
4. Execute statements sequentially
5. Stop execution on `return`
6. Destroy scope
7. Return result

---

## 6. Scope Behavior

- Each function call creates a new isolated scope
- Local variables inside function do not affect outer scope
- Global variables can be accessed unless overridden

### Example

```

!x = 10

define function !!test() is REAL
!x = 5
return !x
endfunction

!y = !!test()

```

Result:

```

y = 5
x = 10  (unchanged global)

```

---

## 7. Type Enforcement

Functions declare a return type:

```

is RETURN\_TYPE

```

### Rules

- Returned value must match declared type
- If mismatch → error raised:

```

RETURN\_TYPE error

```

---

## 8. Expression Integration

Functions can be used inside expressions:

```

!x = !!add(5, 3) \* 2

```

---

### Behavior

- Function executes before outer expression
- Result is used in enclosing computation

---

## 9. Interaction with Objects and Python

Functions can interact with:

- PyDBML objects
- Plugin objects
- Python modules

---

### Example

```

import module builtins

define function !!writeFile(!text is STRING) is REAL
!f = object open('file.txt', 'w')
!f.write(!text)
!f.close()
return 1
endfunction

```

---

### Behavior

- Functions can create Python objects
- Call Python methods
- Return results of Python operations

---

## 10. Error Behavior

Errors inside functions:

- propagate to caller
- can be handled using `HANDLE`

---

### Example

```

define function !!safeDiv(!a is REAL, !b is REAL) is REAL
HANDLE ANY
return 0
ELSEHANDLE NONE
return !a / !b
ENDHANDLE
endfunction

```

---

## 11. Nested Execution

Functions may call other functions:

```

define function !!square(!x is REAL) is REAL
return !x \* !x
endfunction

define function !!compute(!a is REAL) is REAL
return !!square(!a) + 1
endfunction

```

---

## 12. Execution Guarantees

Functions guarantee:

- isolated execution scope
- deterministic behavior
- predictable return flow
- consistent type enforcement

---

## 13. Limitations

- No recursion depth limits enforced explicitly (runtime dependent)
- No default parameter values
- No variadic arguments
- No closures or lexical capture
