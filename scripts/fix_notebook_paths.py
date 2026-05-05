"""
Script para corrigir caminhos relativos no notebook.
"""

import json
from pathlib import Path

notebook_path = Path("notebooks/deteccao_intrusao_rede.ipynb")

print("Carregando notebook...")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

changes_made = 0

# Corrigir caminhos nos código das células
for cell_idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    
    source_lines = cell['source']
    new_lines = []
    
    for line in source_lines:
        original_line = line
        
        # Correção 1: ../CICIDS2017/ -> ../data/CICIDS2017/
        if '../CICIDS2017/' in line:
            line = line.replace('../CICIDS2017/', '../data/CICIDS2017/')
            changes_made += 1
            print(f"Célula {cell_idx}: Corrigido caminho CICIDS2017")
        
        # Correção 2: imagens_artigo/ -> ../figures/imagens_artigo/
        if "os.makedirs('imagens_artigo')" in line:
            line = line.replace("'imagens_artigo'", "'../figures/imagens_artigo/'")
            changes_made += 1
            print(f"Célula {cell_idx}: Corrigido caminho imagens_artigo")
        
        if "os.path.exists('imagens_artigo')" in line:
            line = line.replace("'imagens_artigo'", "'../figures/imagens_artigo/'")
            changes_made += 1
            print(f"Célula {cell_idx}: Corrigido path check imagens_artigo")
        
        new_lines.append(line)
    
    cell['source'] = new_lines

print(f"\nTotal de correções feitas: {changes_made}")

print("Salvando notebook corrigido...")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook atualizado com sucesso!")
