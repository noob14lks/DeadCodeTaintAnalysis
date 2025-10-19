import os
import csv

SOURCE_KEYWORDS = ['input(', 'request.args', 'request.form', 'os.environ']
SINK_KEYWORDS = ['os.system', 'subprocess.run', 'eval', 'exec', 'open(', 'requests.get', 'cursor.execute']

def find_taint_flows(file_path, base_dir):
    taint_flows = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            source = next((src for src in SOURCE_KEYWORDS if src in line), None)
            if source:
                for j in range(i, min(i + 5, len(lines))): 
                    sink = next((snk for snk in SINK_KEYWORDS if snk in lines[j]), None)
                    if sink:
                        relative_path = os.path.relpath(file_path, base_dir)
                        taint_flows.append({
                            'file': relative_path,
                            'line': i + 1,
                            'source': source,
                            'sink': sink,
                            'snippet': lines[i].strip() + '  -->  ' + lines[j].strip()
                        })
                        break
    except Exception as e:
        print(f" Error reading {file_path}: {e}")

    return taint_flows

def analyze_all_repos(base_dir):
    all_flows = []
    for dirpath, _, filenames in os.walk(base_dir):
        for file in filenames:
            if file.endswith('.py'):
                file_path = os.path.join(dirpath, file)
                flows = find_taint_flows(file_path, base_dir)
                all_flows.extend(flows)
    return all_flows

def write_csv(flows, output_csv_path):
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file', 'line', 'source', 'sink', 'snippet']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in flows:
            writer.writerow(row)

if __name__ == "__main__":
    dataset_dir = os.path.join(os.path.dirname(__file__), 'dataset')
    output_csv = os.path.join(os.path.dirname(__file__), 'taint_flows.csv')

    print(f" Scanning Python files in: {dataset_dir}")
    flows = analyze_all_repos(dataset_dir)
    write_csv(flows, output_csv)
    print(f" Done! Found {len(flows)} taint flows.")
    print(f" Results saved to: {output_csv}")
