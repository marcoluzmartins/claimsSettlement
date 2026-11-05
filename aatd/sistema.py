"""Sistema de previsão AATD: aprende com o ficheiro de treino e depois prevê qualquer ficheiro de teste.

Dois passos:

  1) TREINAR   python sistema.py treinar data/training.csv
     Lê o ficheiro de treino, prepara os dados, compara 7 modelos com cross-validation,
     escolhe o melhor (maior accuracy) e guarda-o em resultados/melhor_modelo.joblib.
     Também grava a tabela de comparação em resultados/comparacao_modelos.csv.

  2) PREVER    python sistema.py prever data/task.csv
     Carrega o modelo guardado, lê o ficheiro e grava resultados/submissao.csv (colunas i,y).
     Se o ficheiro de teste tiver o y preenchido, mostra também a accuracy, o recall, etc.

Opções úteis:
  --rapido   (treinar) não afina os hiperparâmetros: demora segundos em vez de minutos
  --modelo   (prever) caminho de outro modelo guardado
  --saida    (prever) caminho do CSV de saída

Também se pode usar dentro de Python:
    from sistema import treinar, prever
    treinar("data/training.csv")
    prever("data/task.csv")

Decisões de preparação (justificadas no Notebook 1): o identificador i é ignorado; os valores em falta
são preenchidos com a mediana do treino e ganham um indicador "estava em falta"; os outliers e as linhas
repetidas mantêm-se; as classes não são equilibradas; os modelos sensíveis à escala (KNN, MLP, Naive Bayes)
recebem as variáveis normalizadas. Tudo isto fica dentro do Pipeline, por isso é aprendido só com o treino.
"""
import argparse
import re
import time
import warnings
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import BaggingClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score, make_scorer, precision_score,
                             recall_score)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_validate
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")
SEMENTE = 42
PASTA = Path("resultados")


# ----------------------------------------------------------------------------- dados
def ler_dados(caminho, com_y=False):
    """Lê o CSV e devolve as colunas de entrada (d* e x*) e, se existir preenchido, o y."""
    df = pd.read_csv(caminho)
    entradas = [c for c in df.columns if re.fullmatch(r"d\d+", c)] + [c for c in df.columns if re.fullmatch(r"x\d+", c)]
    y = df["y"].astype(int) if "y" in df.columns and df["y"].notna().all() else None
    if com_y and y is None:
        raise SystemExit(f"O ficheiro {caminho} precisa da coluna y preenchida para treinar.")
    return df, entradas, y


# ----------------------------------------------------------------------------- modelos
def catalogo():
    """Os 7 modelos: (modelo, grelha de hiperparâmetros a testar, precisa de normalização?)."""
    return {
        "KNN": (KNeighborsClassifier(),
                {"modelo__n_neighbors": [3, 5, 11, 21], "modelo__weights": ["uniform", "distance"]}, True),
        "Decision Tree": (DecisionTreeClassifier(random_state=SEMENTE),
                          {"modelo__max_depth": [None, 10, 15], "modelo__min_samples_leaf": [1, 2, 5]}, False),
        "Naive Bayes": (GaussianNB(),
                        {"modelo__var_smoothing": [1e-9, 1e-6, 1e-3]}, True),
        "MLP": (MLPClassifier(max_iter=600, random_state=SEMENTE),
                {"modelo__hidden_layer_sizes": [(64,), (64, 32), (128, 64)], "modelo__alpha": [1e-4, 1e-2]}, True),
        "Random Forest": (RandomForestClassifier(n_estimators=300, random_state=SEMENTE),
                          {"modelo__max_depth": [None, 20], "modelo__min_samples_leaf": [1, 2],
                           "modelo__max_features": ["sqrt", 0.5]}, False),
        "Bagging": (BaggingClassifier(DecisionTreeClassifier(), n_estimators=100, random_state=SEMENTE),
                    {"modelo__n_estimators": [100, 200], "modelo__max_samples": [1.0, 0.8]}, False),
        "Boosting": (GradientBoostingClassifier(random_state=SEMENTE),
                     {"modelo__max_depth": [3, 6, 9], "modelo__n_estimators": [150, 300]}, False),
    }


def montar(modelo, escalar):
    """Pipeline = receita aplicada sempre pela mesma ordem: preencher faltas, normalizar (se preciso), modelo."""
    passos = [("imputar", SimpleImputer(strategy="median", add_indicator=True))]
    if escalar:
        passos.append(("escalar", StandardScaler()))
    passos.append(("modelo", clone(modelo)))
    return Pipeline(passos)


def estimador(nome, rapido):
    """Devolve o que vai ser avaliado: o pipeline simples (--rapido) ou o pipeline com afinação de hiperparâmetros."""
    modelo, grelha, escalar = catalogo()[nome]
    pipe = montar(modelo, escalar)
    if rapido:
        return pipe
    interno = StratifiedKFold(3, shuffle=True, random_state=SEMENTE)
    return GridSearchCV(pipe, grelha, cv=interno, scoring="accuracy", n_jobs=1)


# ----------------------------------------------------------------------------- 1) treinar
def treinar(caminho, rapido=False, pasta=PASTA):
    """Aprende com o ficheiro de treino, compara os modelos e guarda o melhor."""
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    df, entradas, y = ler_dados(caminho, com_y=True)
    X = df[entradas]
    print(f"Treino: {len(df)} produtos, {len(entradas)} variáveis, {y.mean() * 100:.1f}% com y=1.")
    print("Modo rápido (sem afinação)." if rapido else "Com afinação de hiperparâmetros (demora alguns minutos).")

    folds = StratifiedKFold(10, shuffle=True, random_state=SEMENTE)
    metricas = {"accuracy": "accuracy",
                "recall": make_scorer(recall_score, zero_division=0),
                "precision": make_scorer(precision_score, zero_division=0),
                "f1": make_scorer(f1_score, zero_division=0)}

    def avaliar(nome, est):
        t0 = time.time()
        r = cross_validate(est, X, y, cv=folds, scoring=metricas, n_jobs=-1)
        linha = {"modelo": nome, "accuracy": r["test_accuracy"].mean(), "desvio accuracy": r["test_accuracy"].std(),
                 "recall": r["test_recall"].mean(), "precision": r["test_precision"].mean(),
                 "f_measure": r["test_f1"].mean()}
        print(f"  {nome:14s} accuracy {linha['accuracy']:.4f} ± {linha['desvio accuracy']:.4f} "
              f"| recall {linha['recall']:.3f} | precision {linha['precision']:.3f} "
              f"| F {linha['f_measure']:.3f}  ({time.time() - t0:.0f}s)", flush=True)
        return linha

    print("\nCross-validation de 10 folds (os mesmos folds para todos os modelos):")
    linhas = [avaliar("Baseline (sempre y=0)", DummyClassifier(strategy="most_frequent"))]
    for nome in catalogo():
        linhas.append(avaliar(nome, estimador(nome, rapido)))
    tabela = pd.DataFrame(linhas).set_index("modelo")
    tabela.round(4).to_csv(pasta / "comparacao_modelos.csv")

    melhor = tabela.drop(index="Baseline (sempre y=0)")["accuracy"].idxmax()
    print(f"\nMelhor modelo: {melhor} (accuracy {tabela.loc[melhor, 'accuracy']:.4f}). A treinar com todo o treino...")
    final = estimador(melhor, rapido).fit(X, y)
    parametros = getattr(final, "best_params_", "por defeito")
    pacote = {"modelo": final, "variaveis": entradas, "nome": melhor, "parametros": parametros,
              "tabela": tabela, "proporcao_y1_treino": float(y.mean()), "sklearn": sklearn.__version__}
    joblib.dump(pacote, pasta / "melhor_modelo.joblib")
    print(f"Hiperparâmetros: {parametros}")
    print(f"Guardado: {pasta / 'melhor_modelo.joblib'} e {pasta / 'comparacao_modelos.csv'}")
    return tabela


# ----------------------------------------------------------------------------- 2) prever
def prever(caminho, modelo=None, saida=None):
    """Usa o modelo guardado para prever o ficheiro de teste e grava o CSV com as colunas i,y."""
    modelo = Path(modelo) if modelo else PASTA / "melhor_modelo.joblib"
    if not modelo.exists():
        raise SystemExit(f"Não encontro o modelo {modelo}. Corre primeiro: python sistema.py treinar data/training.csv")
    pacote = joblib.load(modelo)
    if pacote["sklearn"] != sklearn.__version__:
        print(f"Aviso: o modelo foi treinado com scikit-learn {pacote['sklearn']} e estás a usar {sklearn.__version__}. "
              "Se der erro, volta a correr o treinar.")

    df, _, y_real = ler_dados(caminho)
    em_falta = [c for c in pacote["variaveis"] if c not in df.columns]
    if em_falta:
        raise SystemExit(f"Ao ficheiro {caminho} faltam as colunas: {em_falta}")
    if "i" not in df.columns:
        raise SystemExit(f"O ficheiro {caminho} não tem a coluna i, necessária para a submissão.")

    previsto = pd.Series(pacote["modelo"].predict(df[pacote["variaveis"]]), index=df.index).astype(int)
    resultado = pd.DataFrame({"i": df["i"], "y": previsto})
    saida = Path(saida) if saida else PASTA / "submissao.csv"
    saida.parent.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(saida, index=False)

    print(f"Modelo usado: {pacote['nome']}  {pacote['parametros']}")
    print(f"Ficheiro lido: {caminho} ({len(df)} produtos). Previsões gravadas em {saida}")
    print("\nVerificações:")
    print(f"  linhas: {len(resultado)} | cabeçalho: i,y | i únicos: {resultado['i'].is_unique} | "
          f"valores de y só 0/1: {set(resultado['y']) <= {0, 1}}")
    print(f"  produtos previstos com y=1: {previsto.mean() * 100:.1f}% (no treino: {pacote['proporcao_y1_treino'] * 100:.1f}%)")
    print(f"  valores em falta nas variáveis (preenchidos pela mediana do treino): "
          f"{int(df[pacote['variaveis']].isna().sum().sum())}")

    if y_real is not None:
        print("\nO ficheiro tem y preenchido, por isso comparo com o real:")
        print(f"  accuracy {accuracy_score(y_real, previsto):.4f} | recall {recall_score(y_real, previsto):.3f} | "
              f"precision {precision_score(y_real, previsto, zero_division=0):.3f} | "
              f"F-measure {f1_score(y_real, previsto):.3f}")
        print("  matriz de confusão (linhas = real, colunas = previsto):")
        print(pd.DataFrame(confusion_matrix(y_real, previsto), index=["real 0", "real 1"],
                           columns=["prev 0", "prev 1"]).to_string())
    return resultado


# ----------------------------------------------------------------------------- linha de comandos
def main():
    ap = argparse.ArgumentParser(description="Aprende com o ficheiro de treino e prevê o ficheiro de teste.")
    sub = ap.add_subparsers(dest="comando", required=True)
    t = sub.add_parser("treinar", help="aprender com o ficheiro de treino")
    t.add_argument("ficheiro", help="CSV de treino, por exemplo data/training.csv")
    t.add_argument("--rapido", action="store_true", help="sem afinação de hiperparâmetros (segundos)")
    p = sub.add_parser("prever", help="prever um ficheiro de teste com o modelo guardado")
    p.add_argument("ficheiro", help="CSV de teste, por exemplo data/task.csv")
    p.add_argument("--modelo", help="modelo guardado (por defeito resultados/melhor_modelo.joblib)")
    p.add_argument("--saida", help="CSV de saída (por defeito resultados/submissao.csv)")
    a = ap.parse_args()
    if a.comando == "treinar":
        treinar(a.ficheiro, rapido=a.rapido)
    else:
        prever(a.ficheiro, modelo=a.modelo, saida=a.saida)


if __name__ == "__main__":
    main()
