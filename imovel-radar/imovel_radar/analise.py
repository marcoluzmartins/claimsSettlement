"""Junta estimativa, veredicto e projeção numa só análise."""
from dataclasses import dataclass

from .forecast import projetar
from .models import Estimativa, Projecao, Qualidade, Veredicto
from .valuation import estimar
from .verdict import avaliar_preco


@dataclass
class Analise:
    estimativa: Estimativa
    veredicto: Veredicto
    projecao: Projecao
    qualidade: Qualidade | None
    dados_sinteticos: bool


def analisar(anuncio, referencia, config, data_avaliacao=None, qualidade=None):
    estimativa = estimar(anuncio, referencia, config, data_avaliacao, qualidade)
    veredicto = avaliar_preco(anuncio, estimativa, config)
    projecao = projetar(estimativa, veredicto.preco_efetivo, referencia.serie(anuncio.concelho), config)
    return Analise(estimativa, veredicto, projecao, qualidade, referencia.sintetica)
