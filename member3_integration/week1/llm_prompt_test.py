import json

def summarize_issues(issues):
    """Mock LLM summary generator (replace with OpenAI API later)."""
    summaries = []
    for issue in issues:
        if issue["issue_type"] == "Dead Code":
            text = f"The file {issue['file']} contains unused functions which may clutter the codebase."
        elif issue["issue_type"] == "Taint Flow":
            text = f"The file {issue['file']} shows suspicious data flow from user input to system calls, which is risky."
        else:
            text = f"The file {issue['file']} has general code issues."
        summaries.append(text)
    return summaries

def main():
    with open("mock_data.json", "r", encoding="utf-8") as f:
        mock_data = json.load(f)

    issues = []
    for file, info in mock_data["dead_code_results"].items():
        if info["functions"]:
            issues.append({"file": file, "issue_type": "Dead Code"})

    for file, info in mock_data["taint_analysis_results"].items():
        if info["tainted_flows"]:
            issues.append({"file": file, "issue_type": "Taint Flow"})

    summaries = summarize_issues(issues)
    print("\n".join(summaries))

if __name__ == "__main__":
    main()
