# -*- coding: utf-8 -*-
"""Verificação de sobreajuste (overfitting): treino vs CV vs validação, curvas de aprendizagem,
CV aninhada, teste de permutação de etiquetas e intervalo de confiança bootstrap."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.base import clone
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import (GridSearchCV, StratifiedKFold, cross_val_score, learning_curve, train_test_split)
import trabalho_aatd as T

OUT = Path("saida_overfit"); OUT.mkdir(exist_ok=True)
tr = pd.read_csv("data/training.csv"); feats = [c for c in tr.columns if c not in ("i", "y")]
D = [c for c in feats if c.startswith("d")]; X = [c for c in feats if c.startswith("x")]
trn, val = train_test_split(tr, test_size=0.2, stratify=tr.y, random_state=T.SEED); trn, val = trn.reset_index(drop=True), val.reset_index(drop=True)
cv = StratifiedKFold(5, shuffle=True, random_state=T.SEED); Xt, yt, Xv, yv = trn[feats], trn.y, val[feats], val.y

# --- reajustar os modelos (mesma afinação do script principal)
cfg, n_iter = T.configuracoes(False); aj = {}
for n, (p, g) in cfg.items():
    gs = (T.RandomizedSearchCV(p, g, n_iter=n_iter[n], cv=cv, scoring="accuracy", n_jobs=4, random_state=T.SEED) if n_iter and n in n_iter
          else GridSearchCV(p, g, cv=cv, scoring="accuracy", n_jobs=4))
    gs.fit(Xt, yt); aj[n] = gs.best_estimator_; print("ajustado", n, flush=True)

# 1. treino vs CV vs validação
linhas = []
for n, m in aj.items():
    cvs = cross_val_score(m, Xt, yt, cv=cv, scoring="accuracy")
    acc_tr, acc_v = accuracy_score(yt, m.predict(Xt)), accuracy_score(yv, m.predict(Xv))
    linhas.append(dict(modelo=n, treino=acc_tr, cv=cvs.mean(), validacao=acc_v, lacuna_treino_cv=acc_tr - cvs.mean(), lacuna_cv_validacao=cvs.mean() - acc_v,
                       f1_treino=f1_score(yt, m.predict(Xt)), f1_validacao=f1_score(yv, m.predict(Xv))))
R = pd.DataFrame(linhas); R.to_csv(OUT / "treino_cv_validacao.csv", index=False)
print("\n1) TREINO vs CV vs VALIDAÇÃO (accuracy)\n", R.round(4).to_string(index=False), flush=True)
fig, ax = plt.subplots(figsize=(9, 4.5)); R.set_index("modelo")[["treino", "cv", "validacao"]].plot.bar(ax=ax, width=.8)
ax.set_ylim(0.5, 1.02); ax.grid(axis="x", visible=False); ax.set_title("Accuracy: treino vs validação cruzada vs validação"); plt.xticks(rotation=25, ha="right")
ax.legend(["treino", "CV (5 folds)", "validação"], ncol=3, loc="upper center", bbox_to_anchor=(.5, -.3), frameon=False); plt.tight_layout(); plt.savefig(OUT / "treino_cv_val.png", dpi=150); plt.close()

# 2. curvas de aprendizagem
fig, axs = plt.subplots(1, 4, figsize=(15, 3.6), sharey=True); lc = {}
for a, n in zip(axs, ["AdaBoost", "Gradient Boosting", "Extra Trees", "Árvore de Decisão"]):
    sz, ts, vs = learning_curve(clone(aj[n]), Xt, yt, cv=cv, train_sizes=np.linspace(.2, 1, 5), scoring="accuracy", n_jobs=4, random_state=T.SEED)
    a.plot(sz, ts.mean(1), "o-", label="treino"); a.plot(sz, vs.mean(1), "o-", label="CV")
    a.fill_between(sz, vs.mean(1) - vs.std(1), vs.mean(1) + vs.std(1), alpha=.2, color="C1"); a.set_title(n); a.set_xlabel("n.º de exemplos de treino")
    lc[n] = dict(tamanhos=sz.tolist(), treino=ts.mean(1).round(4).tolist(), cv=vs.mean(1).round(4).tolist())
axs[0].set_ylabel("accuracy"); axs[0].legend(); plt.tight_layout(); plt.savefig(OUT / "curvas_aprendizagem.png", dpi=150); plt.close()
json.dump(lc, open(OUT / "curvas_aprendizagem.json", "w"), indent=1)
print("\n2) CURVAS DE APRENDIZAGEM (accuracy CV com 20% ... 100% do treino)")
for n, d in lc.items(): print(f"  {n:18s} CV: {d['cv']}  | treino: {d['treino']}", flush=True)

# 3. CV aninhada (afinação dentro de cada fold externo) com grelhas reduzidas -> estimativa sem viés de seleção
cfg_r, _ = T.configuracoes(True); ext = StratifiedKFold(5, shuffle=True, random_state=7); inn = StratifiedKFold(3, shuffle=True, random_state=7)
print("\n3) CV ANINHADA (externa 5 folds, interna 3 folds; grelhas reduzidas)")
aninhada = {}
for n in ["Extra Trees", "Gradient Boosting", "AdaBoost", "Random Forest"]:
    p, g = cfg_r[n]; s = cross_val_score(GridSearchCV(p, g, cv=inn, scoring="accuracy", n_jobs=4), Xt, yt, cv=ext, scoring="accuracy")
    aninhada[n] = (round(s.mean(), 4), round(s.std(), 4)); print(f"  {n:18s} {s.mean():.4f} ± {s.std():.4f}", flush=True)
json.dump(aninhada, open(OUT / "cv_aninhada.json", "w"), indent=1)

# 4. teste de permutação das etiquetas (sem sinal real a accuracy deve ficar ~ baseline)
rng = np.random.RandomState(0); yp = pd.Series(rng.permutation(yt.values)); perm = {}
print("\n4) TESTE DE PERMUTAÇÃO (y embaralhado; baseline = %.3f)" % max(yt.mean(), 1 - yt.mean()))
for n in ["AdaBoost", "Extra Trees"]:
    s = cross_val_score(clone(aj[n]), Xt, yp, cv=cv, scoring="accuracy"); perm[n] = round(s.mean(), 4)
    print(f"  {n:18s} accuracy CV com etiquetas aleatórias: {s.mean():.4f}", flush=True)
json.dump(perm, open(OUT / "permutacao.json", "w"), indent=1)

# 5. IC bootstrap da accuracy na validação
print("\n5) IC 95% (bootstrap, 2000 réplicas) da accuracy na validação")
ic = {}
for n in ["AdaBoost", "Gradient Boosting", "Extra Trees", "Bagging", "Random Forest"]:
    pr = aj[n].predict(Xv).astype(int); y = yv.values; b = [accuracy_score(y[i], pr[i]) for i in (rng.randint(0, len(y), len(y)) for _ in range(2000))]
    ic[n] = (round(float(np.percentile(b, 2.5)), 4), round(float(np.percentile(b, 97.5)), 4)); print(f"  {n:18s} [{ic[n][0]:.4f}; {ic[n][1]:.4f}]")
json.dump(ic, open(OUT / "ic_validacao.json", "w"), indent=1)
