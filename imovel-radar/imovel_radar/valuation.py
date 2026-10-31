"""Estimativa indicativa do valor de mercado de um imóvel."""
import math
from datetime import date

from .models import Estimativa
from .reference import DadosInsuficientes, cagr_anual, indice_de_data

MAX_TRIMESTRES_EXTRAPOLADOS = 4
N_TRANSACOES_ASSUMIDO = 20


def _confianca(meia_amplitude):
    if meia_amplitude < 0.15:
        return "alta"
    if meia_amplitude < 0.25:
        return "média"
    return "baixa"


def estimar(anuncio, referencia, config, data_avaliacao=None, qualidade=None):
    data_avaliacao = data_avaliacao or date.today()
    serie = referencia.serie(anuncio.concelho)
    ultimo = serie[-1]
    avisos = []

    # Preço mediano ao nível da data pedida: extrapola metade da tendência
    # recente, no máximo MAX_TRIMESTRES_EXTRAPOLADOS trimestres.
    preco_m2 = ultimo.preco_m2
    lacuna = min(max(indice_de_data(data_avaliacao) - ultimo.indice, 0), MAX_TRIMESTRES_EXTRAPOLADOS)
    if lacuna:
        try:
            tendencia, _ = cagr_anual(serie)
        except DadosInsuficientes:
            tendencia = 0.0
        preco_m2 *= math.exp(0.5 * math.log1p(tendencia) / 4 * lacuna)
        avisos.append(
            f"Último dado em {ultimo.rotulo}; o preço foi extrapolado {lacuna} trimestre(s) com metade da tendência recente."
        )

    if anuncio.estado not in config.fatores_estado:
        raise ValueError(
            f"Estado desconhecido: {anuncio.estado!r}. Válidos: {sorted(config.fatores_estado)}"
        )
    f_estado = config.fatores_estado[anuncio.estado]

    f_idade = 1.0
    if anuncio.ano_construcao:
        idade = data_avaliacao.year - anuncio.ano_construcao
        f_idade = 1 - config.depreciacao_idade_anual * (idade - config.idade_referencia)
        f_idade = min(max(f_idade, 0.85), 1.10)

    f_qualidade = 1.0
    if qualidade is not None:
        f_qualidade = 1 + (qualidade.nota - 50) / 50 * config.ajuste_qualidade_max

    casa = anuncio.area_util_m2 * preco_m2 * f_idade * f_estado * f_qualidade
    terreno = piscina = 0.0
    nao_valorizados = []

    if anuncio.area_terreno_m2 > 0:
        if config.terreno_eur_m2 is not None:
            terreno = anuncio.area_terreno_m2 * config.terreno_eur_m2
        else:
            nao_valorizados.append(f"terreno de {anuncio.area_terreno_m2:g} m2")
    if "piscina" in anuncio.extras:
        if config.valor_piscina is not None:
            piscina = config.valor_piscina
        else:
            nao_valorizados.append("piscina")

    outros = sorted(set(anuncio.extras) - {"piscina"})
    if outros:
        avisos.append(f"Extras não modelados: {', '.join(outros)}.")
    if nao_valorizados:
        avisos.append(
            "Sem valor definido para: " + ", ".join(nao_valorizados)
            + ". A estimativa pode estar subavaliada."
        )

    n = ultimo.n_transacoes
    if n <= 0:
        avisos.append(f"Número de transações desconhecido; assumido {N_TRANSACOES_ASSUMIDO}.")
        n = N_TRANSACOES_ASSUMIDO
    penalizacao_extras = 0.10 if nao_valorizados else 0.0
    meia = math.sqrt(0.08**2 + (0.6 / math.sqrt(n)) ** 2 + penalizacao_extras**2)

    central = casa + terreno + piscina
    return Estimativa(
        central=central,
        minimo=central * (1 - meia),
        maximo=central * (1 + meia),
        preco_m2_base=preco_m2,
        trimestre_base=ultimo.rotulo,
        n_transacoes=ultimo.n_transacoes,
        meia_amplitude=meia,
        confianca=_confianca(meia),
        extras_nao_valorizados=nao_valorizados,
        avisos=avisos,
        componentes={
            "casa": casa, "terreno": terreno, "piscina": piscina,
            "fator_estado": f_estado, "fator_idade": f_idade, "fator_qualidade": f_qualidade,
        },
    )
