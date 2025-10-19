import json
import os

PROJECT_ROOT = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis"
MOCK_DATA_PATH = os.path.join(PROJECT_ROOT, "code_integration", "week1", "mock_data.json")

def load_mock_data():
    with open(MOCK_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_dead_code(dead_code):
    print("\n--- Dead Code Summary ---")
    for file_data in dead_code:
        file = file_data["file"]
        for func in file_data["functions"]:
            print(f"{file}: {func['name']} → {func['status']}")

def summarize_semgrep_findings(semgrep_findings):
    for finding in semgrep_findings:
        print(f"{finding['path']} [{finding['severity']}]")
        print(f"  → {finding['check_id']}")
        print(f"  → Lines {finding['start_line']} to {finding['end_line']}\n")

def main():
    data = load_mock_data()
    summarize_dead_code(data.get("dead_code", []))
    summarize_semgrep_findings(data.get("semgrep_findings", []))

if __name__ == "__main__":
    main()
