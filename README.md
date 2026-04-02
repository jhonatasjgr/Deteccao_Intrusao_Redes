# Deteccao de Intrusao em Redes com CICIDS2017 e XAI

Este artefato acompanha o artigo sobre classificacao multiclasse de trafego de rede para deteccao de intrusoes com o benchmark CICIDS2017. O pipeline implementado no notebook principal inclui limpeza e transformacao de dados, agrupamento de classes, balanceamento por SMOTE, treinamento comparativo de modelos supervisionados e analise de explicabilidade com SHAP. O objetivo e reproduzir as principais evidencias experimentais do artigo, com foco em metricas de desempenho (especialmente acuracia e recall), estabilidade de execucao e interpretabilidade.

# Estrutura do readme.md

Este README segue os requisitos minimos da avaliacao de artefatos do SBRC e esta organizado nas secoes:

1. Selos Considerados
2. Informacoes basicas
3. Dependencias
4. Preocupacoes com seguranca
5. Instalacao
6. Teste minimo
7. Experimentos
8. LICENSE


Mapeamento previsto dos artefatos:

- data/CICIDS2017/: arquivos CSV do benchmark.
- notebooks/deteccao_intrusao_rede.ipynb: notebook principal.
- results/catboost_info/: logs e metadados de execucao.
- figures/imagens_artigo/: figuras do artigo.
- docs/: documentos de submissao (apendice/checklist).
- scripts/: utilitarios de validacao, organizacao e smoke test.

# Selos Considerados

Os selos considerados para avaliacao sao:

- Disponivel (D)
- Funcional (F)
- Sustentavel (S)
- Reproduzivel (R)

# Informacoes basicas

## Ambiente de execucao recomendado

- Sistema operacional: Windows 10/11 ou Linux recente.
- Python: 3.10 ou 3.11.
- CPU: 4 nucleos ou mais.
- RAM recomendada: 16 GB (minimo pratico: 8 GB).
- Disco recomendado: 20 GB livres.

## Componentes principais

- Notebook de referencia: notebooks/deteccao_intrusao_rede.ipynb.
- Dataset: CICIDS2017 em data/CICIDS2017/.
- Resultados visuais: figuras em figures/imagens_artigo/.

# Dependencias

As dependencias estao listadas em requirements.txt e foram derivadas dos imports do notebook.

Principais bibliotecas:

- numpy
- pandas
- scikit-learn
- imbalanced-learn
- matplotlib
- seaborn
- xgboost
- lightgbm
- catboost
- shap
- jupyter/notebook

## Dados externos (benchmark)

O experimento depende dos 8 CSVs do CICIDS2017 em caminho relativo:

- data/CICIDS2017/Monday-WorkingHours.pcap_ISCX.csv
- data/CICIDS2017/Tuesday-WorkingHours.pcap_ISCX.csv
- data/CICIDS2017/Wednesday-workingHours.pcap_ISCX.csv
- data/CICIDS2017/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
- data/CICIDS2017/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
- data/CICIDS2017/Friday-WorkingHours-Morning.pcap_ISCX.csv
- data/CICIDS2017/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
- data/CICIDS2017/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv

# Preocupacoes com seguranca

Este artefato nao exige credenciais, nao abre portas de rede, nao realiza varredura ativa e nao modifica configuracoes sensiveis do sistema. A execucao e offline sobre arquivos CSV.

Risco operacional esperado: uso elevado de memoria e CPU durante SMOTE e treinamento. Recomenda-se execucao em ambiente isolado (venv/conda), com monitoramento de recursos.

# Instalacao

## 1) Criar e ativar ambiente virtual

Windows (PowerShell):

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

## 2) Organizar estrutura recomendada

Executar o script de organizacao (Windows):

powershell -ExecutionPolicy Bypass -File scripts/organizar_artefato.ps1

Opcional (simulacao sem alterar arquivos):

powershell -ExecutionPolicy Bypass -File scripts/organizar_artefato.ps1 -DryRun

## 3) Posicionar dataset no caminho relativo correto

Colocar os CSVs em:

data/CICIDS2017/

## 4) Abrir notebook

jupyter notebook

Abrir e executar em ordem:

notebooks/deteccao_intrusao_rede.ipynb

# Teste minimo

Objetivo: validar rapidamente se o ambiente esta funcional para revisao do artefato.

## Passo 1: Validacao estrutural

python scripts/validate_artifact.py

Saida esperada:

VALIDACAO_OK

## Passo 2: Smoke test rapido no notebook

python scripts/smoke_test_notebook.py

Saida esperada:

SMOKE_TEST_OK

Esse teste executa apenas as celulas iniciais de setup/import do notebook (sem executar treino completo), sendo adequado para verificacao inicial do Selo Funcional.

# Experimentos

Esta secao descreve como reproduzir as principais reivindicacoes do artigo com caminhos relativos.

## Reivindicacao #1 (Acuracia)

Reivindicacao: o pipeline de classificacao multiclasse atinge alta acuracia na deteccao de ataques apos preprocessamento, selecao de features e balanceamento.

Como reproduzir:

1. Executar o notebook notebooks/deteccao_intrusao_rede.ipynb do inicio ate a etapa de comparacao de modelos.
2. Localizar a tabela final de resultados (df_resultados) com as metricas por modelo.
3. Confirmar o valor da coluna Acuracia do modelo campeao.

Evidencias relacionadas:

- figures/imagens_artigo/radar_comparacao_modelos.pdf
- figures/imagens_artigo/curva_de_aprendizado_Random Forest.pdf (ou modelo campeao)

## Reivindicacao #2 (Recall)

Reivindicacao: o pipeline mantem recall elevado entre as classes apos balanceamento por SMOTE.

Como reproduzir:

1. Executar o bloco de agrupamento de classes e o bloco de SMOTE no notebook.
2. Executar o treino e a avaliacao para gerar as metricas por modelo.
3. Confirmar o valor da coluna Recall na tabela de resultados e inspecionar matriz de confusao normalizada.

Evidencias relacionadas:

- figures/imagens_artigo/distribuicao_classes_ataque(apos_balanceamento_smote).pdf
- figures/imagens_artigo/matriz_confusao_normalizada_Random Forest.pdf (ou modelo campeao)

Observacao de tempo e recursos:

- Tempo total: pode variar de dezenas de minutos a horas, conforme hardware.
- Pico de memoria: ocorre principalmente no balanceamento SMOTE e em treinamento de modelos em paralelo.

# LICENSE

Este artefato e distribuido sob a licenca MIT. Consulte o arquivo LICENSE.
