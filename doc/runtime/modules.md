
# Module System

## 1. Overview

PyDBML supports importing Python modules into runtime.

---

## 2. Syntax

```

import module module\_name

```

---

## 3. Execution

1. Load Python module
2. Register contents in registry
3. Make accessible to runtime

---

## 4. Registered Objects

After import:

- functions → callable
- classes → object creation
- modules → namespace access

---

## 5. Example

```

import module builtins

!f = object open('file.txt', 'w')

```

---

## 6. Behavior

- Names are case-insensitive
- Functions become callable
- Classes become object types

---

## 7. Scope

Modules are global once imported

---

## 8. Errors

```

IMPORT\_ERROR → module not found

```