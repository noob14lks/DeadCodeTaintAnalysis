import csv
import json
import os

PROJECT_ROOT = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis"
MEM1_LABELS = os.path.join(PROJECT_ROOT, "deadcode", "week1", "labels.csv")
SEMGREP_FILE = os.path.join(PROJECT_ROOT, "taint_analysis", "week1", "output.json")  # Your Semgrep JSON file
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "code_integration", "week1", "mock_data.json")

def load_dead_code(labels_file):
    dead_code = {}
    with open(labels_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            file = row["file"]
            func = row["function_or_class"]
            status = row["label"]
            if file not in dead_code:
                dead_code[file] = {"file": file, "functions": []}
            dead_code[file]["functions"].append({"name": func, "status": status})
    return list(dead_code.values())

def load_semgrep_findings(json_file):
    try:
        with open(json_file, encoding="utf-16") as f:  # Use utf-16 if needed
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load Semgrep results: {e}")
        return []

    findings = []
    for item in data.get("results", []):
        findings.append({
            "check_id": item.get("check_id"),
            "path": item.get("path"),
            "start_line": item.get("start", {}).get("line"),
            "end_line": item.get("end", {}).get("line"),
            "message": item.get("extra", {}).get("message"),
            "severity": item.get("extra", {}).get("severity"),
            "category": item.get("extra", {}).get("metadata", {}).get("category"),
            "confidence": item.get("extra", {}).get("metadata", {}).get("confidence"),
            "likelihood": item.get("extra", {}).get("metadata", {}).get("likelihood"),
            "impact": item.get("extra", {}).get("metadata", {}).get("impact"),
            "engine_kind": item.get("extra", {}).get("engine_kind")
        })
    return findings

def main():
    dead_code = load_dead_code(MEM1_LABELS)
    semgrep_findings = load_semgrep_findings(SEMGREP_FILE)

    combined_data = {
        "dead_code": dead_code,
        "semgrep_findings": semgrep_findings
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2)

    print(f"✅ mock_data.json created at {OUTPUT_FILE} with:")
    print(f"   - {len(dead_code)} dead code files")
    print(f"   - {len(semgrep_findings)} semgrep findings")

if __name__ == "__main__":
    main()
