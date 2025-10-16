# Source and Sink Patterns for Taint Analysis
## 🔹 Overview
In taint analysis, **sources** are points where untrusted or sensitive data enters a program, and **sinks** are points where data leaves the program or is executed in a way that could cause harm.  
The goal is to track whether **tainted data (from a source)** flows into a **sink** without proper sanitization.

---

## 🔸 Common Source Patterns
| Source Type | Example Code | Description |
|--------------|--------------|-------------|
| User Input | `input()` | Direct user-provided data |
| Web Request | `request.GET['username']` | Data from HTTP requests |
| File Read | `open('data.txt').read()` | Reading external or untrusted files |
| Environment Variables | `os.getenv('API_KEY')` | External environment configuration |
| Command-Line Args | `sys.argv` | User input from command-line interface |

---

## 🔸 Common Sink Patterns
| Sink Type | Example Code | Risk Description |
|------------|--------------|------------------|
| System Command | `os.system(user_input)` | Command Injection risk |
| File Write | `open('file.txt', 'w').write(user_input)` | Data tampering or leakage |
| Database Query | `cursor.execute(f"SELECT * FROM users WHERE name='{user_input}'")` | SQL Injection risk |
| Print/Logging | `print(password)` | Sensitive information exposure |
| Network Send | `requests.post(url, data=user_input)` | Data exfiltration risk |

---

## 🔸 Sanitization Functions (Safe Usage)
| Function | Purpose |
|-----------|----------|
| `html.escape()` | Escapes HTML characters |
| `shlex.quote()` | Escapes shell arguments |
| `re.escape()` | Escapes regex patterns |
| `urllib.parse.quote()` | URL-encodes unsafe data |

---

## 🔸 Example Source → Sink Flow

```python
user_input = input("Enter command: ")
os.system(user_input)  

import shlex
user_input = input("Enter command: ")
safe_input = shlex.quote(user_input)
os.system(safe_input)  
