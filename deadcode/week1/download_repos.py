import os
from git import Repo

PROJECT_ROOT = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis"
TARGET_DIR = os.path.join(PROJECT_ROOT, "deadcode", "week1", "dataset", "github_repos")

os.makedirs(TARGET_DIR, exist_ok=True)

REPOS = [
    "https://github.com/pallets/flask.git",
    "https://github.com/psf/requests.git",
    "https://github.com/tiangolo/fastapi.git",
]

for url in REPOS:
    name = url.split("/")[-1].replace(".git", "")
    path = os.path.join(TARGET_DIR, name)
    if not os.path.exists(path):
        print(f"Cloning {name}...")
        Repo.clone_from(url, path, depth=1)
        print(f"✅ {name} cloned successfully!")
    else:
        print(f"⚠️ {name} already exists, skipping.")
