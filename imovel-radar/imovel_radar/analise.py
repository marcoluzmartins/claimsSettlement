"""Junta estimativa, veredicto, padrão da zona, histórico e projeção numa só análise."""
import dataclasses
import statistics
from dataclasses import dataclass
from datetime import date

from .forecast import projetar
from .models import Estimativa, Padrao, Projecao, Qualidade, Veredicto
from .reference import DadosInsuficientes, cagr_anual
from .valuation import estimar
from .verdict import avaliar_preco

MARGEM_MINIMA_PADRAO = 0.10


@dataclass
class Analise:
    estimativa: Estimativa
    veredicto: Veredicto
    padrao: Padrao
    historico: dict
    projecao: Projecao
    qualidade: Qualidade | None
    dados_sinteticos: bool


def _crescimento(serie):
    try:
        return cagr_anual(serie, 5)[0]
    except DadosInsuficientes:
        return None


def calcular_padrao(anuncio, estimativa, referencia, config):
    """Compara o preço/m2 pedido com a mediana da zona e de zonas semelhantes.

    É uma comparação bruta de €/m2: não desconta piscina, terreno, anexos nem
    estado, por isso um imóvel com extras tende a ficar acima do padrão.
    """
    pedido = anuncio.preco_pedido / anuncio.area_util_m2
    zona = estimativa.preco_m2_base
    semelhantes = []
    for nome, distancia in referencia.zonas_semelhantes(anuncio.concelho, config.n_zonas_semelhantes):
        serie = referencia.serie(nome)
        semelhantes.append({
            "concelho": nome,
            "preco_m2": serie[-1].preco_m2,
            "crescimento": _crescimento(serie),
            "distancia": distancia,
        })
    mediana_sem = statistics.median(s["preco_m2"] for s in semelhantes) if semelhantes else None
    dif_zona = pedido / zona - 1
    dif_sem = pedido / mediana_sem - 1 if mediana_sem else None

    limite = max(estimativa.meia_amplitude, MARGEM_MINIMA_PADRAO)
    dentro = abs(dif_zona) <= limite
    if dentro:
        leitura = f"O preço por m2 está dentro do padrão da zona ({dif_zona:+.0%} face à mediana)."
    elif dif_zona > 0:
        leitura = f"O preço por m2 está {dif_zona:.0%} acima da mediana da zona."
    else:
        leitura = f"O preço por m2 está {-dif_zona:.0%} abaixo da mediana da zona."
    if not dentro and dif_zona > 0 and (anuncio.extras or anuncio.anexos or anuncio.area_terreno_m2 > 0):
        leitura += " Parte da diferença pode vir de piscina, anexos ou terreno, que a comparação bruta não desconta."
    return Padrao(
        preco_m2_pedido=pedido,
        mediana_zona=zona,
        diferenca_vs_zona=dif_zona,
        semelhantes=semelhantes,
        mediana_semelhantes=mediana_sem,
        diferenca_vs_semelhantes=dif_sem,
        dentro_do_padrao=dentro,
        leitura=leitura,
    )


def construir_historico(concelho, semelhantes, referencia, trimestres):
    """Preço mediano/m2 da zona e das semelhantes nos últimos trimestres, com índice base 100."""
    serie_zona = referencia.serie(concelho)[-trimestres:]
    indices = [p.indice for p in serie_zona]
    series = {referencia.nome(concelho): {p.indice: p.preco_m2 for p in serie_zona}}
    for s in semelhantes:
        series[s["concelho"]] = {p.indice: p.preco_m2 for p in referencia.serie(s["concelho"])}

    precos, base100 = {}, {}
    for nome, por_indice in series.items():
        valores = [por_indice.get(i) for i in indices]
        primeiro = next((v for v in valores if v is not None), None)
        precos[nome] = valores
        base100[nome] = [None if v is None or not primeiro else v / primeiro * 100 for v in valores]
    rotulos = [f"{i // 4}Q{i % 4 + 1}" for i in indices]
    return {"zona": referencia.nome(concelho), "trimestres": rotulos, "preco_m2": precos, "indice_base_100": base100}


def analisar(anuncio, referencia, config, data_avaliacao=None, qualidade=None):
    estimativa = estimar(anuncio, referencia, config, data_avaliacao, qualidade)
    veredicto = avaliar_preco(anuncio, estimativa, config)
    padrao = calcular_padrao(anuncio, estimativa, referencia, config)
    historico = construir_historico(anuncio.concelho, padrao.semelhantes, referencia, config.trimestres_historico)
    projecao = projetar(estimativa, veredicto.preco_efetivo, referencia.serie(anuncio.concelho), config)
    return Analise(estimativa, veredicto, padrao, historico, projecao, qualidade, referencia.sintetica)


def analise_para_dict(analise, anuncio, data_avaliacao=None):
    """Estrutura serializável em JSON, usada pela API e pela app."""
    d = dataclasses.asdict(analise)
    cenarios = {c["nome"]: c["trajetoria"] for c in d["projecao"]["cenarios"]}
    anos = sorted(next(iter(cenarios.values())))
    d["projecao"]["grafico"] = {"anos": anos, **{n: [t[a] for a in anos] for n, t in cenarios.items()}}
    d["anuncio"] = dataclasses.asdict(anuncio)
    d["meta"] = {"data_referencia": (data_avaliacao or date.today()).isoformat(), "sintetico": analise.dados_sinteticos}
    return d
