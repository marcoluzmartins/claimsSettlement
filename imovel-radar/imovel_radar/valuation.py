"""Estimativa indicativa do valor de mercado de um imóvel."""
import math
from datetime import date

from .models import Estimativa
from .reference import DadosInsuficientes, cagr_anual, indice_de_data

MAX_TRIMESTRES_EXTRAPOLADOS = 4
N_TRANSACOES_ASSUMIDO = 20
INCERTEZA_EXTRAS_ESTIMADOS = 0.05   # componentes valorizados por fator, não medidos
INCERTEZA_EXTRAS_EM_FALTA = 0.10    # componentes que ficaram de fora


def _confianca(meia_amplitude):
    if meia_amplitude < 0.15:
        return "alta"
    if meia_amplitude < 0.25:
        return "média"
    return "baixa"


def _preco_m2_na_data(serie, data_avaliacao, avisos):
    """Último preço mediano, extrapolado com metade da tendência recente (máx. 4 trimestres)."""
    ultimo = serie[-1]
    lacuna = min(max(indice_de_data(data_avaliacao) - ultimo.indice, 0), MAX_TRIMESTRES_EXTRAPOLADOS)
    if not lacuna:
        return ultimo.preco_m2
    try:
        tendencia, _ = cagr_anual(serie)
    except DadosInsuficientes:
        tendencia = 0.0
    avisos.append(
        f"Último dado em {ultimo.rotulo}; o preço foi extrapolado {lacuna} trimestre(s) com metade da tendência recente."
    )
    return ultimo.preco_m2 * math.exp(0.5 * math.log1p(tendencia) / 4 * lacuna)


def estimar(anuncio, referencia, config, data_avaliacao=None, qualidade=None):
    data_avaliacao = data_avaliacao or date.today()
    serie = referencia.serie(anuncio.concelho)
    ultimo = serie[-1]
    avisos = []
    preco_m2 = _preco_m2_na_data(serie, data_avaliacao, avisos)

    if anuncio.estado not in config.fatores_estado:
        raise ValueError(
            f"Estado desconhecido: {anuncio.estado!r}. Válidos: {sorted(config.fatores_estado)}"
        )
    f_idade = 1.0
    if anuncio.ano_construcao:
        idade = data_avaliacao.year - anuncio.ano_construcao
        f_idade = 1 - config.depreciacao_idade_anual * (idade - config.idade_referencia)
        f_idade = min(max(f_idade, 0.85), 1.10)

    base = anuncio.area_util_m2 * preco_m2
    atual, contribuicoes = base, []

    def aplicar(nome, fator):
        nonlocal atual
        delta = atual * (fator - 1)
        atual *= fator
        if abs(delta) >= 0.5:
            contribuicoes.append({"fator": nome, "valor": delta})

    aplicar("Idade do edifício", f_idade)
    aplicar("Estado de conservação", config.fatores_estado[anuncio.estado])
    if anuncio.exposicao_solar:
        aplicar(f"Exposição solar ({anuncio.exposicao_solar})", config.fatores_exposicao[anuncio.exposicao_solar])
    aplicar("Acessos", config.fatores_acesso[anuncio.acesso])
    if qualidade is not None:
        aplicar("Apreciação (fotos/descrição)", 1 + (qualidade.nota - 50) / 50 * config.ajuste_qualidade_max)
    casa = atual

    nao_valorizados, estimados, adicionais = [], False, 0.0

    def somar(nome, valor, por_fator):
        nonlocal estimados, adicionais
        contribuicoes.append({"fator": nome, "valor": valor})
        adicionais += valor
        estimados = estimados or por_fator

    if anuncio.anexos:
        if anuncio.area_anexos_m2 > 0:
            somar("Anexos", anuncio.area_anexos_m2 * preco_m2 * config.fator_anexos_m2, True)
        else:
            nao_valorizados.append("anexos (sem área indicada)")
    if "piscina" in anuncio.extras:
        if config.valor_piscina is not None:
            somar("Piscina", config.valor_piscina, False)
        elif config.piscina_fator_casa is not None:
            somar("Piscina", casa * config.piscina_fator_casa, True)
        else:
            nao_valorizados.append("piscina")
    if anuncio.area_terreno_m2 > 0:
        if config.terreno_eur_m2 is not None:
            somar("Terreno", anuncio.area_terreno_m2 * config.terreno_eur_m2, False)
        elif config.terreno_fator_m2 is not None:
            somar("Terreno", anuncio.area_terreno_m2 * preco_m2 * config.terreno_fator_m2, True)
        else:
            nao_valorizados.append(f"terreno de {anuncio.area_terreno_m2:g} m2")

    outros = sorted(set(anuncio.extras) - {"piscina"})
    if outros:
        avisos.append(f"Extras não modelados: {', '.join(outros)}.")
    if nao_valorizados:
        avisos.append(
            "Sem valor definido para: " + ", ".join(nao_valorizados)
            + ". A estimativa pode estar subavaliada."
        )
    if estimados:
        avisos.append(
            "Piscina, terreno e anexos foram valorizados com fatores genéricos (pressupostos a calibrar), "
            "não com comparáveis reais."
        )
    if anuncio.quartos:
        m2_por_quarto = anuncio.area_util_m2 / anuncio.quartos
        if m2_por_quarto < 12 or m2_por_quarto > 60:
            avisos.append(
                f"{anuncio.quartos} quartos para {anuncio.area_util_m2:g} m2 ({m2_por_quarto:.0f} m2 por quarto) "
                "é pouco habitual; confirme os dados."
            )

    n = ultimo.n_transacoes
    if n <= 0:
        avisos.append(f"Número de transações desconhecido; assumido {N_TRANSACOES_ASSUMIDO}.")
        n = N_TRANSACOES_ASSUMIDO
    extras_incerteza = (
        INCERTEZA_EXTRAS_EM_FALTA if nao_valorizados else INCERTEZA_EXTRAS_ESTIMADOS if estimados else 0.0
    )
    meia = math.sqrt(0.08**2 + (0.6 / math.sqrt(n)) ** 2 + extras_incerteza**2)

    central = casa + adicionais
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
        componentes={"base_mediana": base, "casa": casa, "contribuicoes": contribuicoes},
    )
