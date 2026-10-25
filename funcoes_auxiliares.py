"""Regras de negócio da Proposta 10: normalização de ramos e prazos de regularização."""
import pandas as pd

MAPEAMENTO_RAMO = {
    "Automovel": "Automovel",
    "Automóvel": "Automovel",
    "Habitacao": "Habitacao",
    "Habitação": "Habitacao",
    "Viagem": "Viagem",
    "Responsabilidade Civil": "ResponsabilidadeCivil",
    "ResponsabilidadeCivil": "ResponsabilidadeCivil",
}

LIMITES = {
    "Automovel": 25,
    "Habitacao": 25,
    "Viagem": 10,
    "ResponsabilidadeCivil": 35,
}


def normalizar_ramo(ramo):
    """Devolve o nome padrão do ramo (sem espaços nas pontas nem acentos)."""
    if pd.isna(ramo):
        return ramo
    valor = str(ramo).strip()
    return MAPEAMENTO_RAMO.get(valor, valor)


def limite_regularizacao(ramo):
    """Devolve o limite em dias do ramo, ou None se o ramo for desconhecido."""
    return LIMITES.get(normalizar_ramo(ramo))


def cumpre_prazo(ramo, dias_resolucao):
    """True se os dias não excedem o limite do ramo.

    Pressuposto: sem limite ou sem dias, não se assinala atraso.
    """
    limite = limite_regularizacao(ramo)
    if limite is None or pd.isna(dias_resolucao):
        return True
    return dias_resolucao <= limite
