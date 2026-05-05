import json
from pathlib import Path

notebook_path = Path("notebooks/deteccao_intrusao_rede.ipynb")
nb = json.load(open(notebook_path))

cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
print("Procurando por referências a dados e paths...\n")

found_count = 0
for i, cell in enumerate(cells):
    source = ''.join(cell['source'])
    if 'read_csv' in source or 'data/' in source or 'path' in source.lower():
        print(f"--- Célula {i} ---")
        print(source)
        print()
        found_count += 1
        if found_count >= 10:
            break
