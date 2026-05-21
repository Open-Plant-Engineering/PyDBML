
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

- Conditions evaluated in order
- First true condition executes
- Else executes if no match

---

## 2. DO Loop

### 2.1 Range Loop

```

do !i from start to end
statements
enddo

```

---

### 2.2 Index Loop

```

do !i indices !arr
statements
enddo

```

---

### 2.3 Value Loop

```

do !v values !arr
statements
enddo

```

---

### 2.4 Infinite Loop

```

do
statements
enddo

```

---

## 3. Loop Control

### Break

```

break

```

Exits loop immediately.

---

### Skip

```

skipif (condition)

```

Skips current iteration.