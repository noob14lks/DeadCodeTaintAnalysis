"""
Download real-world Python repositories that likely contain
taint-related code (user input → sensitive operations).
"""

import os
from git import Repo

PROJECT_ROOT = r"C:\Users\outhd\OneDrive\toac\DeadCodeTaintAnalysis"
DEST_DIR = os.path.join(PROJECT_ROOT, "taint_analysis", "week1", "dataset", "github_repos")
LABELS_PATH = os.path.join(PROJECT_ROOT, "taint_analysis", "week1", "labels.csv")

REPOSITORIES = {
    "httpie": "https://github.com/httpie/httpie.git",
    "flask": "https://github.com/pallets/flask.git",
    "requests": "https://github.com/psf/requests.git",
    "paramiko": "https://github.com/paramiko/paramiko.git",
    "sqlalchemy": "https://github.com/sqlalchemy/sqlalchemy.git",
}

def clone_repo(name, url, dest_dir):
    """Clone repo if not already downloaded."""
    repo_path = os.path.join(dest_dir, name)
    if os.path.exists(repo_path):
        print(f"[SKIP] {name} already exists.")
        return
    try:
        print(f"[CLONING] {name}...")
        Repo.clone_from(url, repo_path, depth=1)
        print(f"[OK] {name} cloned successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to clone {name}: {e}")

def create_labels_file():
    """Create placeholder labels file for manual or automated annotation later."""
    if not os.path.exists(LABELS_PATH):
        with open(LABELS_PATH, "w", encoding="utf-8") as f:
            f.write("file,source_function,sink_function,label\n")
            f.write("# Example: app.py,input,os.system,tainted\n")
        print(f"[INFO] labels.csv created at {LABELS_PATH} for annotation.")

def main():
    os.makedirs(DEST_DIR, exist_ok=True)
    for name, url in REPOSITORIES.items():
        clone_repo(name, url, DEST_DIR)
    create_labels_file()

if __name__ == "__main__":
    main()
