
# Security Model

## 1. Overview

PyDBML allows execution of Python code via modules.

---

## 2. Risks

- File system access
- OS command execution
- External resource access

---

## 3. Current Behavior

No sandboxing is enforced.

---

## 4. Recommendations

- Restrict modules (e.g., os, subprocess)
- Use whitelisting
- Run in controlled environment

---

## 5. Future Improvements

- execution policies
- permission system
- restricted runtime mode

