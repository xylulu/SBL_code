import json

# Read the notebook
notebook_path = "/Users/xylu/Desktop/Data/code/Acoustic_csv_plotting_V6_LossMonitor_StoredInj.ipynb"
with open(notebook_path, 'r') as f:
    notebook = json.load(f)

# Find Cell 6
for i, cell in enumerate(notebook['cells']):
    source_lines = cell.get('source', [])
    source = ''.join(source_lines)
    
    # Look for the problematic lines
    if 'Injection efficiency' in source and ('ax7' in source or 'ax8' in source):
        print(f"=== CELL {i} ===")
        # Find the line with Injection efficiency
        for line in source_lines:
            if 'Injection efficiency' in line:
                print(f"Found: {repr(line)}")
    
    if 'Injection Loss (mA/s)' in source:
        print(f"=== CELL {i} - Injection Loss ===")
        for line in source_lines:
            if 'Injection Loss (mA/s)' in line:
                print(f"Found: {repr(line)}")
