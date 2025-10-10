# safe_flow.py

def safe_input_usage():
    # Example 1: Sanitizing input before using
    user_input = input("Enter filename: ")
    safe_input = user_input.replace("..", "").strip()
    with open(safe_input, "r") as f:
        data = f.read()
    print("File content read safely.")

def safe_password_handling():
    # Example 2: Never printing or logging sensitive data
    import getpass
    password = getpass.getpass("Enter password: ")
    if len(password) >= 8:
        print("Password accepted (not stored or logged).")

def validated_command():
    # Example 3: Command selection is validated
    cmd = input("Enter command (start/stop): ")
    if cmd in ["start", "stop"]:
        print(f"System will {cmd}.")
    else:
        print("Invalid command.")

def hashed_data_flow():
    # Example 4: Sensitive data is hashed before use
    import hashlib
    data = input("Enter your secret key: ")
    hashed = hashlib.sha256(data.encode()).hexdigest()
    print("Hash generated successfully.")
