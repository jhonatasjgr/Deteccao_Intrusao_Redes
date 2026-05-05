#!/bin/bash

#
# Script para organizar a estrutura recomendada do artefato CICIDS2017
#
# Uso:
#   ./organizar_artefato.sh          # Executa a organização completa
#   ./organizar_artefato.sh --dry-run # Simula as ações sem criar diretórios
#

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

DRY_RUN=false

if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# Função para escrever status
write_status() {
    local message="$1"
    local status="${2:-INFO}"
    local color="$NC"
    
    case $status in
        OK)
            color="$GREEN"
            ;;
        WARN)
            color="$YELLOW"
            ;;
        ERROR)
            color="$RED"
            ;;
    esac
    
    echo -e "${color}[${status}]${NC} $message"
}

# Obter diretório raiz
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

DIRS_TO_CREATE=(
    "data/CICIDS2017"
    "notebooks"
    "scripts"
    "results"
    "figures/imagens_artigo"
)

echo "================================"
echo "Organizador de Artefato CICIDS2017"
echo "================================"
echo ""

if [ "$DRY_RUN" = true ]; then
    write_status "MODO SIMULAÇÃO (--dry-run) ativado - nenhuma alteração será feita" "WARN"
    echo ""
fi

write_status "Raiz do repositório: $ROOT_DIR" "INFO"
echo ""

ALL_EXISTS=true

for dir in "${DIRS_TO_CREATE[@]}"; do
    full_path="$ROOT_DIR/$dir"
    
    if [ -d "$full_path" ]; then
        write_status "✓ Diretório já existe: $dir" "OK"
    else
        ALL_EXISTS=false
        if [ "$DRY_RUN" = true ]; then
            write_status "[SIMULAÇÃO] Criaria diretório: $dir" "WARN"
        else
            mkdir -p "$full_path"
            write_status "✓ Diretório criado: $dir" "OK"
        fi
    fi
done

echo ""

# Verificar arquivos essenciais
REQUIRED_FILES=(
    "README.md"
    "requirements.txt"
    "LICENSE"
    "APPENDICE_HOTCRP.md"
    "notebooks/deteccao_intrusao_rede.ipynb"
)

echo "Verificando arquivos essenciais:"
echo ""

FILES_OK=true
for file in "${REQUIRED_FILES[@]}"; do
    full_path="$ROOT_DIR/$file"
    
    if [ -f "$full_path" ]; then
        write_status "✓ Arquivo encontrado: $file" "OK"
    else
        FILES_OK=false
        write_status "✗ Arquivo não encontrado: $file" "ERROR"
    fi
done

echo ""

# Verificar dataset
DATASET_PATH="$ROOT_DIR/data/CICIDS2017"
CSV_FILES=(
    "Monday-WorkingHours.pcap_ISCX.csv"
    "Tuesday-WorkingHours.pcap_ISCX.csv"
    "Wednesday-workingHours.pcap_ISCX.csv"
    "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv"
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv"
    "Friday-WorkingHours-Morning.pcap_ISCX.csv"
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
)

echo "Verificando CSVs do dataset CICIDS2017 em: $DATASET_PATH"
echo ""

DATASET_OK=true
CSV_COUNT=0

if [ -d "$DATASET_PATH" ]; then
    for csv in "${CSV_FILES[@]}"; do
        csv_path="$DATASET_PATH/$csv"
        if [ -f "$csv_path" ]; then
            write_status "✓ CSV encontrado: $csv" "OK"
            ((CSV_COUNT++))
        else
            write_status "✗ CSV não encontrado: $csv" "WARN"
            DATASET_OK=false
        fi
    done
else
    write_status "Diretório $DATASET_PATH não existe. Crie-o e coloque os CSVs nele." "WARN"
    DATASET_OK=false
fi

echo ""
echo "================================"
echo "Resumo:"
echo "================================"

if [ "$ALL_EXISTS" = true ]; then
    echo "Diretórios: OK"
else
    echo "Diretórios: Criados/Faltantes"
fi

if [ "$FILES_OK" = true ]; then
    echo "Arquivos Essenciais: OK"
else
    echo "Arquivos Essenciais: Alguns faltam"
fi

echo "CSVs do Dataset: $CSV_COUNT/8 encontrados"

if [ "$CSV_COUNT" -eq 0 ]; then
    echo ""
    write_status "Próximo passo: Baixe os CSVs do CICIDS2017 e extraia em data/CICIDS2017/" "WARN"
    echo "URL: http://205.174.165.80/CICDataset/CICIDs2017/Dataset/"
fi

if [ "$DRY_RUN" = true ]; then
    echo ""
    write_status "Modo simulação - execute sem --dry-run para criar estrutura" "INFO"
fi

echo ""
