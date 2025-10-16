# Week 1 Research Notes — Member 2 (Taint Analysis)

## 1. Objective
The goal is to detect **tainted data flows** in Python programs — cases where untrusted input (source)
flows into sensitive operations (sink) without proper sanitization.  
This helps identify potential **backdoors, information leaks, or injection vulnerabilities**.

---

## 2. Key Concepts Reviewed

### 🔹 Taint Source
Origin of untrusted or external data.
- `input()`, `sys.argv`, `os.environ`
- Network or file reads
- Database or user API inputs

### 🔹 Taint Propagation
When a tainted variable is assigned or passed into another variable or function.
Example:
```python
user_input = input()
query = "SELECT * FROM users WHERE name='" + user_input + "'"
