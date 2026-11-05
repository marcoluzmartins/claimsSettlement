"""Lê um ficheiro CSV (training.csv ou task.csv) e cria os gráficos de análise exploratória (EDA).

Os gráficos adaptam-se ao ficheiro lido:
  - descobre sozinho quais são as variáveis contínuas (x1, x2, ...) e as discretas (d1, d2, ...);
  - se o ficheiro tem a coluna y preenchida (training.csv), cria também os gráficos que usam o y;
  - se o y está vazio (task.csv), esses gráficos são saltados.

Como usar:
    python eda_graficos.py data/training.csv
    python eda_graficos.py data/task.csv
    python eda_graficos.py data/training.csv --saida minha_pasta

Os gráficos (.png) e as tabelas (.csv) ficam em graficos/<nome do ficheiro>/ (ou na pasta de --saida).
"""
import argparse
import math
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # grava os gráficos em ficheiro, não abre janelas
import matplotlib.pyplot as plt
import pandas as pd

AZUL, LARANJA = "#3b6ea5", "#d98c3b"


# ----------------------------------------------------------------------------- ler os dados
def ler_dados(caminho):
    """Lê o CSV e separa as colunas: identificador, alvo (y), discretas (d*) e contínuas (x*)."""
    df = pd.read_csv(caminho)
    d_vars = [c for c in df.columns if re.fullmatch(r"d\d+", c)]
    x_vars = [c for c in df.columns if re.fullmatch(r"x\d+", c)]
    tem_y = "y" in df.columns and df["y"].notna().any()
    y = df["y"].astype(int) if tem_y else None
    return df, d_vars, x_vars, y


# ----------------------------------------------------------------------------- tabelas
def tabelas(df, d_vars, x_vars, y, pasta):
    """Análise descritiva: estatísticas das x*, frequência das d* e valores em falta."""
    desc_x = df[x_vars].describe().T
    desc_x["valores distintos"] = df[x_vars].nunique()
    desc_x["assimetria"] = df[x_vars].skew()
    desc_x["valores em falta"] = df[x_vars].isna().sum()
    desc_x.round(3).to_csv(pasta / "descritiva_x.csv")

    linhas = []
    for v in d_vars:
        ativo = df[v] == 1
        linha = {"variável": v, "n (d=1)": int(ativo.sum()), "% dos produtos": round(ativo.mean() * 100, 1)}
        if y is not None:
            linha["P(y=1 | d=1)"] = round(y[ativo].mean(), 3)
            linha["P(y=1 | d=0)"] = round(y[~ativo].mean(), 3)
        linhas.append(linha)
    desc_d = pd.DataFrame(linhas).set_index("variável")
    desc_d.to_csv(pasta / "descritiva_d.csv")

    faltas = df.isna().sum()
    faltas = faltas[faltas > 0].drop(labels=["y"], errors="ignore")
    faltas.rename("valores em falta").to_csv(pasta / "valores_em_falta.csv")

    print(f"\nLinhas: {len(df)} | variáveis contínuas: {len(x_vars)} | variáveis discretas: {len(d_vars)}")
    print("\nVariáveis contínuas:")
    print(desc_x.round(2)[["mean", "std", "min", "50%", "max", "valores em falta"]].to_string())
    print("\nValores em falta:", faltas.to_dict() if len(faltas) else "nenhum")
    return desc_d


# ----------------------------------------------------------------------------- gráficos
def guardar(fig, pasta, nome, criados):
    fig.savefig(pasta / f"{nome}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    criados.append(f"{nome}.png")


def grelha(n, colunas=3, altura=3.0, largura=4.0):
    """Cria uma grelha de gráficos com o número de linhas necessário para n variáveis."""
    linhas = math.ceil(n / colunas)
    fig, eixos = plt.subplots(linhas, colunas, figsize=(largura * colunas, altura * linhas), squeeze=False)
    eixos = eixos.flatten()
    for extra in eixos[n:]:
        extra.axis("off")
    return fig, eixos


def grafico_alvo(y, pasta, criados):
    contagem = y.value_counts().sort_index()
    nomes = {0: "y=0 (sem desconto)", 1: "y=1 (com desconto)"}
    fig, ax = plt.subplots(figsize=(4.5, 3.6))
    ax.bar([nomes.get(k, str(k)) for k in contagem.index], contagem.values, color=[AZUL, LARANJA][: len(contagem)])
    for i, v in enumerate(contagem.values):
        ax.text(i, v, f"{v} ({v / len(y) * 100:.1f}%)", ha="center", va="bottom")
    ax.set_ylabel("Produtos")
    ax.set_title("Distribuição da variável alvo")
    guardar(fig, pasta, "01_alvo", criados)


def grafico_histogramas(df, x_vars, pasta, criados):
    fig, eixos = grelha(len(x_vars))
    for ax, v in zip(eixos, x_vars):
        ax.hist(df[v].dropna(), bins=min(30, max(5, df[v].nunique())), color=AZUL, edgecolor="white")
        ax.set_title(v)
        ax.set_ylabel("Produtos")
    fig.suptitle("Histogramas das variáveis contínuas")
    fig.tight_layout()
    guardar(fig, pasta, "02_histogramas_x", criados)


def grafico_frequencia_d(desc_d, pasta, criados):
    ordem = desc_d["% dos produtos"].sort_values().index
    fig, ax = plt.subplots(figsize=(7, 0.3 * len(ordem) + 1.5))
    ax.barh(ordem, desc_d.loc[ordem, "% dos produtos"], color=AZUL)
    ax.set_xlabel("% de produtos com d=1")
    ax.set_title("Frequência das variáveis discretas")
    guardar(fig, pasta, "03_frequencia_d", criados)


def grafico_boxplots(df, x_vars, pasta, criados):
    fig, eixos = grelha(len(x_vars))
    for ax, v in zip(eixos, x_vars):
        ax.boxplot(df[v].dropna(), patch_artist=True, boxprops=dict(facecolor="#b7cde6"),
                   medianprops=dict(color="black"))
        ax.set_title(v)
        ax.set_xticks([])
    fig.suptitle("Boxplots das variáveis contínuas")
    fig.tight_layout()
    guardar(fig, pasta, "04_boxplots_x", criados)


def grafico_boxplots_por_classe(df, x_vars, y, pasta, criados):
    fig, eixos = grelha(len(x_vars))
    for ax, v in zip(eixos, x_vars):
        dados = [df.loc[y == c, v].dropna() for c in sorted(y.unique())]
        ax.boxplot(dados, tick_labels=[f"y={c}" for c in sorted(y.unique())], patch_artist=True,
                   boxprops=dict(facecolor="#b7cde6"), medianprops=dict(color="black"))
        ax.set_title(v)
    fig.suptitle("Variáveis contínuas por classe de y")
    fig.tight_layout()
    guardar(fig, pasta, "05_boxplots_x_por_classe", criados)


def heatmap(corr, titulo, pasta, nome, criados, anotar=True):
    n = len(corr)
    lado = max(5.0, 0.42 * n + 2)
    fig, ax = plt.subplots(figsize=(lado, lado * 0.9))
    im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(n), corr.columns, rotation=90)
    ax.set_yticks(range(n), corr.columns)
    if anotar:
        for i in range(n):
            for j in range(n):
                ax.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title(titulo)
    guardar(fig, pasta, nome, criados)


def grafico_correlacao_com_y(df, d_vars, x_vars, y, pasta, criados):
    corr_y = pd.concat([df[d_vars + x_vars], y], axis=1).corr()["y"].drop("y").sort_values()
    fig, ax = plt.subplots(figsize=(7, 0.28 * len(corr_y) + 1.5))
    ax.barh(corr_y.index, corr_y.values, color=[AZUL if v >= 0 else LARANJA for v in corr_y.values])
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("Correlação com y")
    ax.set_title("Correlação de cada variável com y")
    guardar(fig, pasta, "08_correlacao_com_y", criados)


def grafico_taxa_por_d(desc_d, pasta, criados):
    taxa = desc_d["P(y=1 | d=1)"].sort_values()
    fig, ax = plt.subplots(figsize=(7, 0.3 * len(taxa) + 1.5))
    ax.barh(taxa.index, taxa.values, color=LARANJA)
    ax.set_xlabel("Proporção de produtos em promoção quando d=1")
    ax.set_title("Taxa de promoção em cada variável discreta")
    guardar(fig, pasta, "09_taxa_promocao_por_d", criados)


# ----------------------------------------------------------------------------- programa principal
def main():
    ap = argparse.ArgumentParser(description="Cria os gráficos de EDA a partir de um CSV.")
    ap.add_argument("ficheiro", help="caminho do CSV, por exemplo data/training.csv")
    ap.add_argument("--saida", help="pasta onde guardar os resultados (por defeito: graficos/<nome do ficheiro>)")
    args = ap.parse_args()

    caminho = Path(args.ficheiro)
    pasta = Path(args.saida) if args.saida else Path("graficos") / caminho.stem
    pasta.mkdir(parents=True, exist_ok=True)

    df, d_vars, x_vars, y = ler_dados(caminho)
    print(f"Ficheiro lido: {caminho}  ({'com' if y is not None else 'sem'} valores de y)")

    desc_d = tabelas(df, d_vars, x_vars, y, pasta)
    criados = []

    if y is not None:
        grafico_alvo(y, pasta, criados)
    else:
        print("\nO y está vazio neste ficheiro: os gráficos que usam o y são saltados.")
    grafico_histogramas(df, x_vars, pasta, criados)
    grafico_frequencia_d(desc_d, pasta, criados)
    grafico_boxplots(df, x_vars, pasta, criados)
    if y is not None:
        grafico_boxplots_por_classe(df, x_vars, y, pasta, criados)
        corr_x = pd.concat([df[x_vars], y], axis=1).corr()
        heatmap(corr_x, "Correlação: variáveis contínuas e y", pasta, "06_correlacao_x", criados)
    else:
        heatmap(df[x_vars].corr(), "Correlação entre as variáveis contínuas", pasta, "06_correlacao_x", criados)
    heatmap(df[d_vars + x_vars].corr(), "Correlação entre todas as variáveis", pasta, "07_correlacao_todas",
            criados, anotar=False)
    if y is not None:
        grafico_correlacao_com_y(df, d_vars, x_vars, y, pasta, criados)
        grafico_taxa_por_d(desc_d, pasta, criados)

    print(f"\n{len(criados)} gráficos criados em {pasta}/:")
    for nome in sorted(criados):
        print("  ", nome)


if __name__ == "__main__":
    main()
