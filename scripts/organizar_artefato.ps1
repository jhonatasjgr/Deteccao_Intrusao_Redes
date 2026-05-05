#!/usr/bin/env powershell

<#
.SYNOPSIS
Script para organizar a estrutura recomendada do artefato CICIDS2017.

.DESCRIPTION
Este script cria os diretórios necessários para o artefato e verifica a estrutura.
Pode ser executado em modo simulação (DryRun) para verificar quais ações seriam realizadas.

.PARAMETER DryRun
Se definido, apenas simula as ações sem efetivamente criar diretórios.

.EXAMPLE
.\organizar_artefato.ps1
Executa a organização completa.

.\organizar_artefato.ps1 -DryRun
Simula as ações sem criar diretórios.
#>

param(
    [switch]$DryRun
)

# Cores para output
$greenColor = [System.ConsoleColor]::Green
$yellowColor = [System.ConsoleColor]::Yellow
$redColor = [System.ConsoleColor]::Red

function Write-Status {
    param([string]$message, [string]$status = "INFO")
    
    $color = switch ($status) {
        "OK" { $greenColor }
        "WARN" { $yellowColor }
        "ERROR" { $redColor }
        default { [System.ConsoleColor]::White }
    }
    
    Write-Host "[$status] " -ForegroundColor $color -NoNewline
    Write-Host $message
}

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$dirsToCreate = @(
    "data/CICIDS2017"
    "notebooks"
    "scripts"
    "results"
    "figures/imagens_artigo"
)

Write-Host "================================" 
Write-Host "Organizador de Artefato CICIDS2017"
Write-Host "================================`n"

if ($DryRun) {
    Write-Status "MODO SIMULAÇÃO (DryRun) ativado - nenhuma alteração será feita" "WARN"
    Write-Host ""
}

Write-Status "Raiz do repositório: $rootDir" "INFO"
Write-Host ""

$allExists = $true

foreach ($dir in $dirsToCreate) {
    $fullPath = Join-Path $rootDir $dir
    
    if (Test-Path $fullPath) {
        Write-Status "✓ Diretório já existe: $dir" "OK"
    } else {
        $allExists = $false
        if ($DryRun) {
            Write-Status "[SIMULAÇÃO] Criaria diretório: $dir" "WARN"
        } else {
            try {
                New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
                Write-Status "✓ Diretório criado: $dir" "OK"
            } catch {
                Write-Status "✗ Erro ao criar $dir : $_" "ERROR"
            }
        }
    }
}

Write-Host ""

# Verificar arquivos essenciais
$requiredFiles = @(
    "README.md"
    "requirements.txt"
    "LICENSE"
    "APPENDICE_HOTCRP.md"
    "notebooks/deteccao_intrusao_rede.ipynb"
)

Write-Host "Verificando arquivos essenciais:"
Write-Host ""

$filesOk = $true
foreach ($file in $requiredFiles) {
    $fullPath = Join-Path $rootDir $file
    
    if (Test-Path $fullPath) {
        Write-Status "✓ Arquivo encontrado: $file" "OK"
    } else {
        $filesOk = $false
        Write-Status "✗ Arquivo não encontrado: $file" "ERROR"
    }
}

Write-Host ""

# Verificar dataset
$datasetPath = Join-Path $rootDir "data/CICIDS2017"
$csvFiles = @(
    "Monday-WorkingHours.pcap_ISCX.csv"
    "Tuesday-WorkingHours.pcap_ISCX.csv"
    "Wednesday-workingHours.pcap_ISCX.csv"
    "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv"
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv"
    "Friday-WorkingHours-Morning.pcap_ISCX.csv"
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
)

Write-Host "Verificando CSVs do dataset CICIDS2017 em: $datasetPath"
Write-Host ""

$datasetOk = $true
$csvCount = 0

if (Test-Path $datasetPath) {
    foreach ($csv in $csvFiles) {
        $csvPath = Join-Path $datasetPath $csv
        if (Test-Path $csvPath) {
            Write-Status "✓ CSV encontrado: $csv" "OK"
            $csvCount++
        } else {
            Write-Status "✗ CSV não encontrado: $csv" "WARN"
            $datasetOk = $false
        }
    }
} else {
    Write-Status "Diretório $datasetPath não existe. Crie-o e coloque os CSVs nele." "WARN"
    $datasetOk = $false
}

Write-Host ""
Write-Host "================================" 
Write-Host "Resumo:"
Write-Host "================================"
Write-Host "Diretórios: $(if ($allExists) { 'OK' } else { 'Criados/Faltantes' })"
Write-Host "Arquivos Essenciais: $(if ($filesOk) { 'OK' } else { 'Alguns faltam' })"
Write-Host "CSVs do Dataset: $csvCount/8 encontrados"

if ($csvCount -eq 0) {
    Write-Host ""
    Write-Status "Próximo passo: Baixe os CSVs do CICIDS2017 e extraia em data/CICIDS2017/" "WARN"
    Write-Host "URL: http://205.174.165.80/CICDataset/CICIDs2017/Dataset/"
}

if ($DryRun) {
    Write-Host ""
    Write-Status "Modo simulação - execute sem -DryRun para criar estrutura" "INFO"
}

Write-Host ""
