import json
import pandas as pd
import os

# === Paths ===
WEEK1_PARSED = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis\deadcode\parsed_functions.json"
WEEK1_LABELS = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis\deadcode\labels.csv"
OUTPUT_CSV = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis\deadcode\features.csv"

with open(WEEK1_PARSED, "r", encoding="utf-8") as f:
    parsed_data = json.load(f)

labels_df = pd.read_csv(WEEK1_LABELS)

features = []

for file, items in parsed_data.items():
    for func in items.get("functions", []) + items.get("classes", []):
        label_row = labels_df[
            (labels_df["file"] == file) & (labels_df["function_or_class"] == func)
        ]
        if label_row.empty:
            label = "unknown"
        else:
            label = label_row.iloc[0]["label"]

        features.append({
            "file": file,
            "name": func,
            "name_length": len(func),
            "is_class": func in items.get("classes", []),
            "has_underscore": "_" in func,
            "label": label
        })

# === Save as CSV ===
df = pd.DataFrame(features)
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Features extracted successfully: {len(df)} rows saved to {OUTPUT_CSV}")
