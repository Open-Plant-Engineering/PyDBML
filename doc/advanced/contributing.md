
# Contributing Guide

## 1. Overview

This guide explains how to extend PyDBML.

---

## 2. Adding New AST Node

1. Create node class
2. Add parser rule
3. Implement evaluator handler

---

## 3. Extending Evaluator

Add handler:

```

\_eval\_newnode(self, node)

```

---

## 4. Adding Plugin

1. Create Python class
2. Decorate with @pydbml_class
3. Add methods

---

## 5. Testing

- add pytest case
- validate execution

---

## 6. Guidelines

- keep evaluation deterministic
- follow naming conventions
- ensure type safety