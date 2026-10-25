"""Proposta 10 - Regularização de sinistros."""

from funcoes_auxiliares import (
    normalizar_ramo,
    limite_regularizacao,
    cumpre_prazo,
    Sinistro,
)
from pathlib import Path
import pandas as pd


# Pseudocódigo da regra central (fora_prazo):
#   limite <- limite_regularizacao(ramo)
#   SE limite ou dias_resolucao em falta: considerar dentro do prazo
#   cumpre_prazo <- dias_resolucao <= limite
#   fora_prazo <- NÃO cumpre_prazo

COL_ID = "sinistro"
COL_RAMO = "ramo"
COL_CANAL = "canal"
COL_ESTADO = "estado"
COL_RECLAMADO = "valor_reclamado"
COL_REGULARIZADO = "valor_regularizado"
COL_DIAS = "dias_resolucao"


def main():
    print("\nTarefa 1: Leitura dos dados do ficheiro csv\n")
    directorio = Path(__file__).resolve().parent
    csv_file = directorio / "dados_trabalho_10_seguros.csv"

    if not csv_file.exists():
        raise FileNotFoundError(
            f"Ficheiro de dados não encontrado: {csv_file}\n"
        )
    print(f"Ficheiro de dados encontrado: {csv_file}\n")
    df = pd.read_csv(csv_file)

    print("\nTarefa 1: Verificação da qualidade dos dados\n")
    print(df.dtypes)
    print(df.isna().sum())
    print("Duplicados:", df.duplicated().sum())
    print("Ramos:", df[COL_RAMO].unique().tolist())
    print("Canais:", df[COL_CANAL].unique().tolist())
    print("Estados:", df[COL_ESTADO].unique().tolist())

    df[COL_RAMO] = df[COL_RAMO].map(normalizar_ramo)
    df[COL_RECLAMADO] = pd.to_numeric(
        df[COL_RECLAMADO], errors="coerce").fillna(0)
    df[COL_REGULARIZADO] = pd.to_numeric(
        df[COL_REGULARIZADO], errors="coerce").fillna(0)
    df[COL_DIAS] = pd.to_numeric(df[COL_DIAS], errors="coerce")
    print("\nFeita Tarefa 1\n")

    print("\nTarefa 2: Criação de coluna valor_pendente\n")
    df["valor_pendente"] = df[COL_RECLAMADO].where(
        df[COL_ESTADO].astype(str).str.strip().eq("Pendente"), 0)
    print("Total pendente:", df["valor_pendente"].sum())
    print("\nFeita Tarefa 2\n")

    print("\nTarefa 3: Criação de coluna fora_prazo\n")
    df["limite"] = df[COL_RAMO].map(limite_regularizacao)
    df["fora_prazo"] = [
        not cumpre_prazo(ramo, dias)
        for ramo, dias in zip(df[COL_RAMO], df[COL_DIAS])
    ]
    print("Sinistros fora de prazo:", df["fora_prazo"].sum(), "de", len(df))
    print("\nFeita Tarefa 3\n")

    print("\nTarefa 4: Resumo \n")
    resumo = df.groupby(COL_RAMO).agg(
        n_sinistros=(COL_ID, "count"),
        valor_reclamado=(COL_RECLAMADO, "sum"),
        valor_regularizado=(COL_REGULARIZADO, "sum"),
        valor_pendente=("valor_pendente", "sum"),
        dias_medios=(COL_DIAS, "mean"),
        pct_fora_prazo=("fora_prazo", "mean"),
    )
    resumo["dias_medios"] = resumo["dias_medios"].round(2)
    resumo["pct_fora_prazo"] = resumo["pct_fora_prazo"] * 100
    resumo["pct_fora_prazo"] = resumo["pct_fora_prazo"].round(2)

    print(resumo)

    print("\nFeita Tarefa 4\n")

    print("\nTarefa 5: Demonstração da classe Sinistro \n")

    linha = df[df[COL_ESTADO].astype(str).str.strip().eq("Pendente")].iloc[0]
    sinistro = Sinistro(
        linha[COL_ID], linha[COL_RAMO], linha[COL_ESTADO], linha[COL_RECLAMADO]
    )
    print(f"Sinistro: {sinistro.id_sinistro}, Valor Pendente: {sinistro.valor_pendente()}")
    print("\nFeita Tarefa 5\n")

    print("\nTarefa 6: Exportação dos prioritários\n")
    prioritarios = df[(df[COL_ESTADO].astype(str).str.strip().eq("Pendente")) | df["fora_prazo"]]
    prioritarios = prioritarios.sort_values(
        by=["valor_pendente", COL_DIAS], ascending=[False, False]
    )
    prioritarios.to_csv(directorio / "sinistros_prioritarios.csv", index=False)
    print(f"Ficheiro foi criado em {directorio / 'sinistros_prioritarios.csv'} com sucesso!\n")
    print("\nFeita Tarefa 6\n")

    print("\nApoio às questões de análise\n")
    print(df[COL_CANAL].value_counts(normalize=True))
    print(prioritarios[COL_CANAL].value_counts(normalize=True))
    print(pd.crosstab(prioritarios[COL_CANAL], prioritarios[COL_RAMO]))


if __name__ == "__main__":
    main()
