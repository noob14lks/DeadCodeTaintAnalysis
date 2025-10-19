import ast
import os
import json

PROJECT_ROOT = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis"
DATASET_DIR = os.path.join(PROJECT_ROOT, "deadcode", "dataset")

def extract_functions_and_classes(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)

    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return functions, classes

def parse_directory(directory):
    results = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                funcs, cls = extract_functions_and_classes(path)
                results[os.path.relpath(path, DATASET_DIR)] = {  # use relative paths
                    "functions": funcs,
                    "classes": cls
                }
    return results

if __name__ == "__main__":
    parsed_data = parse_directory(DATASET_DIR)

    OUTPUT_PATH = os.path.join(PROJECT_ROOT, "deadcode", "week1", "parsed_functions.json")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=2)

    print(f"✅ JSON saved to {OUTPUT_PATH} with {len(parsed_data)} files parsed.")