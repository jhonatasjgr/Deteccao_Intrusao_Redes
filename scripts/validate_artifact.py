from __future__ import annotations

import importlib
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NEW_DATASET_DIR = ROOT / "data" / "CICIDS2017"
LEGACY_DATASET_DIR = ROOT / "CICIDS2017"


def resolve_dataset_dir() -> Path:
    if NEW_DATASET_DIR.exists():
        return NEW_DATASET_DIR
    return LEGACY_DATASET_DIR


DATASET_DIR = resolve_dataset_dir()


REQUIRED_REPO_FILES = [
    ROOT / "README.md",
    ROOT / "requirements.txt",
    ROOT / "LICENSE",
]


NOTEBOOK_CANDIDATES = [
    ROOT / "notebooks" / "deteccao_intrusao_rede.ipynb",
    ROOT / "deteccao_intrusao_rede.ipynb",
]


DOC_CANDIDATES = [
    ROOT / "docs" / "APPENDICE_HOTCRP.md",
    ROOT / "APPENDICE_HOTCRP.md",
]


def exists_any(paths: list[Path]) -> bool:
    return any(path.exists() for path in paths)


REQUIRED_OPTIONAL_GROUPS = {
    "Notebook principal": NOTEBOOK_CANDIDATES,
    "Documento de apendice": DOC_CANDIDATES,
}


REQUIRED_DATASET_FILES = [
    "Monday-WorkingHours.pcap_ISCX.csv",
    "Tuesday-WorkingHours.pcap_ISCX.csv",
    "Wednesday-workingHours.pcap_ISCX.csv",
    "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
    "Friday-WorkingHours-Morning.pcap_ISCX.csv",
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
]


REQUIRED_MODULES = [
    "numpy",
    "pandas",
    "sklearn",
    "imblearn",
    "matplotlib",
    "seaborn",
    "xgboost",
    "lightgbm",
    "catboost",
    "shap",
]


def check_files() -> list[str]:
    issues: list[str] = []

    for file_path in REQUIRED_REPO_FILES:
        if not file_path.exists():
            issues.append(f"Arquivo ausente no repositorio: {file_path}")

    for group_name, candidates in REQUIRED_OPTIONAL_GROUPS.items():
        if not exists_any(candidates):
            paths = ", ".join(str(path) for path in candidates)
            issues.append(f"{group_name} nao encontrado em nenhum caminho esperado: {paths}")

    if not DATASET_DIR.exists():
        issues.append(
            f"Diretorio de dataset nao encontrado: {DATASET_DIR} "
            "(esperado em data/CICIDS2017 ou CICIDS2017)"
        )
    else:
        for filename in REQUIRED_DATASET_FILES:
            path = DATASET_DIR / filename
            if not path.exists():
                issues.append(f"CSV ausente no dataset: {path}")

    return issues


def check_imports() -> list[str]:
    issues: list[str] = []
    for module_name in REQUIRED_MODULES:
        try:
            importlib.import_module(module_name)
        except Exception as exc:  # pragma: no cover
            issues.append(f"Falha ao importar modulo '{module_name}': {exc}")
    return issues


def main() -> int:
    print("Validando estrutura do artefato...\n")

    issues = []
    issues.extend(check_files())
    issues.extend(check_imports())

    if issues:
        print("VALIDACAO_FALHOU")
        print("Foram encontrados problemas:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("VALIDACAO_OK")
    print("Artefato pronto para avaliacao minima (dependencias e entradas encontradas).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
