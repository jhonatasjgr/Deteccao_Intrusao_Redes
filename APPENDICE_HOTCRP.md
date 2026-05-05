# Apêndice - Detecção de Intrusão em Redes com CICIDS2017 e XAI

## Informações do Artefato

Este documento serve como apêndice complementar ao artigo submetido, fornecendo detalhes técnicos adicionais sobre a implementação, dados experimentais e resultados.

### Identificação do Artefato

- **Título do Artigo**: Detecção de Intrusão em Redes com CICIDS2017 e XAI
- **Tipo**: Software e Dados
- **Linguagem**: Python 3.10+
- **Data de Submissão**: 2026
- **Repositório**: https://github.com/jhonatasjgr/Deteccao_Intrusao_Redes

## Componentes Principais

### 1. Dataset

- **Nome**: CICIDS2017 (Canadian Institute for Cybersecurity Intrusion Detection System)
- **Formato**: CSV (Comma-Separated Values)
- **Arquivos**: 8 CSVs, um por dia de coleta
- **Tamanho Total**: ~1-2 GB (dependendo da compressão)
- **Atributos**: 78 características de fluxo de rede

### 2. Modelos Avaliados

Os seguintes algoritmos de aprendizado de máquina foram avaliados:

1. **Random Forest** - Modelo de ensemble baseado em árvores
2. **XGBoost** - Gradient Boosting otimizado
3. **LightGBM** - Gradient Boosting leve
4. **CatBoost** - Gradient Boosting para dados categóricos
5. **Redes Neurais** (se aplicável) - Modelos deep learning
6. **Outros** - Conforme especificado no artigo

### 3. Técnicas de Explicabilidade (XAI)

- **SHAP** (SHapley Additive exPlanations)
  - Valores SHAP para importância global de features
  - Dependência parcial de variáveis críticas
  - Análise local de decisões

### 4. Métricas de Avaliação

- **Acurácia**: Taxa geral de classificação correta
- **Precisão**: Taxa de verdadeiros positivos entre predições positivas
- **Recall**: Taxa de detecção de instâncias positivas
- **F1-Score**: Média harmônica entre precisão e recall
- **Tempo de Inferência**: Latência por amostra

## Reprodução dos Resultados

### Ambiente Recomendado

- **Python**: 3.10 ou 3.11
- **RAM**: Mínimo 8GB, recomendado 16GB
- **Tempo de Execução**: 4-8 horas para pipeline completo

### Passos Principais de Execução

1. **Preparação de Dados**
   - Carregamento dos CSVs
   - Limpeza e tratamento de valores ausentes
   - Transformação de atributos

2. **Engenharia de Features**
   - Normalização
   - Seleção de features relevantes
   - Agregação de classes

3. **Balanceamento de Classes**
   - SMOTE (Synthetic Minority Over-sampling Technique)

4. **Treinamento e Avaliação**
   - Divisão treino/teste
   - Treinamento de modelos
   - Validação cruzada

5. **Explicabilidade**
   - Análise SHAP
   - Visualizações de importância

## Principais Descobertas

### Trade-off Precisão vs. Velocidade

- **Random Forest**: 99.64% acurácia, mas inferência lenta
- **CatBoost**: 99.42% acurácia, inferência 3.4x mais rápida
- Discussão: CatBoost oferece melhor relação para defesa em tempo real

### Fatores Críticos de Decisão

As top-5 features mais importantes para detecção:
1. [Feature conforme experimento]
2. [Feature conforme experimento]
3. [Feature conforme experimento]
4. [Feature conforme experimento]
5. [Feature conforme experimento]

(Detalhes específicos disponíveis no notebook)

## Arquivos Importantes

```
.
├── deteccao_intrusao_rede.ipynb       # Notebook principal com pipeline completo
├── notebooks/
│   └── deteccao_intrusao_rede.ipynb   # Referência duplicada
├── data/
│   └── CICIDS2017/                    # CSVs do benchmark
├── scripts/
│   ├── run_pipeline.py                # Execução automatizada
│   ├── validate_artifact.py           # Validação estrutural
│   └── smoke_test_notebook.py         # Teste rápido
├── results/                           # Logs e metadados
├── figures/                           # Visualizações
└── requirements.txt                   # Dependências Python
```

## Notas Técnicas

### Limitações Conhecidas

1. Requisitos computacionais elevados para dataset completo
2. Tempo de treinamento varia conforme hardware disponível
3. SMOTE pode gerar amostras sintéticas que aumentam a memória

### Recomendações de Uso

1. Use a versão com script Python (`run_pipeline.py`) para reprodução automatizada
2. Execute em ambiente virtual (venv ou conda)
3. Monitore uso de memória durante SMOTE
4. Use GPU se disponível para modelos com suporte CUDA

## Referências de Implementação

- CICIDS2017 Dataset: https://www.unb.ca/cic/datasets/ids-2017.html
- SHAP Documentation: https://shap.readthedocs.io/
- Scikit-learn: https://scikit-learn.org/
- CatBoost: https://catboost.ai/
- XGBoost: https://xgboost.readthedocs.io/

## Contato e Suporte

Para dúvidas ou problemas na execução do artefato, consulte:
- Repositório: https://github.com/jhonatasjgr/Deteccao_Intrusao_Redes
- Issues no GitHub
- Documentação no README.md

---

**Versão do Apêndice**: 1.0  
**Data**: 2026
