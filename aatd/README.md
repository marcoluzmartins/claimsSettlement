# AATD: previsão de produtos em promoção

Trabalho de Algoritmos de Apoio à Tomada de Decisão (FEP, 2026/27). Prever `y=1` (produto com desconto); métrica: accuracy.

| Ficheiro | Conteúdo | Capítulos do relatório |
|---|---|---|
| `01_EDA_Preparacao.ipynb` | Exploração dos dados e decisões de preparação | Business understanding, Data understanding, Data preparation |
| `02_Modelacao_Avaliacao.ipynb` | Modelos, comparação e submissão (a fazer) | Modelling, Evaluation, Results |
| `eda_graficos.py` | Script que lê um CSV e cria os gráficos e tabelas de EDA | Data understanding |

Para correr: `pip install -r requirements.txt`, colocar `training.csv` e `task.csv` em `data/` (a pasta não vai para o Git) e executar os notebooks por ordem.
O Notebook 1 grava em `outputs/` as figuras, as tabelas e os folds usados pelo Notebook 2.

## Script de gráficos

```bash
python eda_graficos.py data/training.csv
python eda_graficos.py data/task.csv
```

Cria os gráficos em `graficos/<nome do ficheiro>/`. Usa só `pandas` e `matplotlib`. Com o `training.csv` cria 9 gráficos; com o `task.csv`, onde o `y` está vazio, salta os que dependem do `y` e cria 5.
