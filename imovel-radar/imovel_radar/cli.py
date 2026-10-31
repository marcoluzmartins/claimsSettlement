"""Linha de comandos: python -m imovel_radar anuncio.json"""
import argparse
import dataclasses
import json
import sys
from datetime import date
from pathlib import Path

from .analise import analisar
from .config import Config
from .models import Anuncio
from .quality import QualidadeIAErro, pontuar_com_ia, pontuar_descricao
from .reference import ConcelhoDesconhecido, Referencia

DADOS_POR_OMISSAO = Path(__file__).resolve().parent.parent / "data" / "sample" / "preco_m2_concelho_SINTETICO.csv"


def eur(valor):
    return f"{valor:,.0f}".replace(",", " ") + " €"


def pct(valor, sinal=False):
    return f"{valor:+.1%}" if sinal else f"{valor:.1%}"


def formatar(anuncio, a, config, data):
    e, v, p = a.estimativa, a.veredicto, a.projecao
    linhas = []
    if a.dados_sinteticos:
        linhas += ["!! DADOS SINTÉTICOS DE EXEMPLO - os números abaixo NÃO são reais !!", ""]
    linhas += [
        f"Imóvel: {anuncio.titulo or anuncio.tipologia or 'sem título'} | {anuncio.concelho} | "
        f"{anuncio.area_util_m2:g} m2 úteis | pedido {eur(anuncio.preco_pedido)}",
        f"Data de referência: {data.isoformat()}",
        "",
        "ESTIMATIVA INDICATIVA (não é uma avaliação oficial)",
        f"  Valor central: {eur(e.central)}   intervalo: {eur(e.minimo)} a {eur(e.maximo)}",
        f"  Confiança: {e.confianca} (±{pct(e.meia_amplitude)}) | base: {e.preco_m2_base:,.0f} €/m2 em {e.trimestre_base}".replace(",", " ")
        + f"; {e.n_transacoes or '?'} transações",
    ]
    if a.qualidade:
        linhas.append(f"  Apreciação (fotos/descrição): {a.qualidade.nota:.0f}/100 [{a.qualidade.origem}] - {a.qualidade.resumo}")
        if a.qualidade.positivos:
            linhas.append("    + " + "; ".join(a.qualidade.positivos))
        if a.qualidade.negativos:
            linhas.append("    - " + "; ".join(a.qualidade.negativos))
    linhas += [
        "",
        f"VEREDICTO: {v.categoria.upper()}",
        f"  Preço efetivo (pedido -{config.margem_negociacao:.0%} de negociação): {eur(v.preco_efetivo)} "
        f"= {pct(v.diferenca_pct, True)} face à estimativa",
    ]
    if v.mensagem:
        linhas.append(f"  {v.mensagem}")
    linhas += ["", f"VALORIZAÇÃO PROJETADA (histórico: {pct(p.cagr_historico)}/ano em {p.anos_historico:.0f} anos, volatilidade {pct(p.volatilidade)})"]
    cab = "  Horizonte   " + "".join(f"{c.nome:>26}" for c in p.cenarios)
    linhas.append(cab)
    for h in config.horizontes_anos:
        if p.retorno_valido:
            celulas = [f"{eur(c.valores[h])} ({pct(c.retorno_liquido_anual[h], True)}/ano)" for c in p.cenarios]
        else:
            celulas = [eur(c.valores[h]) for c in p.cenarios]
        linhas.append(f"  {h:>2} anos     " + "".join(f"{c:>26}" for c in celulas))
    if p.retorno_valido:
        linhas.append(f"  (retorno líquido anual, após {config.custos_compra_pct:.0%} de custos de compra; "
                      f"real = descontando {config.inflacao_anual:.0%} de inflação)")
        base = next(c for c in p.cenarios if c.nome == "base")
        h5 = 5 if 5 in config.horizontes_anos else config.horizontes_anos[0]
        linhas.append(f"  Cenário base a {h5} anos: {pct(base.retorno_real_anual[h5], True)}/ano em termos reais")
    else:
        linhas.append("  (valor de mercado projetado da parte estimada; retorno omitido, ver avisos)")

    avisos = e.avisos + p.avisos
    if avisos:
        linhas += ["", "AVISOS"] + [f"  - {x}" for x in avisos]
    return "\n".join(linhas)


def construir_parser():
    p = argparse.ArgumentParser(prog="imovel_radar", description=__doc__)
    p.add_argument("anuncio", help="ficheiro JSON com os dados do anúncio")
    p.add_argument("--dados", default=str(DADOS_POR_OMISSAO), help="CSV com preço mediano por m2 e trimestre")
    p.add_argument("--data", type=date.fromisoformat, default=None, help="data de referência AAAA-MM-DD (por omissão, hoje)")
    p.add_argument("--config", help="JSON com pressupostos que substituem os valores por omissão")
    p.add_argument("--com-ia", action="store_true", help="analisa as fotos e a descrição com um modelo de IA")
    p.add_argument("--json", action="store_true", help="resultado em JSON")
    return p


def main(argv=None):
    args = construir_parser().parse_args(argv)
    try:
        anuncio = Anuncio.de_dict(json.loads(Path(args.anuncio).read_text(encoding="utf-8")))
        config = Config.de_ficheiro(args.config) if args.config else Config()
        referencia = Referencia.carregar(args.dados)
        data = args.data or date.today()
        if args.com_ia:
            qualidade = pontuar_com_ia(anuncio.descricao, anuncio.fotos)
        elif anuncio.descricao:
            qualidade = pontuar_descricao(anuncio.descricao)
        else:
            qualidade = None
        analise = analisar(anuncio, referencia, config, data, qualidade)
    except (OSError, ValueError, ConcelhoDesconhecido, QualidadeIAErro) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(dataclasses.asdict(analise), ensure_ascii=False, indent=2))
    else:
        print(formatar(anuncio, analise, config, data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
