import os
import csv

PROJECT_ROOT = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis"
DATASET_DIR = os.path.join(PROJECT_ROOT, "taint_analysis", "week1", "dataset", "github_repos")
LABELS_PATH = os.path.join(PROJECT_ROOT, "taint_analysis", "week1", "labels.csv")

if not os.path.exists(DATASET_DIR):
    raise FileNotFoundError(f"{DATASET_DIR} does not exist!")

with open(LABELS_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["file", "source_function", "sink_function", "label"])

    for repo in os.listdir(DATASET_DIR):
        repo_path = os.path.join(DATASET_DIR, repo)
        if not os.path.isdir(repo_path):
            continue
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    abs_file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_file_path, DATASET_DIR)
                    writer.writerow([rel_path, "", "", ""])

print(f"✅ labels.csv created at {LABELS_PATH} for manual labeling.")
