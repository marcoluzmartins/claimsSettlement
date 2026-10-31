"""Gera séries FICTÍCIAS de preço mediano por m2, só para testar a app.

Os números não correspondem a nenhum concelho real. Substituir por dados do INE
(mesmo formato de colunas) antes de tirar qualquer conclusão.
"""
import csv
import random
from pathlib import Path

DESTINO = Path(__file__).resolve().parent.parent / "data" / "sample" / "preco_m2_concelho_SINTETICO.csv"

# nome, preço inicial €/m2, crescimento anual, ruído trimestral, transações (min, max)
CONCELHOS = [
    ("Exemplo-Litoral", 1400, 0.065, 0.012, (250, 450)),
    ("Exemplo-Interior", 650, 0.040, 0.020, (15, 40)),
    ("Exemplo-Metropole", 1100, 0.085, 0.010, (700, 1400)),
]


def gerar(semente=42):
    rng = random.Random(semente)
    for nome, preco, crescimento, ruido, (n_min, n_max) in CONCELHOS:
        for ano in range(2014, 2027):
            for tri in range(1, 5):
                if (ano, tri) > (2026, 2):
                    break
                yield nome, f"{ano}Q{tri}", round(preco), rng.randint(n_min, n_max)
                preco *= (1 + crescimento) ** 0.25 * (1 + rng.gauss(0, ruido))


if __name__ == "__main__":
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    with DESTINO.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["concelho", "trimestre", "preco_m2_mediano", "n_transacoes", "fonte"])
        for linha in gerar():
            w.writerow([*linha, "SINTETICO"])
    print(f"Escrito {DESTINO}")
