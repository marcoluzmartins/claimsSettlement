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
    if pd.isna(ramo):
        return ramo
    valor = str(ramo).strip()
    return MAPEAMENTO_RAMO.get(valor, valor)


def limite_regularizacao(ramo):
    return LIMITES.get(normalizar_ramo(ramo))


def cumpre_prazo(ramo, dias_resolucao):
    limite = limite_regularizacao(ramo)
    if limite is None or pd.isna(dias_resolucao):
        return True
    return dias_resolucao <= limite

class Sinistro:
    def __init__(self, id_sinistro, ramo, estado, valor_reclamado):
        self.id_sinistro = id_sinistro
        self.ramo = ramo
        self.estado = estado
        self.valor_reclamado = valor_reclamado

    def valor_pendente(self):
        return self.valor_reclamado if self.estado == "Pendente" else 0
