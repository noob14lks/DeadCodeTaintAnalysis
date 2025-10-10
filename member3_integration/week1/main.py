import json
from pathlib import Path

def load_mock_data():
    mock_file = Path(__file__).parent / "mock_data.json"
    with open(mock_file, "r", encoding="utf-8") as f:
        return json.load(f)

def integrate_results(dead_code_data, taint_data):
    """Combine both analyses into a single risk summary."""
    integrated_results = []

    for file, info in dead_code_data.items():
        integrated_results.append({
            "file": file,
            "issue_type": "Dead Code",
            "details": f"{len(info['functions'])} unused or rarely used functions",
            "risk_level": "Low"
        })

    for file, info in taint_data.items():
        integrated_results.append({
            "file": file,
            "issue_type": "Taint Flow",
            "details": f"{len(info['tainted_flows'])} suspicious data flows",
            "risk_level": "High" if len(info['tainted_flows']) > 0 else "Low"
        })

    return integrated_results

def main():
    print("🚀 Secure Dead Code & Taint Analysis Tool (Prototype)")
    mock_data = load_mock_data()

    integrated = integrate_results(
        mock_data["dead_code_results"],
        mock_data["taint_analysis_results"]
    )

    print(json.dumps(integrated, indent=2))

if __name__ == "__main__":
    main()
