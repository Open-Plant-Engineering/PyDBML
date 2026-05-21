
# Evaluation Semantics

## 1. Evaluation Model

- Expressions evaluated recursively
- Statements executed sequentially

---

## 2. Scope Resolution

Order:

1. Local scope
2. Global scope
3. Error if not found

---

## 3. Short Circuit Evaluation

```

AND
OR

```

Evaluate lazily.

---

## 4. Function Execution

- New scope created
- Parameters assigned
- Return exits execution