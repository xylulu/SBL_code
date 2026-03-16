import json

# Read the notebook
notebook_path = "/Users/xylu/Desktop/Data/code/Acoustic_csv_plotting_V6_LossMonitor_StoredInj.ipynb"
with open(notebook_path, 'r') as f:
    notebook = json.load(f)

# Find and fix the syntax errors in cell 6
fixed = False
for i, cell in enumerate(notebook['cells']):
    source_lines = cell.get('source', [])
    source = ''.join(source_lines)
    
    # Look for syntax errors in lines with extra parentheses
    has_error = False
    if 'fontweight="bold"))' in source:  # Extra paren
        print(f"Found syntax error in cell {i}: extra parenthesis detected")
        # Fix all instances of double closing parens
        source = source.replace(
            'fontweight="bold"))',
            'fontweight="bold")'
        )
        has_error = True
    
    if 'ax9.set_ylabel("Injection Loss' in source:
        print(f"Found axis error in cell {i}: ax9 should be ax8")
        source = source.replace(
            'ax9.set_ylabel("Injection Loss (mA/s)", fontsize=14, fontweight="bold")',
            'ax8.set_ylabel("Injection Loss (mA/s)", fontsize=14, fontweight="bold")'
        )
        has_error = True
    
    if 'ax8.set_ylabel("Injection efficiency' in source:
        print(f"Found axis error in cell {i}: ax8 should be ax7 for efficiency")
        source = source.replace(
            'ax8.set_ylabel("Injection efficiency (%)", fontsize=14, fontweight="bold")',
            'ax7.set_ylabel("Injection efficiency (%)", fontsize=14, fontweight="bold")'
        )
        has_error = True
    
    if has_error:
        cell['source'] = [source]
        print(f"✓ Fixed cell {i}")
        fixed = True

if fixed:
    # Write back
    with open(notebook_path, 'w') as f:
        json.dump(notebook, f, indent=1)
    print("✓ Notebook updated successfully")
else:
    print("✗ Could not find errors to fix")
