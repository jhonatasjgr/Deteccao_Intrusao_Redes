from __future__ import annotations

import json
from pathlib import Path
import traceback


ROOT = Path(__file__).resolve().parents[1]

NOTEBOOK_CANDIDATES = [
    ROOT / "notebooks" / "deteccao_intrusao_rede.ipynb",
    ROOT / "deteccao_intrusao_rede.ipynb",
]


def resolve_notebook() -> Path:
    for path in NOTEBOOK_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Notebook principal nao encontrado. Caminhos tentados: "
        + ", ".join(str(p) for p in NOTEBOOK_CANDIDATES)
    )


def collect_startup_cells(nb_data: dict, max_cells: int = 4) -> list[str]:
    code_cells: list[str] = []
    for cell in nb_data.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        if "read_csv(" in source:
            break
        code_cells.append(source)
        if len(code_cells) >= max_cells:
            break
    return code_cells


def main() -> int:
    notebook_path = resolve_notebook()
    print(f"Notebook encontrado: {notebook_path}")

    data = json.loads(notebook_path.read_text(encoding="utf-8"))
    startup_cells = collect_startup_cells(data, max_cells=4)

    if not startup_cells:
        print("SMOKE_TEST_FALHOU")
        print("Nenhuma celula de setup encontrada para execucao rapida.")
        return 1

    global_ctx: dict = {"__name__": "__main__"}
    bootstrap = "import matplotlib\nmatplotlib.use('Agg')\n"

    try:
        exec(bootstrap, global_ctx)
        for i, src in enumerate(startup_cells, start=1):
            print(f"Executando celula de smoke test #{i}...")
            exec(src, global_ctx)
    except Exception:
        print("SMOKE_TEST_FALHOU")
        traceback.print_exc()
        return 1

    print("SMOKE_TEST_OK")
    print("Celulas iniciais de setup/import do notebook executaram com sucesso.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
