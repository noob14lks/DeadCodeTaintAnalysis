import ast
import os
import json

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
                results[path] = {
                    "functions": funcs,
                    "classes": cls
                }
    return results

if __name__ == "__main__":
    directory = "./dataset"
    parsed_data = parse_directory(directory)
    print(json.dumps(parsed_data, indent=2))
