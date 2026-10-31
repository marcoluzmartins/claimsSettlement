"""Pressupostos do modelo.

Nenhum destes valores vem de fonte oficial: são pontos de partida a rever.
Todos podem ser substituídos por um ficheiro JSON (ver Config.de_ficheiro).
"""
import json
from dataclasses import dataclass, field, fields
from pathlib import Path

FATORES_ESTADO = {
    "novo": 1.10,
    "renovado": 1.06,
    "bom": 1.00,
    "razoavel": 0.93,
    "para_recuperar": 0.72,
}


@dataclass(frozen=True)
class Config:
    # Preço pedido vs. preço de venda: o INE mede vendas, os anúncios mostram pedidos.
    margem_negociacao: float = 0.05

    # Impostos e despesas de compra (IMT, imposto de selo, registos, notário).
    # Confirmar as tabelas em vigor; depende do tipo de compra.
    custos_compra_pct: float = 0.07
    custos_venda_pct: float = 0.0

    # Limites do veredicto, sobre preço efetivo / estimativa central.
    limite_sobrevalorizado: float = 1.10
    limite_aceitavel_min: float = 0.90
    limite_pechincha: float = 0.75

    # Ajustes da estimativa.
    fatores_estado: dict = field(default_factory=lambda: dict(FATORES_ESTADO))
    idade_referencia: int = 30
    depreciacao_idade_anual: float = 0.002
    ajuste_qualidade_max: float = 0.06  # +-6% para nota 100/0
    # Sem valor definido, terreno e piscina não entram na estimativa e ficam sinalizados.
    terreno_eur_m2: float | None = None
    valor_piscina: float | None = None

    # Previsão.
    crescimento_longo_prazo: float = 0.02  # nominal, ao ano
    decaimento_tendencia: float = 0.7      # peso da tendência recente a cada ano
    inflacao_anual: float = 0.02
    horizontes_anos: tuple = (3, 5, 10)

    @classmethod
    def de_ficheiro(cls, caminho):
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
        validos = {f.name for f in fields(cls)}
        desconhecidos = set(dados) - validos
        if desconhecidos:
            raise ValueError(f"Parâmetros desconhecidos: {sorted(desconhecidos)}")
        if "horizontes_anos" in dados:
            dados["horizontes_anos"] = tuple(dados["horizontes_anos"])
        return cls(**dados)
