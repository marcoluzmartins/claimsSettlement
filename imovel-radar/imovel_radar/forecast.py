"""Projeção de valorização a médio e longo prazo, em cenários.

Não é uma previsão: parte da tendência histórica da zona e faz-a convergir
para um crescimento de longo prazo. Os cenários deslocam o crescimento anual
em +-meio desvio-padrão da variação homóloga histórica.
"""
from .models import CenarioProjecao, Projecao
from .reference import DadosInsuficientes, cagr_anual, volatilidade_anual

VOLATILIDADE_POR_OMISSAO = 0.05
DESLOCAMENTO_MAX = 0.04


def _crescimento_anual(ano, g_historico, config, deslocamento):
    g = config.crescimento_longo_prazo + (g_historico - config.crescimento_longo_prazo) * (
        config.decaimento_tendencia ** (ano - 1)
    )
    return max(g + deslocamento, -0.5)


def _cenario(nome, deslocamento, valor_atual, custo_total, g_historico, config):
    horizonte_max = max(config.horizontes_anos)
    valor, taxas, trajetoria = valor_atual, [], {0: valor_atual}
    for ano in range(1, horizonte_max + 1):
        g = _crescimento_anual(ano, g_historico, config, deslocamento)
        taxas.append(g)
        valor *= 1 + g
        trajetoria[ano] = valor

    valores, total, anual, real = {}, {}, {}, {}
    for h in config.horizontes_anos:
        liquido = trajetoria[h] * (1 - config.custos_venda_pct)
        t = liquido / custo_total - 1
        a = (1 + t) ** (1 / h) - 1 if t > -1 else -1.0
        valores[h], total[h], anual[h] = trajetoria[h], t, a
        real[h] = (1 + a) / (1 + config.inflacao_anual) - 1
    return CenarioProjecao(
        nome=nome,
        crescimento_anual_medio=sum(taxas) / len(taxas),
        valores=valores,
        retorno_liquido_total=total,
        retorno_liquido_anual=anual,
        retorno_real_anual=real,
        trajetoria=trajetoria,
    )


def projetar(estimativa, preco_efetivo, serie, config):
    """Cenários de valor de mercado e retorno líquido para quem comprar a `preco_efetivo`."""
    g_historico, anos = cagr_anual(serie)
    avisos = []
    try:
        vol = volatilidade_anual(serie)
    except DadosInsuficientes:
        vol = VOLATILIDADE_POR_OMISSAO
        avisos.append("Volatilidade não medida (histórico curto); assumido 5%.")
    desloc = min(0.5 * vol, DESLOCAMENTO_MAX)

    custo_total = preco_efetivo * (1 + config.custos_compra_pct)
    cenarios = [
        _cenario(nome, d, estimativa.central, custo_total, g_historico, config)
        for nome, d in (("pessimista", -desloc), ("base", 0.0), ("otimista", desloc))
    ]

    avisos.append(
        "Cenários, não previsões: o passado não garante o futuro. O retorno não inclui "
        "rendas, IMI, condomínio, obras nem impostos sobre a mais-valia."
    )
    if max(config.horizontes_anos) >= 20:
        avisos.append("A 20 anos a incerteza é muito elevada (política, juros, demografia, obras na zona): use-o só como ordem de grandeza.")
    if estimativa.confianca == "baixa":
        avisos.append("A estimativa de partida tem confiança baixa; os valores projetados herdam essa incerteza.")
    retorno_valido = not estimativa.extras_nao_valorizados
    if not retorno_valido:
        avisos.append(
            "Retorno omitido: a estimativa ignora "
            + ", ".join(estimativa.extras_nao_valorizados)
            + ", por isso comparar o valor projetado com o preço pago daria um resultado enganador. "
            "Defina terreno_eur_m2 / valor_piscina na configuração."
        )
    return Projecao(
        cagr_historico=g_historico,
        volatilidade=vol,
        anos_historico=anos,
        cenarios=cenarios,
        retorno_valido=retorno_valido,
        avisos=avisos,
    )
