"""Séries históricas de preço mediano por m2 e estatísticas derivadas.

Formato do CSV (o mesmo para dados do INE depois de descarregados e normalizados):
    concelho,trimestre,preco_m2_mediano,n_transacoes,fonte
    Exemplo,2024Q3,1500,120,INE
"""
import csv
import math
import re
import statistics
import unicodedata
from dataclasses import dataclass
from pathlib import Path


class DadosInsuficientes(Exception):
    """Série curta demais para calcular a estatística pedida."""


class ConcelhoDesconhecido(KeyError):
    pass


_RE_TRIMESTRE = re.compile(r"^\s*(\d{4})\s*[-_ ]?\s*[QqTt]([1-4])\s*$")


def normalizar_nome(nome):
    sem_acentos = "".join(
        c for c in unicodedata.normalize("NFKD", str(nome)) if not unicodedata.combining(c)
    )
    return " ".join(sem_acentos.casefold().split())


def parse_trimestre(texto):
    m = _RE_TRIMESTRE.match(str(texto))
    if not m:
        raise ValueError(f"Trimestre inválido: {texto!r} (esperado AAAAQn, ex.: 2024Q3)")
    return int(m.group(1)), int(m.group(2))


@dataclass(frozen=True)
class Ponto:
    ano: int
    trimestre: int
    preco_m2: float
    n_transacoes: int = 0

    @property
    def indice(self):
        return self.ano * 4 + self.trimestre - 1

    @property
    def rotulo(self):
        return f"{self.ano}Q{self.trimestre}"


def indice_de_data(data):
    return data.year * 4 + (data.month - 1) // 3


class Referencia:
    def __init__(self, series, sintetica=False):
        self._series = {normalizar_nome(k): (k, sorted(v, key=lambda p: p.indice)) for k, v in series.items()}
        self.sintetica = sintetica

    @classmethod
    def carregar(cls, caminho):
        series, sintetica = {}, False
        with Path(caminho).open(newline="", encoding="utf-8") as f:
            for linha in csv.DictReader(f):
                if not (linha.get("preco_m2_mediano") or "").strip():
                    continue
                ano, tri = parse_trimestre(linha["trimestre"])
                ponto = Ponto(
                    ano, tri,
                    float(linha["preco_m2_mediano"]),
                    int(float(linha.get("n_transacoes") or 0)),
                )
                series.setdefault(linha["concelho"].strip(), []).append(ponto)
                if "sint" in (linha.get("fonte") or "").casefold():
                    sintetica = True
        if not series:
            raise ValueError(f"Sem dados em {caminho}")
        return cls(series, sintetica)

    def concelhos(self):
        return sorted(nome for nome, _ in self._series.values())

    def serie(self, concelho):
        try:
            return self._series[normalizar_nome(concelho)][1]
        except KeyError:
            raise ConcelhoDesconhecido(
                f"Concelho sem dados: {concelho!r}. Disponíveis: {', '.join(self.concelhos())}"
            ) from None


def cagr_anual(serie, anos=10):
    """Crescimento anual composto do preço mediano nos últimos `anos` anos.

    Devolve (taxa, anos efetivamente usados).
    """
    ultimo = serie[-1]
    alvo = ultimo.indice - 4 * anos
    base = next(p for p in serie if p.indice >= alvo)
    trimestres = ultimo.indice - base.indice
    if trimestres < 8:
        raise DadosInsuficientes("São precisos pelo menos 2 anos de histórico.")
    return (ultimo.preco_m2 / base.preco_m2) ** (4 / trimestres) - 1, trimestres / 4


def volatilidade_anual(serie):
    """Desvio-padrão das variações homólogas (log) do preço mediano."""
    por_indice = {p.indice: p.preco_m2 for p in serie}
    variacoes = [
        math.log(p.preco_m2 / por_indice[p.indice - 4])
        for p in serie
        if p.indice - 4 in por_indice
    ]
    if len(variacoes) < 8:
        raise DadosInsuficientes("Histórico insuficiente para medir a volatilidade.")
    return statistics.stdev(variacoes)
