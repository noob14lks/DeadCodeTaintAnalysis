# risky_flow.py

import os
import subprocess

def direct_system_call():
    # Example 1: Directly executing user input
    command = input("Enter system command: ")
    os.system(command)  # ❌ Dangerous: Command injection possible

def eval_user_input():
    # Example 2: Evaluating raw input
    user_expr = input("Enter expression: ")
    eval(user_expr)  # ❌ Dangerous: Code execution

def insecure_file_access():
    # Example 3: Using user input as filename directly
    filename = input("Enter file to delete: ")
    os.remove(filename)  # ❌ Dangerous: Arbitrary file deletion

def password_logging():
    # Example 4: Logging sensitive data in plain text
    password = input("Enter password: ")
    with open("log.txt", "w") as f:
        f.write(password)  # ❌ Sensitive data exposure

def network_command_injection():
    # Example 5: Passing untrusted network data to shell
    import socket
    s = socket.socket()
    s.bind(("localhost", 8080))
    s.listen(1)
    conn, _ = s.accept()
    data = conn.recv(1024).decode()
    subprocess.run(data, shell=True)  # ❌ Dangerous: Remote command execution
