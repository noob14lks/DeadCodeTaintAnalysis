# taint_tracker.py
import ast
import json
import sys
from pathlib import Path
from typing import Set, Dict, List, Any, Optional

# --- Configuration: Define Sources, Sinks, and Sanitizers ---
SOURCES: Set[str] = {'input', 'os.getenv', 'request.args.get', 'request.form.get'}
SINKS: Set[str] = {'os.system', 'eval', 'exec', 'subprocess.run', 'subprocess.call'}
SANITIZERS: Set[str] = {'str', 'int', 'float', 'escapeshellarg'}

class TaintVisitor(ast.NodeVisitor):
    """AST visitor to track tainted variables from sources to sinks."""
    def __init__(self):
        # {var_name: {'source_lineno': int, 'distance': int, 'sanitized': bool}}
        self.tainted_vars: Dict[str, Dict[str, Any]] = {}
        self.flagged_flows: List[Dict[str, Any]] = []

    def _get_function_name(self, node: ast.Call) -> Optional[str]:
        """Extracts a full function name (e.g., 'os.system') from a call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        if isinstance(node.func, ast.Attribute):
            parts = []
            curr = node.func
            while isinstance(curr, ast.Attribute):
                parts.append(curr.attr)
                curr = curr.value
            if isinstance(curr, ast.Name):
                parts.append(curr.id)
                return ".".join(reversed(parts))
        return None

    def visit_Assign(self, node: ast.Assign):
        """Handle taint introduction and propagation on assignment."""
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            self.generic_visit(node)
            return

        target_name = node.targets[0].id
        value_node = node.value

        # Case 1: Taint Introduction (e.g., x = input())
        if isinstance(value_node, ast.Call):
            func_name = self._get_function_name(value_node)
            if func_name in SOURCES:
                self.tainted_vars[target_name] = {'source_lineno': node.lineno, 'distance': 0, 'sanitized': False}
            # Case 1b: Sanitization (e.g., x = int(y))
            elif func_name in SANITIZERS and value_node.args and isinstance(value_node.args[0], ast.Name):
                arg_name = value_node.args[0].id
                if arg_name in self.tainted_vars:
                    self.tainted_vars[target_name] = self.tainted_vars[arg_name].copy()
                    self.tainted_vars[target_name]['sanitized'] = True
        # Case 2: Taint Propagation (e.g., y = x)
        elif isinstance(value_node, ast.Name):
            source_name = value_node.id
            if source_name in self.tainted_vars:
                self.tainted_vars[target_name] = self.tainted_vars[source_name].copy()
                self.tainted_vars[target_name]['distance'] += 1
        
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        """Check if a tainted variable is used in a sink function."""
        func_name = self._get_function_name(node)
        if func_name in SINKS:
            for arg in node.args:
                if isinstance(arg, ast.Name) and arg.id in self.tainted_vars:
                    taint_info = self.tainted_vars[arg.id]
                    self.flagged_flows.append({
                        'source_variable': arg.id,
                        'source_lineno': taint_info['source_lineno'],
                        'sink_function': func_name,
                        'sink_lineno': node.lineno,
                        'distance': taint_info['distance'] + 1,
                        'sanitized': taint_info['sanitized']
                    })
        self.generic_visit(node)

def analyze_file(filepath: Path) -> List[Dict[str, Any]]:
    """Parses a single Python file and returns a list of flagged flows."""
    print(f"[*] Analyzing '{filepath}'...")
    try:
        source_code = filepath.read_text(encoding="utf-8")
        tree = ast.parse(source_code, filename=str(filepath))
        visitor = TaintVisitor()
        visitor.visit(tree)
        # Add the filename to each flow found in this file
        for flow in visitor.flagged_flows:
            flow['filename'] = str(filepath)
        return visitor.flagged_flows
    except Exception as e:
        print(f"⚠️  Skipping '{filepath}' due to an error: {e}")
        return []


def main():
    """Main function to drive the script."""
    # --- Hardcode the path to your dataset here ---
    # ⬇️ MAKE SURE TO REPLACE THIS WITH THE ACTUAL PATH ON YOUR COMPUTER ⬇️
    TARGET_DIRECTORY_PATH = r"C:\Users\outhd\OneDrive\toac\DeadCodeTaintAnalysis\taint_analysis\week1\dataset\github_repos"

    target_path = Path(TARGET_DIRECTORY_PATH)
    
    # It's still a good idea to check if the path is valid!
    if not target_path.is_dir():
        print(f"Error: The hardcoded path '{target_path}' does not exist or is not a valid directory.")
        # We don't need sys.exit(1) here, but returning is clean.
        return
    
    # ... rest of the code
    all_flows = [flow for filepath in target_path.rglob("*.py") for flow in analyze_file(filepath)]

    print("\n--- Analysis Complete ---")
    if not all_flows:
        print("✅ No tainted flows found across all files.")
        return

    print(f"Found {len(all_flows)} total potential tainted flow(s).")
    output_file = "flows.json"
    with open(output_file, 'w') as f:
        json.dump(all_flows, f, indent=2)
    print(f"\nFlow details for all files saved to {output_file}")

if __name__ == "__main__":
    main()