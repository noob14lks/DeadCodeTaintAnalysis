# feature_extraction.py
import json
import csv
import sys
import re

def contains_sensitive_keyword(var_name: str) -> bool:
    """Check if a variable name contains sensitive keywords."""
    sensitive_words = ['password', 'secret', 'key', 'token', 'auth', 'passwd']
    return any(re.search(word, var_name, re.IGNORECASE) for word in sensitive_words)

def extract_features(flows_data: list) -> list:
    """Extracts features from the flow data and returns a list of feature dicts."""
    feature_list = []
    for flow in flows_data:
        var_name = flow['source_variable']
        features = {
            'filename': flow['filename'],
            'sink_lineno': flow['sink_lineno'],
            'flow_length': flow['distance'],
            'contains_password': 1 if contains_sensitive_keyword(var_name) else 0,
            'is_sanitized': 1 if flow['sanitized'] else 0,
            'sink_function': flow['sink_function'],
        }
        feature_list.append(features)
    return feature_list

def main():
    """Main function to drive feature extraction."""
    input_json_path = "flows.json"
    output_csv_path = "features.csv"

    try:
        with open(input_json_path, 'r') as f:
            flows = json.load(f)
    except FileNotFoundError:
        print(f"Error: '{input_json_path}' not found. Run taint_tracker.py first.")
        sys.exit(1)
    
    if not flows:
        print("Input file contains no flows. Exiting.")
        return

    print(f"[*] Extracting features from {len(flows)} flows...")
    features = extract_features(flows)
    
    header = features[0].keys()
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(features)

    print(f"✅ Features successfully extracted and saved to '{output_csv_path}'.")

if __name__ == "__main__":
    main()