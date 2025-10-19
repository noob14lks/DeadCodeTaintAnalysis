import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REPO_BASE = os.path.join(BASE_DIR, 'dataset', 'github_repos')

OUTPUT_DIR = os.path.join(BASE_DIR, 'analysis_results')
os.makedirs(OUTPUT_DIR, exist_ok=True)

repos = [d for d in os.listdir(REPO_BASE) if os.path.isdir(os.path.join(REPO_BASE, d))]

CONFIG_PATH = os.path.join(BASE_DIR, 'lanalyzer_config.json')

for repo in repos:
    repo_path = os.path.join(REPO_BASE, repo)
    output_path = os.path.join(OUTPUT_DIR, f"{repo}_analysis.txt")

    print(f"Running analysis on {repo}...")

    with open(output_path, 'w') as outfile:
        subprocess.run(
            [
                'lanalyzer',
                'analyze',
                '--target', repo_path,
                '--config', CONFIG_PATH,
                '--debug'
            ],
            stdout=outfile,
            stderr=subprocess.STDOUT
        )

print("\nAll repositories analyzed. Check the 'analysis_results' folder.")
