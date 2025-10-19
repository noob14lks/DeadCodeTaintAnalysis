import json
import os
import textwrap

PROJECT_ROOT = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis"
MOCK_DATA_FILE = os.path.join(PROJECT_ROOT, "code_integration", "mock_data.json")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "code_integration", "explanations.txt")

def load_mock_data(path=MOCK_DATA_FILE):
    if not os.path.exists(path):
        raise FileNotFoundError(f"mock_data.json not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def is_short_function_name(name):
    return len(name) <= 4 or name.startswith("tmp") or name.startswith("test")

def looks_like_placeholder(func_info):
    name = func_info.get("name", "")
    status = func_info.get("status", "")
    if status == "unused" and (is_short_function_name(name) or name.startswith("unused") or name.startswith("debug")):
        return True
    return False

def generate_dead_code_explanation(file, func):
    name = func.get("name", "<unknown>")
    status = func.get("status", "unused")
    reasons = []

    if status == "unused":
        reasons.append(f"The function `{name}` is not referenced or called within `{file}` (labeled unused).")
    else:
        reasons.append(f"The function `{name}` is marked `{status}`.")

    if looks_like_placeholder(func):
        reasons.append("The function name and body suggest this may be a placeholder or debug helper (e.g., short name or 'unused' prefix).")
    else:
        reasons.append("It may still be unused because it lacks references, docstrings, or it only contains trivial code like `pass` or simple prints.")

    risk = "Low"
    if name.lower().startswith(("password", "secret", "key")) or "token" in name.lower():
        risk = "High"
        reasons.append("The function name suggests it may be handling secrets — unused secret-handling code can be a hidden risk.")
    elif "log" in name.lower():
        risk = "Medium"
        reasons.append("Even if unused, functions that log sensitive-sounding variables (e.g., passwords) could leak secrets if later wired in incorrectly.")

    suggestion = []
    suggestion.append("Remove or archive this function if genuinely unused, or add clear docstrings and tests to justify keeping it.")
    if risk in ("High", "Medium"):
        suggestion.append("If it touches secrets or sensitive data, rotate any credentials and audit surrounding code for accidental usage.")

    explanation = textwrap.dedent(f"""
    FILE: {file}
    ISSUE: Dead / Unused function `{name}` (status: {status})
    RISK: {risk}
    WHY:
      - {' '.join(reasons)}
    SUGGESTIONS:
      - {' '.join(suggestion)}
    """).strip()

    return explanation

def build_explanations(data):
    explanations = []
    dead_code = data.get("dead_code", [])

    for file_entry in dead_code:
        file = file_entry.get("file", "<unknown>")
        for func in file_entry.get("functions", []):
            if func.get("status", "") == "unused":
                explanations.append(generate_dead_code_explanation(file, func))
            else:
                if looks_like_placeholder(func):
                    explanations.append(generate_dead_code_explanation(file, func))

    return explanations

def save_explanations(explanations, path=OUTPUT_FILE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(explanations))
    print(f"✅ Explanations written to: {path}")

def main():
    try:
        data = load_mock_data()
    except FileNotFoundError as e:
        print("ERROR:", e)
        print("Make sure mock_data.json exists. Run generate_mock_data.py first.")
        return

    explanations = build_explanations(data)

    if not explanations:
        print("No issues found to explain.")
    else:
        print("\n\n--- EXPLANATIONS PREVIEW ---\n")
        for ex in explanations:
            print(ex)
            print("\n" + "-" * 60 + "\n")

        save_explanations(explanations)

if __name__ == "__main__":
    main()
