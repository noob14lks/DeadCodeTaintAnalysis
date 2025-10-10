import csv
import json
import os

PROJECT_ROOT = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis"
MEM1_LABELS = os.path.join(PROJECT_ROOT, "deadcode", "week1", "labels.csv")
MEM2_LABELS = os.path.join(PROJECT_ROOT, "taint_analysis", "week1", "labels.csv")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "code_integration", "week1", "mock_data.json")

def load_member1_dead_code(labels_file):
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

def load_member2_taint(labels_file):
    taint_flows = []
    with open(labels_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            file = row["file"]
            source = row["source_function"]
            sink = row["sink_function"]
            label = row["label"]
            if not file or not source or not sink:
                continue
            taint_flows.append({
                "file": file,
                "source": source,
                "sink": sink,
                "label": label
            })
    return taint_flows

def main():
    dead_code = load_member1_dead_code(MEM1_LABELS)
    taint_flows = load_member2_taint(MEM2_LABELS)

    combined_data = {
        "dead_code": dead_code,
        "taint_flows": taint_flows
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2)

    print(f"✅ mock_data.json created at {OUTPUT_FILE} with {len(dead_code)} dead code files and {len(taint_flows)} taint flows!")

if __name__ == "__main__":
    main()
