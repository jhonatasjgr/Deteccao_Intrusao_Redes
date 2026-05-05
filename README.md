# Detecção de Intrusão em Redes com CICIDS2017 e XAI

Este artefato acompanha o artigo sobre classificação multiclasse de tráfego de rede para detecção de intrusões com o benchmark CICIDS2017. O pipeline implementado inclui limpeza e transformação de dados, agrupamento de classes, balanceamento por SMOTE, treinamento comparativo de modelos supervisionados e análise de explicabilidade com SHAP. O objetivo é reproduzir as principais evidências experimentais do artigo, com foco em métricas de desempenho (especialmente acurácia e recall), estabilidade de execução e interpretabilidade.

## Estrutura do README

Este README segue os requisitos mínimos da avaliação de artefatos do SBRC e está organizado nas seções:

1. Selos Considerados
2. Informações Básicas
3. Dependências
4. Preocupações com Segurança
5. Instalação
6. Teste Mínimo
7. Experimentos
8. LICENSE

Mapeamento previsto dos artefatos:

- `data/CICIDS2017/`: arquivos CSV do benchmark (extraídos do arquivo ZIP)
- `notebooks/deteccao_intrusao_rede.ipynb`: notebook principal com pipeline completo
- `results/catboost_info/`: logs e metadados de execução
- `figures/imagens_artigo/`: figuras do artigo
- `APPENDICE_HOTCRP.md`: documento de apêndice para submissão
- `scripts/`: utilitários de validação, organização, automação e smoke test

# Selos Considerados

Os selos considerados para avaliação são:

- Disponível (D)
- Funcional (F)
- Sustentável (S)
- Reproduzível (R)

# Informações Básicas

## Ambiente de Execução Recomendado

- **Sistema Operacional**: 
  - Windows: 10 ou 11 (PowerShell 5.1 ou superior)
  - Linux: Ubuntu 20.04 LTS, Ubuntu 22.04 LTS, ou Debian 11+
  - macOS: 10.14 ou superior

- **Python**: 3.10 ou 3.11
- **CPU**: 4 núcleos ou mais
- **RAM**: 16 GB recomendado (mínimo prático: 8 GB)
- **Disco**: 20 GB livres
- **Tempo de Execução Completo**: 4-8 horas

## Componentes Principais

- **Notebook de Referência**: `notebooks/deteccao_intrusao_rede.ipynb`
- **Dataset**: CICIDS2017 em `data/CICIDS2017/`
- **Resultados Visuais**: figuras em `figures/imagens_artigo/`
- **Apêndice**: `APPENDICE_HOTCRP.md`

# Dependências

As dependências estão listadas em `requirements.txt` e foram derivadas dos imports do notebook.

## Principais Bibliotecas com Versões

```
numpy>=1.24,<2.1
pandas>=2.0,<2.3
scikit-learn>=1.4,<1.7
imbalanced-learn>=0.12,<0.14
matplotlib>=3.8,<3.11
seaborn>=0.13,<0.14
xgboost>=2.0,<2.2
lightgbm>=4.3,<4.7
catboost>=1.2,<1.3
shap>=0.45,<0.48
jupyter>=1.0,<2.0
notebook>=7.0,<8.0
nbformat>=5.10,<6.0
```

## Dados Externos (Benchmark)

O experimento depende dos 8 CSVs do CICIDS2017 extraídos em caminho relativo `data/CICIDS2017/`:

```
Monday-WorkingHours.pcap_ISCX.csv
Tuesday-WorkingHours.pcap_ISCX.csv
Wednesday-workingHours.pcap_ISCX.csv
Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
Friday-WorkingHours-Morning.pcap_ISCX.csv
Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
```

**Nota**: Os arquivos estão disponíveis em http://205.174.165.80/CICDataset/CICIDs2017/Dataset/ 
Os CSVs geralmente vêm compactados em formato `.zip` e precisam ser extraídos antes de serem colocados em `data/CICIDS2017/`.

# Preocupações com Segurança

Este artefato não exige credenciais, não abre portas de rede, não realiza varredura ativa e não modifica configurações sensíveis do sistema. A execução é offline sobre arquivos CSV.

**Risco Operacional Esperado**: Uso elevado de memória e CPU durante SMOTE e treinamento. Recomenda-se execução em ambiente isolado (venv/conda), com monitoramento de recursos.

# Instalação

## Pré-requisitos

- Git instalado
- Python 3.10 ou 3.11 instalado
- Pip atualizado

## 1) Clonar o Repositório

```bash
git clone https://github.com/jhonatasjgr/Deteccao_Intrusao_Redes
cd Deteccao_Intrusao_Redes
```

## 2) Criar e Ativar Ambiente Virtual

### Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Preparar Dataset

Os arquivos CSV do CICIDS2017 devem ser colocados em `data/CICIDS2017/`.

**Passos para preparar o dataset:**

1. Baixe os CSVs do CICIDS2017 de: http://205.174.165.80/CICDataset/CICIDs2017/Dataset/
2. Extraia os arquivos se vierem em formato ZIP:
   ```bash
   # Linux/macOS
   unzip CICIDS2017.zip -d data/CICIDS2017/
   
   # Windows (PowerShell)
   Expand-Archive -Path CICIDS2017.zip -DestinationPath data/CICIDS2017/
   ```
3. Verifique se todos os 8 CSVs estão em `data/CICIDS2017/`

## 4) Executar Teste de Validação (Opcional)

```bash
python scripts/validate_artifact.py
```

Saída esperada:
```
VALIDACAO_OK
Artefato pronto para avaliação mínima (dependências e entradas encontradas).
```

## 5) Abrir Notebook para Execução Interativa

Para explorar e executar o notebook de forma interativa no Jupyter:

```bash
jupyter notebook notebooks/deteccao_intrusao_rede.ipynb
```

**Alternativa (recomendada para reprodução automatizada)**: Use o script Python:

```bash
python scripts/run_pipeline.py
```

# Teste Mínimo

## Objetivo

Validar rapidamente se o ambiente está funcional para revisão do artefato.

## Passo 1: Validação Estrutural

```bash
python scripts/validate_artifact.py
```

Saída esperada:

```
VALIDACAO_OK
Artefato pronto para avaliação mínima (dependências e entradas encontradas).
```

## Passo 2: Smoke Test Rápido no Notebook

```bash
python scripts/smoke_test_notebook.py
```

Saída esperada:

```
SMOKE_TEST_OK
Células iniciais de setup/import do notebook executaram com sucesso.
```

## Passo 3: Executar Pipeline Completo (Opcional)

Para reproduzir todos os experimentos com automação completa:

```bash
python scripts/run_pipeline.py --help
```

# Experimentos

## Reivindicação #1: Avaliação Comparativa de Modelos

O notebook implementa treinamento e avaliação de seis algoritmos de ML:

1. Random Forest
2. XGBoost
3. LightGBM
4. CatBoost
5. Redes Neurais (conforme artigo)
6. Modelo adicional (conforme artigo)

**Métrica Principal**: Acurácia e tempo de inferência

**Resultado Esperado**: CatBoost oferece melhor trade-off entre precisão e velocidade (~99.42% acurácia, 0.65s de inferência).

**Como Reproduzir via Notebook**:

1. Abra `notebooks/deteccao_intrusao_rede.ipynb`
2. Execute célula por célula até a seção de "Comparação de Modelos"
3. Localize a tabela final de resultados (df_resultados) com as métricas por modelo
4. Confirme o valor da coluna Acurácia do modelo campeão

**Evidências Relacionadas**:

- `figures/imagens_artigo/radar_comparacao_modelos.pdf`
- `figures/imagens_artigo/curva_de_aprendizado_*.pdf`

## Reivindicação #2: Explicabilidade com SHAP

O notebook aplica SHAP (SHapley Additive exPlanations) para interpretar decisões dos modelos:

- Importância global de features
- Dependência parcial
- Análise local de predições

**Resultado Esperado**: Identificação clara das features mais relevantes para detecção de intrusões.

**Como Reproduzir via Notebook**:

1. Execute as seções iniciais de preparação de dados
2. Procure pela seção "Análise de Explicabilidade com SHAP"
3. Execute as células de análise SHAP
4. Inspecione os gráficos gerados com dependência parcial e importância

**Evidências Relacionadas**:

- `figures/imagens_artigo/shap_*.pdf`
- `figures/imagens_artigo/dependencia_parcial_*.pdf`

## Execução do Pipeline Completo

### Via Notebook Interativo (Modo Manual):

1. Abra `notebooks/deteccao_intrusao_rede.ipynb` em Jupyter
2. Execute célula por célula (Shift+Enter no Jupyter)
3. Siga os comentários e documentação inline

### Via Script Automatizado (Recomendado):

```bash
python scripts/run_pipeline.py --full
```

O script:
- Carrega automaticamente os dados
- Executa todas as etapas do pipeline
- Gera resultados em `results/`
- Exibe progresso durante execução
- Salva visualizações em `figures/`

**Tempo Esperado**: 4-8 horas (variável conforme hardware)

## Reprodução Esperada de Resultados

Ao executar o pipeline, você deverá obter resultados similares aos reportados no artigo:

| Modelo      | Acurácia | Tempo (s) |
|-------------|----------|-----------|
| Random Forest | ~0.9964  | ~2.5      |
| XGBoost     | ~0.9958  | ~1.2      |
| LightGBM    | ~0.9956  | ~0.8      |
| CatBoost    | ~0.9942  | ~0.65     |

**Nota**: Pequenas variações (±0.01%) são esperadas devido a diferenças de hardware e versões de bibliotecas.
# Arquivos Importantes

```
Deteccao_Intrusao_Redes/
├── README.md                              # Este arquivo
├── APPENDICE_HOTCRP.md                    # Apêndice do artigo
├── LICENSE                                # Licença
├── requirements.txt                       # Dependências Python
│
├── notebooks/
│   └── deteccao_intrusao_rede.ipynb      # Notebook principal
│
├── scripts/
│   ├── validate_artifact.py              # Validação estrutural
│   ├── smoke_test_notebook.py            # Teste rápido
│   └── run_pipeline.py                   # Automação completa
│
├── data/
│   └── CICIDS2017/                       # CSVs do benchmark (não inclusos)
│
├── results/
│   └── catboost_info/                    # Logs e metadados
│
└── figures/
    └── imagens_artigo/                   # Visualizações
```

## Resolução de Problemas

### Erro: "ModuleNotFoundError: No module named 'sklearn'"

**Solução**: Ative o ambiente virtual e reinstale dependências:
```bash
source .venv/bin/activate  # Linux/macOS
# ou
.\.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### Erro: "FileNotFoundError: data/CICIDS2017/Monday-WorkingHours..."

**Solução**: Verifique se os CSVs estão em `data/CICIDS2017/`. Se estão em ZIP, extraia:
```bash
unzip CICIDS2017.zip -d data/CICIDS2017/  # Linux/macOS
# ou
Expand-Archive -Path CICIDS2017.zip -DestinationPath data/CICIDS2017/  # Windows
```

### Erro: "MemoryError" durante SMOTE

**Solução**: Aumente a RAM disponível ou reduza o tamanho da amostra editando o notebook.

### Erro: "No such file or directory: scripts/organizar_artefato.ps1"

**Solução**: Este script foi refatorado. Use `python scripts/run_pipeline.py` em seu lugar.

## Referências

- CICIDS2017 Dataset: https://www.unb.ca/cic/datasets/ids-2017.html
- SHAP: https://github.com/slundberg/shap
- Scikit-learn: https://scikit-learn.org/
- CatBoost: https://catboost.ai/
- XGBoost: https://xgboost.readthedocs.io/
- Imbalanced-learn: https://imbalanced-learn.org/

## Autores

J. Gomes Ribeiro, I. Bezerra Reis, J. Cavalcante Lacerda Junior

---

**Versão**: 2.0  
**Última Atualização**: 2026
# LICENSE

Este artefato e distribuido sob a licenca MIT. Consulte o arquivo LICENSE.
