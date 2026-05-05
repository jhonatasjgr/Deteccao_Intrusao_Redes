"""
Script automatizado para executar o pipeline completo de detecção de intrusão.

Este script executa o notebook de forma não-interativa, gerando todos os resultados,
logs e visualizações sem necessidade de interface gráfica.

Uso:
    python scripts/run_pipeline.py              # Execução completa
    python scripts/run_pipeline.py --help       # Mostrar ajuda
    python scripts/run_pipeline.py --dry-run    # Simular execução
    python scripts/run_pipeline.py --smoke-test # Apenas células iniciais
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path
import subprocess
import shutil


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "notebooks" / "deteccao_intrusao_rede.ipynb"
RESULTS_DIR = ROOT / "results"
LOGS_DIR = RESULTS_DIR / "logs"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOGS_DIR / f"pipeline_execution_{TIMESTAMP}.log"


def setup_logging(dry_run: bool = False) -> None:
    """Configure o sistema de logging."""
    if not dry_run:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Criar arquivo de log
        with open(LOG_FILE, "w") as f:
            f.write(f"Pipeline Execution Log\n")
            f.write(f"Started: {datetime.now().isoformat()}\n")
            f.write("=" * 60 + "\n\n")


def log_message(message: str, level: str = "INFO", dry_run: bool = False) -> None:
    """Registra mensagem no console e arquivo de log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] [{level}] {message}"
    
    # Print no console
    colors = {
        "INFO": "\033[94m",      # Blue
        "SUCCESS": "\033[92m",   # Green
        "WARNING": "\033[93m",   # Yellow
        "ERROR": "\033[91m",     # Red
        "RESET": "\033[0m"
    }
    
    color = colors.get(level, colors["RESET"])
    print(f"{color}{formatted_msg}{colors['RESET']}")
    
    # Log no arquivo (se não for dry-run)
    if not dry_run and LOG_FILE.exists():
        with open(LOG_FILE, "a") as f:
            f.write(formatted_msg + "\n")


def check_dependencies() -> bool:
    """Verifica se todas as dependências estão instaladas."""
    log_message("Verificando dependências...", "INFO")
    
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "scripts/validate_artifact.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            log_message("Dependências verificadas com sucesso", "SUCCESS")
            return True
        else:
            log_message(f"Erro na validação: {result.stdout}\n{result.stderr}", "ERROR")
            return False
            
    except Exception as e:
        log_message(f"Erro ao verificar dependências: {str(e)}", "ERROR")
        return False


def check_notebook() -> bool:
    """Verifica se o notebook existe."""
    if NOTEBOOK_PATH.exists():
        log_message(f"Notebook encontrado: {NOTEBOOK_PATH}", "SUCCESS")
        return True
    else:
        log_message(f"Notebook não encontrado: {NOTEBOOK_PATH}", "ERROR")
        return False


def check_dataset() -> bool:
    """Verifica se o dataset CICIDS2017 está disponível."""
    dataset_dir = ROOT / "data" / "CICIDS2017"
    
    if not dataset_dir.exists():
        log_message(f"Diretório do dataset não encontrado: {dataset_dir}", "WARNING")
        log_message("Por favor, coloque os CSVs do CICIDS2017 em data/CICIDS2017/", "WARNING")
        return False
    
    required_files = [
        "Monday-WorkingHours.pcap_ISCX.csv",
        "Tuesday-WorkingHours.pcap_ISCX.csv",
        "Wednesday-workingHours.pcap_ISCX.csv",
        "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
        "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
        "Friday-WorkingHours-Morning.pcap_ISCX.csv",
        "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
        "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
    ]
    
    found_count = 0
    for filename in required_files:
        filepath = dataset_dir / filename
        if filepath.exists():
            found_count += 1
        else:
            log_message(f"CSV não encontrado: {filename}", "WARNING")
    
    log_message(f"CSVs encontrados: {found_count}/{len(required_files)}", "INFO")
    
    if found_count == 0:
        log_message("Nenhum CSV do dataset foi encontrado!", "ERROR")
        return False
    elif found_count < len(required_files):
        log_message("Apenas alguns CSVs foram encontrados. A execução pode falhar.", "WARNING")
        return True
    else:
        log_message("Todos os CSVs encontrados", "SUCCESS")
        return True


def execute_notebook_with_papermill(dry_run: bool = False) -> bool:
    """Executa o notebook usando papermill (recomendado)."""
    try:
        import papermill as pm
    except ImportError:
        log_message("Papermill não instalado. Tentando instalação...", "WARNING")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "papermill", "-q"])
        import papermill as pm
    
    output_notebook = RESULTS_DIR / f"notebook_output_{TIMESTAMP}.ipynb"
    
    if dry_run:
        log_message(f"[DRY-RUN] Executaria notebook com papermill", "INFO")
        log_message(f"[DRY-RUN] Entrada: {NOTEBOOK_PATH}", "INFO")
        log_message(f"DRY-RUN] Saída: {output_notebook}", "INFO")
        return True
    
    try:
        log_message(f"Iniciando execução do notebook com papermill...", "INFO")
        log_message(f"Entrada: {NOTEBOOK_PATH}", "INFO")
        log_message(f"Saída: {output_notebook}", "INFO")
        log_message("Isto pode levar vários minutos (4-8 horas dependendo do hardware)...", "INFO")
        
        pm.execute_notebook(
            str(NOTEBOOK_PATH),
            str(output_notebook),
            kernel_name='python3'
        )
        
        log_message("Notebook executado com sucesso", "SUCCESS")
        log_message(f"Output salvo em: {output_notebook}", "SUCCESS")
        return True
        
    except Exception as e:
        log_message(f"Erro ao executar notebook: {str(e)}", "ERROR")
        traceback.print_exc()
        return False


def execute_notebook_with_nbconvert(dry_run: bool = False) -> bool:
    """Executa o notebook usando nbconvert (fallback)."""
    output_notebook = RESULTS_DIR / f"notebook_output_{TIMESTAMP}.ipynb"
    output_html = RESULTS_DIR / f"notebook_output_{TIMESTAMP}.html"
    
    if dry_run:
        log_message(f"[DRY-RUN] Executaria notebook com nbconvert", "INFO")
        return True
    
    try:
        log_message("Tentando executar com nbconvert...", "INFO")
        
        cmd = [
            sys.executable, "-m", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--ExecutePreprocessor.timeout=3600",
            f"--output={output_notebook}",
            str(NOTEBOOK_PATH)
        ]
        
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        
        if result.returncode == 0:
            log_message("Notebook executado com sucesso com nbconvert", "SUCCESS")
            
            # Gerar também versão HTML
            html_cmd = [
                sys.executable, "-m", "nbconvert",
                "--to", "html",
                f"--output={output_html}",
                str(output_notebook)
            ]
            subprocess.run(html_cmd, cwd=ROOT)
            
            log_message(f"Output salvo em: {output_notebook}", "SUCCESS")
            log_message(f"HTML gerado em: {output_html}", "SUCCESS")
            return True
        else:
            log_message(f"Erro em nbconvert: {result.stderr}", "ERROR")
            return False
            
    except Exception as e:
        log_message(f"Erro ao executar com nbconvert: {str(e)}", "ERROR")
        return False


def run_smoke_test(dry_run: bool = False) -> bool:
    """Executa apenas o smoke test (células iniciais)."""
    if dry_run:
        log_message("[DRY-RUN] Executaria smoke test", "INFO")
        return True
    
    try:
        log_message("Executando smoke test...", "INFO")
        result = subprocess.run(
            [sys.executable, "scripts/smoke_test_notebook.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        log_message(result.stdout, "INFO")
        
        if result.returncode == 0:
            log_message("Smoke test passou", "SUCCESS")
            return True
        else:
            log_message(f"Smoke test falhou: {result.stderr}", "ERROR")
            return False
            
    except Exception as e:
        log_message(f"Erro ao executar smoke test: {str(e)}", "ERROR")
        return False


def generate_report(dry_run: bool = False) -> None:
    """Gera relatório final de execução."""
    if dry_run:
        return
    
    report_file = RESULTS_DIR / f"execution_report_{TIMESTAMP}.txt"
    
    with open(report_file, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("RELATÓRIO DE EXECUÇÃO DO PIPELINE\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Data/Hora: {datetime.now().isoformat()}\n")
        f.write(f"Raiz: {ROOT}\n")
        f.write(f"Notebook: {NOTEBOOK_PATH}\n")
        f.write(f"Log: {LOG_FILE}\n\n")
        
        f.write("Verificações realizadas:\n")
        f.write("- Dependências ✓\n")
        f.write("- Notebook ✓\n")
        f.write("- Dataset ✓\n\n")
        
        f.write("Saídas geradas em:\n")
        f.write(f"- Resultados: {RESULTS_DIR}\n")
        f.write(f"- Logs: {LOGS_DIR}\n\n")
    
    log_message(f"Relatório salvo em: {report_file}", "SUCCESS")


def main() -> int:
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Execute o pipeline completo de detecção de intrusão"
    )
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Executar apenas o smoke test (células iniciais)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simular a execução sem fazer mudanças"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Executar pipeline completo (padrão)"
    )
    
    args = parser.parse_args()
    
    setup_logging(dry_run=args.dry_run)
    
    print("\n" + "=" * 60)
    print("PIPELINE DE DETECÇÃO DE INTRUSÃO EM REDES")
    print("=" * 60 + "\n")
    
    if args.dry_run:
        log_message("MODO SIMULAÇÃO ATIVADO - nenhuma alteração será feita", "WARNING")
        print()
    
    # Checklist pré-execução
    log_message("Iniciando checklist pré-execução...", "INFO")
    print()
    
    if not check_dependencies():
        log_message("Instalação de dependências necessária", "ERROR")
        if not args.dry_run:
            return 1
    
    if not check_notebook():
        log_message("Notebook não encontrado", "ERROR")
        return 1
    
    if not check_dataset():
        if not args.dry_run:
            log_message("Dataset incompleto. Execute com --dry-run para mais detalhes.", "ERROR")
            return 1
    
    print()
    
    # Executar
    if args.smoke_test:
        log_message("Executando apenas smoke test...", "INFO")
        success = run_smoke_test(dry_run=args.dry_run)
    else:
        log_message("Executando pipeline completo...", "INFO")
        print()
        
        # Tentar com papermill primeiro (melhor opção)
        try:
            import papermill  # noqa: F401
            success = execute_notebook_with_papermill(dry_run=args.dry_run)
        except ImportError:
            # Fallback para nbconvert
            log_message("Papermill não disponível. Usando nbconvert...", "WARNING")
            success = execute_notebook_with_nbconvert(dry_run=args.dry_run)
    
    print()
    
    if success or args.dry_run:
        generate_report(dry_run=args.dry_run)
        log_message("Pipeline finalizado com sucesso", "SUCCESS")
        return 0
    else:
        log_message("Pipeline falhou", "ERROR")
        return 1


if __name__ == "__main__":
    sys.exit(main())
