# -*- coding: utf-8 -*-
"""
Trabalho AATD – classificação de produtos com desconto (y=1), metodologia CRISP-DM.

Executa de ponta a ponta:
  1. Compreensão dos dados (EDA): descrição, histogramas, boxplots, correlações, testes
  2. Preparação: valores em falta, outliers, desequilíbrio, redundância, divisão treino/validação, CV
  3. Modelação: KNN, Árvore de Decisão, Naive Bayes, MLP, Random Forest, Bagging, AdaBoost,
     Gradient Boosting (+ Extra Trees) com afinação por CV
  4. Avaliação: tabela comparativa (accuracy, precision, recall, F-measure), matrizes de confusão, ROC/PR
  5. Modelo final -> submission.csv (colunas i, y)

Uso:
    pip install pandas numpy scipy scikit-learn imbalanced-learn statsmodels matplotlib seaborn
    python trabalho_aatd.py --treino training.csv --teste task.csv --saida saida
    python trabalho_aatd.py --rapido      # grelhas reduzidas (poucos minutos)
"""
import argparse, json, time, warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.base import clone
from sklearn.ensemble import (AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier,
                              GradientBoostingClassifier, RandomForestClassifier)
from sklearn.feature_selection import mutual_info_classif
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix, f1_score,
                             precision_recall_curve, precision_score, recall_score, roc_auc_score, roc_curve)
from sklearn.model_selection import (GridSearchCV, RandomizedSearchCV, StratifiedKFold,
                                     cross_validate, train_test_split)
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.pipeline import Pipeline as IPipe
from imblearn.under_sampling import RandomUnderSampler
from statsmodels.stats.outliers_influence import variance_inflation_factor

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", font_scale=0.9)
SEED = 42
COR = {0: "#4C72B0", 1: "#DD8452"}


# ---------------------------------------------------------------------------------------------
# utilitários
# ---------------------------------------------------------------------------------------------
class Pastas:
    def __init__(self, base):
        self.base = Path(base); self.figs = self.base / "figs"; self.tabs = self.base / "tabelas"
        self.figs.mkdir(parents=True, exist_ok=True); self.tabs.mkdir(parents=True, exist_ok=True)


def guardar_fig(P, nome):
    plt.tight_layout(); plt.savefig(P.figs / nome, dpi=150); plt.close()


def titulo(txt):
    print("\n" + "=" * 90 + f"\n{txt}\n" + "=" * 90, flush=True)


# ---------------------------------------------------------------------------------------------
# 1. COMPREENSÃO DOS DADOS (EDA)
# ---------------------------------------------------------------------------------------------
def eda(tr, te, D, X, P):
    titulo("1. COMPREENSÃO DOS DADOS (EDA)")
    feats = D + X
    print(f"treino: {tr.shape} | teste: {te.shape}")
    print("alvo:\n", tr.y.value_counts().rename({0: "sem desconto", 1: "com desconto"}))
    print("em falta (treino):", tr[feats].isna().sum()[lambda s: s > 0].to_dict(),
          "| (teste):", te[feats].isna().sum()[lambda s: s > 0].to_dict())
    print("registos duplicados (treino):", int(tr[feats].duplicated().sum()),
          "| linhas de teste com gémeo no treino:", int(te[feats].merge(tr[feats].drop_duplicates()).shape[0]))
    print("x9 em falta -> taxa de y=1:", tr.loc[tr.x9.isna(), "y"].mean(),
          "| x9 observado:", round(tr.loc[tr.x9.notna(), "y"].mean(), 4))

    desc = tr[X].describe().T
    desc["assimetria"] = tr[X].skew(); desc["curtose"] = tr[X].kurt(); desc["n_valores"] = tr[X].nunique()
    desc["em_falta"] = tr[X].isna().sum()
    desc.round(3).to_csv(P.tabs / "descritiva_x.csv"); print(desc.round(2).to_string())

    dd = pd.DataFrame({"prevalencia_%": tr[D].mean() * 100, "n": tr[D].sum(),
                       "P(y=1|d=1)_%": [tr.loc[tr[c] == 1, "y"].mean() * 100 for c in D],
                       "P(y=1|d=0)_%": [tr.loc[tr[c] == 0, "y"].mean() * 100 for c in D]})
    dd.round(2).to_csv(P.tabs / "descritiva_d.csv"); print(dd.round(2).to_string())

    # alvo
    fig, ax = plt.subplots(figsize=(4.5, 3.2)); c = tr.y.value_counts().sort_index()
    ax.bar(["0 (sem desconto)", "1 (com desconto)"], c.values, color=[COR[0], COR[1]])
    for i, v in enumerate(c.values): ax.text(i, v + 30, f"{v} ({v / len(tr) * 100:.1f}%)", ha="center")
    ax.set_title("Distribuição da variável alvo"); guardar_fig(P, "alvo.png")

    # histogramas / densidades por classe / boxplots (grelha 3x3 das variáveis contínuas)
    def grelha(fun, nome, titulo_):
        fig, axs = plt.subplots(3, 3, figsize=(10, 8))
        for a, v in zip(axs.ravel(), X): fun(a, v); a.set_title(v); a.set_xlabel("")
        plt.suptitle(titulo_); guardar_fig(P, nome)
    grelha(lambda a, v: sns.histplot(tr[v].dropna(), bins=30, ax=a, color="#4C72B0"), "hist_x.png", "Histogramas")
    grelha(lambda a, v: [sns.kdeplot(tr.loc[tr.y == k, v].dropna(), ax=a, color=COR[k], fill=True, alpha=.3,
                                     label=f"y={k}", warn_singular=False) for k in (0, 1)], "kde_x_por_y.png", "Densidades por classe")
    grelha(lambda a, v: sns.boxplot(x=tr[v].dropna(), ax=a, color="#8DA0CB", fliersize=2), "box_x.png", "Diagramas de caixa")
    grelha(lambda a, v: sns.boxplot(data=tr, x="y", y=v, ax=a, palette=[COR[0], COR[1]], fliersize=2), "box_x_por_y.png",
           "Diagramas de caixa por classe")

    # variáveis discretas
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.5)); dd["prevalencia_%"].plot.bar(ax=axs[0], color="#4C72B0")
    axs[0].set_title("Prevalência das variáveis discretas (%)"); xx = np.arange(len(D))
    axs[1].bar(xx - .2, dd["P(y=1|d=1)_%"], .4, label="d=1", color=COR[1]); axs[1].bar(xx + .2, dd["P(y=1|d=0)_%"], .4, label="d=0", color=COR[0])
    axs[1].axhline(tr.y.mean() * 100, color="k", ls="--", lw=1, label="média global"); axs[1].set_xticks(xx)
    axs[1].set_xticklabels(D, rotation=90); axs[1].legend(); axs[1].set_title("P(y=1) (%) conforme d"); guardar_fig(P, "vars_d.png")

    # correlações
    corr = tr[X + D + ["y"]].corr()
    fig, ax = plt.subplots(figsize=(10, 8.5)); sns.heatmap(corr, cmap="coolwarm", center=0, vmin=-1, vmax=1, ax=ax, linewidths=.3)
    ax.set_title("Matriz de correlação"); guardar_fig(P, "corr_todas.png")
    fig, ax = plt.subplots(figsize=(5.5, 4.5)); sns.heatmap(tr[X].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, vmin=-1, vmax=1, ax=ax)
    ax.set_title("Correlação entre variáveis contínuas"); guardar_fig(P, "corr_x.png")
    cy = corr["y"].drop("y").sort_values(); cy.round(4).to_csv(P.tabs / "corr_com_y.csv")
    fig, ax = plt.subplots(figsize=(5.5, 6)); ax.barh(cy.index, cy.values, color=["#DD8452" if v > 0 else "#4C72B0" for v in cy.values])
    ax.set_title("Correlação de cada variável com y"); guardar_fig(P, "corr_y.png")

    # testes de associação com y
    linhas = [(v, "Mann-Whitney", stats.mannwhitneyu(tr.loc[tr.y == 0, v].dropna(), tr.loc[tr.y == 1, v].dropna()).pvalue) for v in X]
    linhas += [(v, "Qui-quadrado", stats.chi2_contingency(pd.crosstab(tr[v], tr.y))[1]) for v in D]
    t = pd.DataFrame(linhas, columns=["variavel", "teste", "p_valor"]); t["signif_5%"] = t.p_valor < .05
    t.to_csv(P.tabs / "testes_associacao.csv", index=False)
    print(f"\nvariáveis com associação significativa a 5%: {int(t['signif_5%'].sum())}/{len(t)}")


# ---------------------------------------------------------------------------------------------
# 2. PREPARAÇÃO DOS DADOS
# ---------------------------------------------------------------------------------------------
def preparar(tr, D, X, P):
    titulo("2. PREPARAÇÃO DOS DADOS")
    feats = D + X
    # 2.1 divisão treino interno / validação (hold-out estratificado) + CV estratificada
    trn, val = train_test_split(tr, test_size=0.2, stratify=tr.y, random_state=SEED)
    trn, val = trn.reset_index(drop=True), val.reset_index(drop=True)
    cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
    print(f"treino interno: {len(trn)} (y=1: {trn.y.mean():.4f}) | validação: {len(val)} (y=1: {val.y.mean():.4f})")
    folds = [(k, len(a), len(b), round(trn.y.iloc[a].mean(), 4), round(trn.y.iloc[b].mean(), 4)) for k, (a, b) in enumerate(cv.split(trn[feats], trn.y), 1)]
    pd.DataFrame(folds, columns=["fold", "n_treino", "n_teste", "y1_treino", "y1_teste"]).to_csv(P.tabs / "folds_cv.csv", index=False)
    Xt, yt = trn[feats], trn.y

    def aval(modelo, nome, cols=None):
        s = cross_validate(modelo, Xt if cols is None else Xt[cols], yt, cv=cv, scoring=["accuracy", "precision", "recall", "f1"])
        return {k: round(s[f"test_{k}"].mean(), 4) for k in ("accuracy", "precision", "recall", "f1")}

    # 2.2 valores em falta
    print("\n[valores em falta] comparação de imputações (CV)")
    res = {}
    for nm, imp in {"mediana": SimpleImputer(strategy="median"), "média": SimpleImputer(strategy="mean"), "KNN(5)": KNNImputer(n_neighbors=5)}.items():
        for mn, m in {"DT": DecisionTreeClassifier(max_depth=6, random_state=SEED), "RF": RandomForestClassifier(200, n_jobs=-1, random_state=SEED)}.items():
            res[f"{nm}|{mn}"] = aval(make_pipeline(imp, m), mn)
    imp_df = pd.DataFrame(res).T; imp_df.to_csv(P.tabs / "imputacao.csv"); print(imp_df.to_string())

    # 2.3 outliers (Tukey) e efeito da winsorização
    print("\n[outliers] critério de Tukey (1,5·IQR) e |z|>3")
    linhas = []
    for v in X:
        q1, q3 = tr[v].quantile([.25, .75]); i = q3 - q1; lo, hi = q1 - 1.5 * i, q3 + 1.5 * i
        n = int(((tr[v] < lo) | (tr[v] > hi)).sum()); z = int((((tr[v] - tr[v].mean()) / tr[v].std()).abs() > 3).sum())
        linhas.append((v, round(lo, 2), round(hi, 2), n, round(n / len(tr) * 100, 2), z))
    ot = pd.DataFrame(linhas, columns=["variavel", "lim_inf", "lim_sup", "n_outliers_IQR", "%", "n_|z|>3"])
    ot.to_csv(P.tabs / "outliers.csv", index=False); print(ot.to_string(index=False))
    print("nota: x4 tem IQR=0 -> o critério de Tukey marca como outlier qualquer valor != 1 (categorias legítimas)")
    lim = {v: (tr[v].quantile(.25) - 1.5 * (tr[v].quantile(.75) - tr[v].quantile(.25)), tr[v].quantile(.75) + 1.5 * (tr[v].quantile(.75) - tr[v].quantile(.25))) for v in X
           if tr[v].quantile(.75) > tr[v].quantile(.25)}
    xw = tr[X].copy()
    for v, (lo, hi) in lim.items(): xw[v] = xw[v].clip(lo, hi)
    z = lambda d: (d - d.mean()) / d.std()
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
    sns.boxplot(data=z(tr[X]).melt(), x="variable", y="value", ax=axs[0], color="#8DA0CB", fliersize=2); axs[0].set_title("Antes (padronizado)")
    sns.boxplot(data=z(xw).melt(), x="variable", y="value", ax=axs[1], color="#66C2A5", fliersize=2); axs[1].set_title("Depois da winsorização")
    for a in axs: a.set_xlabel("")
    guardar_fig(P, "outliers_antes_depois.png")

    class Wins:  # winsorização ajustada só no treino de cada fold
        def __init__(self): self.l = None
        def fit(self, A, y=None):
            A = np.asarray(A, float); q1, q3 = np.nanpercentile(A, 25, 0), np.nanpercentile(A, 75, 0)
            self.lo, self.hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1); self.k = (q3 - q1) > 0; return self
        def transform(self, A): return np.where(self.k, np.clip(np.asarray(A, float), self.lo, self.hi), np.asarray(A, float))
        def get_params(self, deep=True): return {}
        def set_params(self, **p): return self
        def fit_transform(self, A, y=None): return self.fit(A).transform(A)
    from sklearn.base import BaseEstimator, TransformerMixin
    class Winsor(Wins, BaseEstimator, TransformerMixin): pass
    res = {}
    for mn, m in {"KNN": KNeighborsClassifier(15), "NB": GaussianNB()}.items():
        for w in (False, True):
            passos = [SimpleImputer(strategy="median")] + ([Winsor()] if w else []) + [StandardScaler(), m]
            res[f"{mn}|{'com' if w else 'sem'} winsorização"] = aval(make_pipeline(*passos), mn)
    wdf = pd.DataFrame(res).T; wdf.to_csv(P.tabs / "winsorizacao.csv"); print("\n", wdf.to_string())
    print("-> decisão: outliers mantidos (valores plausíveis; árvores são robustas; winsorização não melhora)")

    # 2.4 desequilíbrio de classes
    print("\n[desequilíbrio] estratégias (CV)")
    estrat = {"Sem tratamento": None, "class_weight": "cw", "Sobreamostragem": RandomOverSampler(random_state=SEED),
              "SMOTE": SMOTE(random_state=SEED), "Subamostragem": RandomUnderSampler(random_state=SEED)}
    modelos = {"DT": lambda cw: DecisionTreeClassifier(max_depth=6, class_weight=cw, random_state=SEED),
               "KNN": lambda cw: KNeighborsClassifier(15),
               "RF": lambda cw: RandomForestClassifier(200, class_weight=cw, n_jobs=-1, random_state=SEED)}
    linhas = []
    for sn, sm in estrat.items():
        for mn, mk in modelos.items():
            if sn == "class_weight" and mn == "KNN": continue
            passos = [("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]
            if sm not in (None, "cw"): passos.append(("res", sm))
            passos.append(("m", mk("balanced" if sm == "cw" else None)))
            linhas.append((sn, mn, *aval(IPipe(passos), mn).values()))
    imb = pd.DataFrame(linhas, columns=["estrategia", "modelo", "accuracy", "precision", "recall", "f1"])
    imb.to_csv(P.tabs / "desequilibrio.csv", index=False); print(imb.to_string(index=False))
    p = imb.pivot(index="estrategia", columns="modelo", values="f1").loc[imb["estrategia"].unique()]
    ax = p.plot.bar(figsize=(8, 4.5)); ax.set_ylabel("F1 (classe 1) - CV"); ax.set_xlabel(""); ax.grid(axis="x", visible=False)
    ax.legend(title="modelo", ncol=3, loc="upper center", bbox_to_anchor=(.5, -.3), frameon=False); plt.xticks(rotation=20, ha="right")
    guardar_fig(P, "desequilibrio.png")
    print("-> decisão: a reamostragem (nenhuma/SMOTE) é tratada como hiperparâmetro de cada modelo")

    # 2.5 redundância de variáveis
    print("\n[redundância] correlações |r|>0,3, VIF, informação mútua")
    Xi = pd.DataFrame(SimpleImputer(strategy="median").fit_transform(tr[feats]), columns=feats); c = Xi.corr().abs()
    pares = pd.DataFrame([(a, b, round(c.loc[a, b], 3)) for i, a in enumerate(feats) for b in feats[i + 1:] if c.loc[a, b] > .3], columns=["v1", "v2", "|r|"]).sort_values("|r|", ascending=False)
    pares.to_csv(P.tabs / "pares_correlacionados.csv", index=False); print(pares.head(8).to_string(index=False))
    Xv = Xi[X].assign(const=1); vif = pd.Series([variance_inflation_factor(Xv.values, i) for i in range(len(X))], index=X).round(2)
    vif.to_csv(P.tabs / "vif.csv", header=["VIF"]); print("VIF:", vif.to_dict())
    mi = pd.Series(mutual_info_classif(Xi, tr.y, discrete_features=[f in D for f in feats], random_state=SEED), index=feats).sort_values()
    mi.round(4).to_csv(P.tabs / "informacao_mutua.csv", header=["MI"])
    fig, ax = plt.subplots(figsize=(5.5, 6)); ax.barh(mi.index, mi.values, color="#8DA0CB"); ax.set_title("Informação mútua com y"); guardar_fig(P, "info_mutua.png")
    cand = {"todas": [], "sem x3": ["x3"], "sem x3 e x4": ["x3", "x4"], "sem MI≈0": list(mi[mi < 0.001].index)}
    res = {}
    for nm, drop in cand.items():
        cols = [f for f in feats if f not in drop]
        res[nm] = {"n_vars": len(cols), **aval(make_pipeline(SimpleImputer(strategy="median"), RandomForestClassifier(200, n_jobs=-1, random_state=SEED)), nm, cols)}
    rd = pd.DataFrame(res).T; rd.to_csv(P.tabs / "remocao_variaveis.csv"); print(rd.to_string())
    print("-> decisão: mantêm-se todas as variáveis (sem redundância severa; ganhos dentro do ruído)")
    return trn, val, cv


# ---------------------------------------------------------------------------------------------
# 3. MODELAÇÃO
# ---------------------------------------------------------------------------------------------
def pipe(modelo, escalar):
    """imputação pela mediana + indicador de ausência; padronização nos modelos sensíveis à escala."""
    passos = [("imp", SimpleImputer(strategy="median", add_indicator=True))]
    if escalar: passos.append(("sc", StandardScaler()))
    return IPipe(passos + [("res", "passthrough"), ("m", modelo)])


def configuracoes(rapido):
    RES = ["passthrough", SMOTE(random_state=SEED)]
    dt = lambda **k: DecisionTreeClassifier(random_state=SEED, **k)
    if rapido:
        return {
            "KNN": (pipe(KNeighborsClassifier(), True), {"m__n_neighbors": [5, 7, 15], "m__weights": ["distance"], "res": RES}),
            "Árvore de Decisão": (pipe(dt(), False), {"m__max_depth": [6, None], "m__min_samples_leaf": [1, 5], "res": RES}),
            "Naive Bayes": (pipe(GaussianNB(), True), {"m__var_smoothing": [1e-6, 1e-1], "res": RES}),
            "MLP": (pipe(MLPClassifier(max_iter=600, early_stopping=True, random_state=SEED), True), {"m__hidden_layer_sizes": [(64, 32)], "m__alpha": [1e-4], "res": RES}),
            "Random Forest": (pipe(RandomForestClassifier(n_jobs=1, random_state=SEED), False), {"m__n_estimators": [300], "m__max_features": ["sqrt", 0.5], "res": RES}),
            "Bagging": (pipe(BaggingClassifier(dt(), n_estimators=50, random_state=SEED), False), {"m__max_samples": [1.0], "res": RES}),
            "AdaBoost": (pipe(AdaBoostClassifier(dt(max_depth=3), random_state=SEED), False), {"m__n_estimators": [100, 300], "m__learning_rate": [0.3, 1.0], "res": RES}),
            "Gradient Boosting": (pipe(GradientBoostingClassifier(random_state=SEED), False), {"m__n_estimators": [200], "m__max_depth": [3, 5], "res": RES}),
            "Extra Trees": (pipe(ExtraTreesClassifier(n_jobs=1, random_state=SEED), False), {"m__n_estimators": [300], "m__max_features": ["sqrt", 0.8], "res": RES}),
        }, None
    return {
        "KNN": (pipe(KNeighborsClassifier(), True), {"m__n_neighbors": [3, 5, 7, 11, 15, 25], "m__weights": ["uniform", "distance"], "m__p": [1, 2], "res": RES}),
        "Árvore de Decisão": (pipe(dt(), False), {"m__max_depth": [4, 6, 8, 12, None], "m__min_samples_leaf": [1, 5, 10], "m__criterion": ["gini", "entropy"], "res": RES}),
        "Naive Bayes": (pipe(GaussianNB(), True), {"m__var_smoothing": [1e-9, 1e-6, 1e-3, 1e-1], "res": RES}),
        "MLP": (pipe(MLPClassifier(max_iter=600, early_stopping=True, random_state=SEED), True), {"m__hidden_layer_sizes": [(32,), (64,), (64, 32)], "m__alpha": [1e-4, 1e-2], "m__learning_rate_init": [1e-3, 1e-2], "res": RES}),
        "Random Forest": (pipe(RandomForestClassifier(n_jobs=1, random_state=SEED), False), {"m__n_estimators": [300, 600], "m__max_features": ["sqrt", 0.5], "m__min_samples_leaf": [1, 2], "res": RES}),
        "Bagging": (pipe(BaggingClassifier(dt(), random_state=SEED, n_jobs=1), False), {"m__n_estimators": [50, 200], "m__max_samples": [0.7, 1.0], "m__estimator__max_depth": [None, 12], "res": RES}),
        "AdaBoost": (pipe(AdaBoostClassifier(dt(), random_state=SEED), False), {"m__n_estimators": [100, 300], "m__learning_rate": [0.3, 1.0], "m__estimator__max_depth": [1, 3, 5], "res": RES}),
        "Gradient Boosting": (pipe(GradientBoostingClassifier(random_state=SEED), False), {"m__n_estimators": [200, 500], "m__learning_rate": [0.05, 0.1], "m__max_depth": [3, 5, 7], "m__subsample": [0.8, 1.0], "res": RES}),
        "Extra Trees": (pipe(ExtraTreesClassifier(n_jobs=1, random_state=SEED), False), {"m__n_estimators": [300, 600], "m__max_features": ["sqrt", 0.5, 0.8], "m__min_samples_leaf": [1, 2], "res": RES}),
    }, {"Gradient Boosting": 12}


def modelar(trn, val, D, X, cv, rapido, njobs, P):
    titulo("3. MODELAÇÃO E 4. AVALIAÇÃO")
    feats = D + X; Xt, yt, Xv, yv = trn[feats], trn.y, val[feats], val.y
    cfg, n_iter = configuracoes(rapido); linhas, ajustados, probs, params = [], {}, {}, {}
    for nome, (p, grelha) in cfg.items():
        t0 = time.time()
        if n_iter and nome in n_iter:
            gs = RandomizedSearchCV(p, grelha, n_iter=n_iter[nome], cv=cv, scoring="accuracy", n_jobs=njobs, random_state=SEED)
        else:
            gs = GridSearchCV(p, grelha, cv=cv, scoring="accuracy", n_jobs=njobs)
        gs.fit(Xt, yt); melhor = gs.best_estimator_
        s = cross_validate(melhor, Xt, yt, cv=cv, scoring=["accuracy", "f1"])
        pv, pr = melhor.predict(Xv), melhor.predict_proba(Xv)[:, 1]; ajustados[nome], probs[nome] = melhor, pr
        res = "nenhuma" if melhor.named_steps["res"] == "passthrough" else "SMOTE"
        params[nome] = {**{k: str(v) for k, v in gs.best_params_.items() if k != "res"}, "reamostragem": res}
        linhas.append(dict(modelo=nome, cv_accuracy=s["test_accuracy"].mean(), cv_std=s["test_accuracy"].std(), cv_f1=s["test_f1"].mean(),
                           accuracy=accuracy_score(yv, pv), precision=precision_score(yv, pv), recall=recall_score(yv, pv),
                           f_measure=f1_score(yv, pv), auc=roc_auc_score(yv, pr), ap=average_precision_score(yv, pr),
                           VN_FP_FN_VP=str(confusion_matrix(yv, pv).ravel().tolist()), reamostragem=res))
        print(f"{nome:18s} CV acc={s['test_accuracy'].mean():.4f}±{s['test_accuracy'].std():.4f} | val acc={linhas[-1]['accuracy']:.4f} "
              f"P={linhas[-1]['precision']:.3f} R={linhas[-1]['recall']:.3f} F={linhas[-1]['f_measure']:.3f} | {res} | {time.time() - t0:.0f}s", flush=True)
    R = pd.DataFrame(linhas); R.to_csv(P.tabs / "comparacao_modelos.csv", index=False)
    json.dump(params, open(P.tabs / "hiperparametros.json", "w"), indent=1, ensure_ascii=False)
    print("\nTABELA COMPARATIVA (validação, classe 1; ordenada por accuracy em CV)")
    print(R.sort_values("cv_accuracy", ascending=False).drop(columns=["VN_FP_FN_VP", "ap"]).round(4).to_string(index=False))

    # figuras
    M = R.sort_values("accuracy", ascending=False).set_index("modelo")
    ax = M[["accuracy", "precision", "recall", "f_measure"]].plot.bar(figsize=(9, 4.8), width=.8); ax.set_ylim(0, 1); ax.set_xlabel("")
    ax.grid(axis="x", visible=False); ax.set_title("Desempenho no conjunto de validação (classe 1)")
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(.5, -.28), frameon=False); plt.xticks(rotation=25, ha="right"); guardar_fig(P, "comparacao_modelos.png")
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))
    for n in M.index:
        f, t, _ = roc_curve(yv, probs[n]); axs[0].plot(f, t, label=f"{n} ({M.loc[n, 'auc']:.3f})")
        pp, rr, _ = precision_recall_curve(yv, probs[n]); axs[1].plot(rr, pp, label=n)
    axs[0].plot([0, 1], [0, 1], "k--", lw=.8); axs[0].set_title("Curvas ROC (AUC)"); axs[0].legend(fontsize=7)
    axs[0].set_xlabel("FPR"); axs[0].set_ylabel("TPR"); axs[1].set_title("Curvas Precision-Recall"); axs[1].set_xlabel("Recall"); axs[1].set_ylabel("Precision")
    guardar_fig(P, "roc_pr.png")
    fig, axs = plt.subplots(3, 3, figsize=(10, 9))
    for a, n in zip(axs.ravel(), cfg):
        sns.heatmap(confusion_matrix(yv, ajustados[n].predict(Xv)), annot=True, fmt="d", cmap="Blues", cbar=False, ax=a, xticklabels=["0", "1"], yticklabels=["0", "1"])
        a.set_title(n); a.set_xlabel("Previsto"); a.set_ylabel("Real")
    guardar_fig(P, "matrizes_confusao.png")
    for nm in ("Random Forest", "Extra Trees"):
        m = ajustados[nm].named_steps["m"]; imp = pd.Series(m.feature_importances_, index=feats + ["x9_em_falta"]).sort_values()
        fig, ax = plt.subplots(figsize=(5.5, 6.5)); ax.barh(imp.index, imp.values, color="#66C2A5"); ax.set_title(f"Importância das variáveis – {nm}")
        guardar_fig(P, f"importancia_{nm.replace(' ', '_')}.png")
    return R, ajustados


# ---------------------------------------------------------------------------------------------
# 5. MODELO FINAL E SUBMISSÃO
# ---------------------------------------------------------------------------------------------
def final(tr, te, R, ajustados, feats, saida):
    titulo("5. MODELO FINAL E SUBMISSÃO")
    melhor = R.sort_values(["cv_accuracy", "cv_f1"], ascending=False).modelo.iloc[0]   # critério: CV no treino interno
    modelo = clone(ajustados[melhor]).fit(tr[feats], tr.y)                              # reajuste com todo o treino
    pred = modelo.predict(te[feats]).astype(int)
    sub = pd.DataFrame({"i": te.i, "y": pred}); sub.to_csv(Path(saida) / "submission.csv", index=False)
    print(f"modelo selecionado: {melhor} | {len(sub)} previsões | % com desconto: {pred.mean() * 100:.1f}% (treino: {tr.y.mean() * 100:.1f}%)")
    print("registos de teste com x9 em falta previstos y=1:", int(pred[te.x9.isna().values].sum()), "de", int(te.x9.isna().sum()))
    print(f"ficheiro: {Path(saida) / 'submission.csv'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--treino", default="training.csv"); ap.add_argument("--teste", default="task.csv")
    ap.add_argument("--saida", default="saida"); ap.add_argument("--rapido", action="store_true", help="grelhas reduzidas")
    ap.add_argument("--njobs", type=int, default=-1, help="processos em paralelo (-1 = todos)")
    a = ap.parse_args()
    tr, te = pd.read_csv(a.treino), pd.read_csv(a.teste)
    feats = [c for c in tr.columns if c not in ("i", "y")]            # 'i' é ignorado
    D = [c for c in feats if c.startswith("d")]; X = [c for c in feats if c.startswith("x")]
    P = Pastas(a.saida)
    eda(tr, te, D, X, P)
    trn, val, cv = preparar(tr, D, X, P)
    R, ajustados = modelar(trn, val, D, X, cv, a.rapido, a.njobs, P)
    final(tr, te, R, ajustados, D + X, a.saida)
    print(f"\nconcluído. Figuras em {P.figs} | tabelas em {P.tabs}")


if __name__ == "__main__":
    main()
