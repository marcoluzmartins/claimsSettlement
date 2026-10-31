"""Veredicto: preço pedido (ajustado à negociação) face à estimativa."""
from .models import Veredicto

SOBREVALORIZADO = "Sobrevalorizado"
ACEITAVEL = "Aceitável"
BOM_NEGOCIO = "Bom negócio"
PECHINCHA = "Pechincha"
INCONCLUSIVO = "Inconclusivo"


def avaliar_preco(anuncio, estimativa, config):
    preco_efetivo = anuncio.preco_pedido * (1 - config.margem_negociacao)
    razao = preco_efetivo / estimativa.central
    diferenca = razao - 1

    if razao > config.limite_sobrevalorizado:
        categoria = SOBREVALORIZADO
    elif razao >= config.limite_aceitavel_min:
        categoria = ACEITAVEL
    elif razao >= config.limite_pechincha:
        categoria = BOM_NEGOCIO
    else:
        categoria = PECHINCHA

    significativo = abs(diferenca) > estimativa.meia_amplitude
    notas = []

    if categoria == SOBREVALORIZADO and estimativa.extras_nao_valorizados:
        categoria = INCONCLUSIVO
        notas.append(
            "O preço parece alto, mas a estimativa ignora "
            + ", ".join(estimativa.extras_nao_valorizados)
            + ", que acrescentam valor. Não é possível dizer que está sobrevalorizado."
        )
    if categoria == PECHINCHA:
        notas.append(
            "Preço muito abaixo do esperado: confirme se não há anúncio falso, ónus, "
            "problemas estruturais ou obras por fazer."
        )
    if not significativo and categoria != INCONCLUSIVO:
        notas.append(
            f"A diferença ({diferenca:+.0%}) está dentro da margem de incerteza (±{estimativa.meia_amplitude:.0%}); "
            "a classificação é pouco fiável."
        )

    return Veredicto(
        categoria=categoria,
        razao=razao,
        preco_efetivo=preco_efetivo,
        diferenca_pct=diferenca,
        significativo=significativo,
        mensagem=" ".join(notas),
    )
