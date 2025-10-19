import json
import re
import csv
import os

DATASET_DIR = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis\deadcode\\dataset"
PARSED_JSON = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis\deadcode\\parsed_functions.json"
OUTPUT_CSV = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis\deadcode\\labels.csv"

with open(PARSED_JSON, "r", encoding="utf-8") as f:
    parsed = json.load(f)

labels = []

for file, items in parsed.items():
    abs_file_path = os.path.normpath(os.path.join(DATASET_DIR, file))
    
    try:
        with open(abs_file_path, "r", encoding="utf-8") as f:
            code = f.read()

        for func in items.get("functions", []) + items.get("classes", []):
            label = "used" if re.search(rf"\b{func}\s*\(", code) else "unused"
            labels.append([file, func, label])
    
    except Exception as e:
        print(f"⚠️ Skipping {file}: {e}")
        continue

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["file", "function_or_class", "label"])
    writer.writerows(labels)

print(f"✅ labels.csv created successfully at {OUTPUT_CSV} with {len(labels)} entries!")