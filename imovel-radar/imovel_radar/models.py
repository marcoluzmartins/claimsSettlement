"""Estruturas de dados partilhadas."""
from dataclasses import dataclass, field


@dataclass
class Anuncio:
    concelho: str
    preco_pedido: float
    area_util_m2: float
    tipologia: str = ""
    ano_construcao: int | None = None
    estado: str = "bom"
    area_terreno_m2: float = 0.0
    extras: tuple = ()
    descricao: str = ""
    fotos: tuple = ()
    titulo: str = ""

    @classmethod
    def de_dict(cls, dados):
        obrigatorios = ("concelho", "preco_pedido", "area_util_m2")
        em_falta = [c for c in obrigatorios if dados.get(c) in (None, "")]
        if em_falta:
            raise ValueError(f"Campos obrigatórios em falta: {em_falta}")
        dados = dict(dados)
        dados["extras"] = tuple(str(e).strip().lower() for e in dados.get("extras", ()))
        dados["fotos"] = tuple(dados.get("fotos", ()))
        validos = set(cls.__dataclass_fields__)
        desconhecidos = set(dados) - validos
        if desconhecidos:
            raise ValueError(f"Campos desconhecidos no anúncio: {sorted(desconhecidos)}")
        anuncio = cls(**dados)
        if anuncio.preco_pedido <= 0 or anuncio.area_util_m2 <= 0:
            raise ValueError("preco_pedido e area_util_m2 têm de ser positivos")
        return anuncio


@dataclass
class Estimativa:
    central: float
    minimo: float
    maximo: float
    preco_m2_base: float
    trimestre_base: str
    n_transacoes: int
    meia_amplitude: float
    confianca: str
    extras_nao_valorizados: list = field(default_factory=list)
    avisos: list = field(default_factory=list)
    componentes: dict = field(default_factory=dict)


@dataclass
class Veredicto:
    categoria: str
    razao: float            # preço efetivo / estimativa central
    preco_efetivo: float
    diferenca_pct: float    # (efetivo - central) / central
    significativo: bool     # diferença maior que a margem de incerteza
    mensagem: str


@dataclass
class CenarioProjecao:
    nome: str
    crescimento_anual_medio: float
    valores: dict           # horizonte (anos) -> valor de mercado projetado
    retorno_liquido_total: dict
    retorno_liquido_anual: dict
    retorno_real_anual: dict


@dataclass
class Projecao:
    cagr_historico: float
    volatilidade: float
    anos_historico: float
    cenarios: list
    retorno_valido: bool = True   # falso se a estimativa ignora extras que valem dinheiro
    avisos: list = field(default_factory=list)


@dataclass
class Qualidade:
    nota: float             # 0-100, 50 = neutro
    resumo: str
    positivos: list = field(default_factory=list)
    negativos: list = field(default_factory=list)
    origem: str = "heuristica"
