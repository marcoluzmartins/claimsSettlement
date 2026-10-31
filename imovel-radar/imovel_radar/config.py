"""Pressupostos do modelo.

Nenhum destes valores vem de fonte oficial: são pontos de partida a rever e
calibrar com dados reais. Todos podem ser substituídos por um ficheiro JSON
(ver Config.de_ficheiro).
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

# Orientação principal das divisões de estar (hemisfério norte).
FATORES_EXPOSICAO = {
    "N": 0.96, "NE": 0.97, "E": 1.00, "SE": 1.02,
    "S": 1.03, "SO": 1.02, "O": 1.00, "NO": 0.97,
}

FATORES_ACESSO = {"bom": 1.00, "razoavel": 0.95, "dificil": 0.88}


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

    # Fatores multiplicativos sobre o valor da casa.
    fatores_estado: dict = field(default_factory=lambda: dict(FATORES_ESTADO))
    fatores_exposicao: dict = field(default_factory=lambda: dict(FATORES_EXPOSICAO))
    fatores_acesso: dict = field(default_factory=lambda: dict(FATORES_ACESSO))
    idade_referencia: int = 30
    depreciacao_idade_anual: float = 0.002
    ajuste_qualidade_max: float = 0.06  # +-6% para nota 100/0

    # Componentes que somam valor. Em cada par, um valor absoluto (se definido)
    # tem prioridade sobre o fator relativo; se ambos forem None, o componente
    # fica fora da estimativa e é sinalizado.
    fator_anexos_m2: float = 0.35       # preço/m2 dos anexos, em fração do preço/m2 da casa
    piscina_fator_casa: float | None = 0.05   # piscina = 5% do valor da casa
    valor_piscina: float | None = None
    terreno_fator_m2: float | None = 0.05     # terreno = 5% do preço/m2 da casa, por m2
    terreno_eur_m2: float | None = None

    # Zonas semelhantes e histórico.
    n_zonas_semelhantes: int = 3
    trimestres_historico: int = 40

    # Previsão.
    crescimento_longo_prazo: float = 0.02  # nominal, ao ano
    decaimento_tendencia: float = 0.7      # peso da tendência recente a cada ano
    inflacao_anual: float = 0.02
    horizontes_anos: tuple = (5, 10, 20)

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
