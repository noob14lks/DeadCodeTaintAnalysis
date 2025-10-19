import json
import csv

with open('output.json', 'r', encoding='utf-16') as f:
    data = json.load(f)

results = data['results']

csv_columns = [
    "check_id",
    "path",
    "start_line",
    "start_col",
    "end_line",
    "end_col",
    "message",
    "severity",
    "confidence",
    "category",
    "likelihood",
    "impact",
    "fingerprint",
    "engine_kind"
]

with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

    for item in results:
        row = {
            "check_id": item.get("check_id"),
            "path": item.get("path"),
            "start_line": item.get("start", {}).get("line"),
            "start_col": item.get("start", {}).get("col"),
            "end_line": item.get("end", {}).get("line"),
            "end_col": item.get("end", {}).get("col"),
            "message": item.get("extra", {}).get("message"),
            "severity": item.get("extra", {}).get("severity"),
            "confidence": item.get("extra", {}).get("metadata", {}).get("confidence"),
            "category": item.get("extra", {}).get("metadata", {}).get("category"),
            "likelihood": item.get("extra", {}).get("metadata", {}).get("likelihood"),
            "impact": item.get("extra", {}).get("metadata", {}).get("impact"),
            "fingerprint": item.get("extra", {}).get("fingerprint"),
            "engine_kind": item.get("extra", {}).get("engine_kind")
        }
        writer.writerow(row)

print("CSV file 'results.csv' created successfully!")
