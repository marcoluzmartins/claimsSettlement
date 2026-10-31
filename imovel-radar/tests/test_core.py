import contextlib
import io
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from imovel_radar.analise import analisar
from imovel_radar.cli import DADOS_POR_OMISSAO, main
from imovel_radar.config import Config
from imovel_radar.forecast import projetar
from imovel_radar.models import Anuncio, Qualidade
from imovel_radar.quality import QualidadeIAErro, extrair_json, pontuar_com_ia, pontuar_descricao
from imovel_radar.reference import (
    ConcelhoDesconhecido, DadosInsuficientes, Ponto, Referencia,
    cagr_anual, normalizar_nome, parse_trimestre, volatilidade_anual,
)
from imovel_radar.valuation import estimar
from imovel_radar.verdict import (
    ACEITAVEL, BOM_NEGOCIO, INCONCLUSIVO, PECHINCHA, SOBREVALORIZADO, avaliar_preco,
)

HOJE = date(2026, 11, 1)


def serie_crescente(taxa_anual=0.05, anos=12, preco=1000.0, n=200, fim=(2026, 2)):
    pontos, ano, tri = [], 2026 - anos, 1
    while (ano, tri) <= fim:
        pontos.append(Ponto(ano, tri, preco, n))
        preco *= (1 + taxa_anual) ** 0.25
        tri += 1
        if tri == 5:
            ano, tri = ano + 1, 1
    return pontos


def referencia(**kw):
    return Referencia({"Zona": serie_crescente(**kw)})


def anuncio(**kw):
    base = dict(concelho="Zona", preco_pedido=200000, area_util_m2=100, estado="bom")
    base.update(kw)
    return Anuncio.de_dict(base)


class ReferenciaTest(unittest.TestCase):
    def test_parse_trimestre(self):
        self.assertEqual(parse_trimestre("2024Q3"), (2024, 3))
        self.assertEqual(parse_trimestre("2024-T1"), (2024, 1))
        with self.assertRaises(ValueError):
            parse_trimestre("2024Q5")

    def test_nome_sem_acentos_nem_maiusculas(self):
        self.assertEqual(normalizar_nome("  Vila  Real "), normalizar_nome("vila real"))
        self.assertEqual(normalizar_nome("Mouçós"), "moucos")

    def test_concelho_desconhecido(self):
        with self.assertRaises(ConcelhoDesconhecido):
            referencia().serie("Outra")

    def test_cagr_recupera_a_taxa(self):
        taxa, anos = cagr_anual(serie_crescente(0.05))
        self.assertAlmostEqual(taxa, 0.05, places=3)
        self.assertGreater(anos, 9)

    def test_serie_curta(self):
        with self.assertRaises(DadosInsuficientes):
            cagr_anual(serie_crescente(anos=1, fim=(2026, 1)))

    def test_volatilidade_zero_em_crescimento_constante(self):
        self.assertAlmostEqual(volatilidade_anual(serie_crescente(0.05)), 0.0, places=6)

    def test_carregar_csv_de_exemplo(self):
        ref = Referencia.carregar(DADOS_POR_OMISSAO)
        self.assertTrue(ref.sintetica)
        self.assertEqual(len(ref.concelhos()), 8)


class EstimativaTest(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.ref = referencia()

    def test_mais_area_vale_mais(self):
        a = estimar(anuncio(area_util_m2=100), self.ref, self.config, HOJE)
        b = estimar(anuncio(area_util_m2=150), self.ref, self.config, HOJE)
        self.assertAlmostEqual(b.central / a.central, 1.5, places=6)

    def test_estado_altera_valor(self):
        bom = estimar(anuncio(estado="bom"), self.ref, self.config, HOJE)
        obras = estimar(anuncio(estado="para_recuperar"), self.ref, self.config, HOJE)
        self.assertLess(obras.central, bom.central)

    def test_estado_invalido(self):
        with self.assertRaises(ValueError):
            estimar(anuncio(estado="otimo"), self.ref, self.config, HOJE)

    def test_poucas_transacoes_baixam_a_confianca(self):
        muitas = estimar(anuncio(), referencia(n=500), self.config, HOJE)
        poucas = estimar(anuncio(), referencia(n=4), self.config, HOJE)
        self.assertGreater(poucas.meia_amplitude, muitas.meia_amplitude)
        self.assertEqual(muitas.confianca, "alta")
        self.assertEqual(poucas.confianca, "baixa")

    def test_extras_sem_valor_ficam_sinalizados(self):
        sem_fatores = Config(terreno_fator_m2=None, piscina_fator_casa=None)
        e = estimar(anuncio(area_terreno_m2=1000, extras=["Piscina", "poço"]), self.ref, sem_fatores, HOJE)
        self.assertEqual(len(e.extras_nao_valorizados), 2)
        self.assertTrue(any("poço" in a for a in e.avisos))

    def test_extras_com_valor_somam(self):
        config = Config(terreno_eur_m2=40, valor_piscina=25000)
        sem = estimar(anuncio(), self.ref, config, HOJE)
        com = estimar(anuncio(area_terreno_m2=1000, extras=["piscina"]), self.ref, config, HOJE)
        self.assertAlmostEqual(com.central - sem.central, 40 * 1000 + 25000, places=4)
        self.assertEqual(com.extras_nao_valorizados, [])

    def test_extrapola_data_posterior_ao_ultimo_dado(self):
        no_dia = estimar(anuncio(), self.ref, self.config, date(2026, 5, 1))
        depois = estimar(anuncio(), self.ref, self.config, HOJE)
        self.assertGreater(depois.preco_m2_base, no_dia.preco_m2_base)
        self.assertTrue(any("extrapolado" in a for a in depois.avisos))

    def test_qualidade_ajusta_dentro_do_limite(self):
        neutra = estimar(anuncio(), self.ref, self.config, HOJE, Qualidade(50, ""))
        otima = estimar(anuncio(), self.ref, self.config, HOJE, Qualidade(100, ""))
        self.assertAlmostEqual(otima.central / neutra.central, 1 + self.config.ajuste_qualidade_max, places=6)


class VeredictoTest(unittest.TestCase):
    def setUp(self):
        self.config = Config(margem_negociacao=0.0, terreno_fator_m2=None, piscina_fator_casa=None)
        self.ref = referencia()
        self.central = estimar(anuncio(), self.ref, self.config, HOJE).central

    def categoria(self, razao, **kw):
        a = anuncio(preco_pedido=self.central * razao, **kw)
        est = estimar(a, self.ref, self.config, HOJE)
        return avaliar_preco(a, est, self.config)

    def test_limites(self):
        self.assertEqual(self.categoria(1.25).categoria, SOBREVALORIZADO)
        self.assertEqual(self.categoria(1.00).categoria, ACEITAVEL)
        self.assertEqual(self.categoria(0.80).categoria, BOM_NEGOCIO)
        self.assertEqual(self.categoria(0.60).categoria, PECHINCHA)

    def test_pechincha_pede_cautela(self):
        self.assertIn("anúncio falso", self.categoria(0.60).mensagem)

    def test_alto_com_extras_sem_valor_e_inconclusivo(self):
        v = self.categoria(1.50, area_terreno_m2=1000)
        self.assertEqual(v.categoria, INCONCLUSIVO)

    def test_baixo_com_extras_sem_valor_continua_valido(self):
        # Se já está barato ignorando os extras, ainda é mais barato com eles.
        v = self.categoria(0.60, extras=["piscina"])
        self.assertEqual(v.categoria, PECHINCHA)

    def test_margem_de_negociacao_reduz_o_preco_efetivo(self):
        config = Config(margem_negociacao=0.10)
        a = anuncio(preco_pedido=200000)
        v = avaliar_preco(a, estimar(a, self.ref, config, HOJE), config)
        self.assertAlmostEqual(v.preco_efetivo, 180000)


class ProjecaoTest(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.ref = referencia(taxa_anual=0.06)
        self.serie = self.ref.serie("Zona")

    def projecao(self, **kw):
        a = anuncio(**kw)
        est = estimar(a, self.ref, self.config, HOJE)
        return est, projetar(est, a.preco_pedido, self.serie, self.config)

    def test_ordem_dos_cenarios(self):
        # Volatilidade nula na série perfeita: usa serie ruidosa para ter desvio.
        serie = serie_crescente(0.06)
        for i in range(0, len(serie), 3):
            serie[i] = Ponto(serie[i].ano, serie[i].trimestre, serie[i].preco_m2 * 1.05, 200)
        ref = Referencia({"Zona": serie})
        a = anuncio()
        est = estimar(a, ref, self.config, HOJE)
        p = projetar(est, a.preco_pedido, ref.serie("Zona"), self.config)
        pess, base, otim = p.cenarios
        self.assertEqual([c.nome for c in p.cenarios], ["pessimista", "base", "otimista"])
        for h in self.config.horizontes_anos:
            self.assertLess(pess.valores[h], base.valores[h])
            self.assertLess(base.valores[h], otim.valores[h])

    def test_crescimento_converge_para_o_longo_prazo(self):
        est, p = self.projecao()
        base = p.cenarios[1]
        self.assertLess(base.crescimento_anual_medio, p.cagr_historico)
        self.assertGreater(base.crescimento_anual_medio, self.config.crescimento_longo_prazo)

    def test_custos_de_compra_reduzem_o_retorno(self):
        a = anuncio()
        est = estimar(a, self.ref, self.config, HOJE)
        sem = projetar(est, a.preco_pedido, self.serie, Config(custos_compra_pct=0.0))
        com = projetar(est, a.preco_pedido, self.serie, Config(custos_compra_pct=0.07))
        self.assertGreater(sem.cenarios[1].retorno_liquido_anual[5], com.cenarios[1].retorno_liquido_anual[5])

    def test_comprar_abaixo_do_valor_melhora_o_retorno(self):
        est, _ = self.projecao()
        barato = projetar(est, est.central * 0.8, self.serie, self.config)
        justo = projetar(est, est.central, self.serie, self.config)
        self.assertGreater(barato.cenarios[1].retorno_liquido_anual[5], justo.cenarios[1].retorno_liquido_anual[5])

    def test_retorno_omitido_com_extras_sem_valor(self):
        sem_fatores = Config(terreno_fator_m2=None, piscina_fator_casa=None)
        a = anuncio(area_terreno_m2=500)
        p = projetar(estimar(a, self.ref, sem_fatores, HOJE), a.preco_pedido, self.serie, sem_fatores)
        self.assertFalse(p.retorno_valido)
        self.assertTrue(any("Retorno omitido" in a for a in p.avisos))

    def test_analise_completa(self):
        a = analisar(anuncio(), self.ref, self.config, HOJE)
        self.assertFalse(a.dados_sinteticos)
        self.assertTrue(a.projecao.retorno_valido)


class QualidadeTest(unittest.TestCase):
    def test_descricao_positiva_e_negativa(self):
        boa = pontuar_descricao("Moradia remodelada e luminosa com vista de rio")
        ma = pontuar_descricao("Casa devoluta, para recuperar, com humidade")
        self.assertGreater(boa.nota, 50)
        self.assertLess(ma.nota, 50)

    def test_negacao_nao_conta_como_defeito(self):
        q = pontuar_descricao("Imóvel sem obras a fazer, sem humidade")
        self.assertGreaterEqual(q.nota, 50)
        self.assertEqual(q.negativos, [])

    def test_nota_dentro_dos_limites(self):
        self.assertEqual(pontuar_descricao("ruína devoluta degradada abandonada humidade infiltrações obras").nota, 0)

    def test_palavra_so_conta_no_inicio(self):
        self.assertEqual(pontuar_descricao("Ideal para renovar a seu gosto").positivos, [])

    def test_extrair_json_com_texto_a_volta(self):
        self.assertEqual(extrair_json('Aqui: {"nota": 70} fim')["nota"], 70)
        with self.assertRaises(QualidadeIAErro):
            extrair_json("sem json")

    def test_ia_sem_modelo_configurado(self):
        import os
        antigo = os.environ.pop("IMOVEL_RADAR_MODEL", None)
        try:
            with self.assertRaises(QualidadeIAErro):
                pontuar_com_ia("x", [], cliente=object())
        finally:
            if antigo is not None:
                os.environ["IMOVEL_RADAR_MODEL"] = antigo

    def test_ia_com_cliente_simulado(self):
        class Bloco:
            type = "text"
            text = 'Resultado: {"nota": 130, "resumo": "ok", "positivos": ["luz"], "negativos": []}'

        class Resposta:
            stop_reason = "end_turn"
            content = [Bloco()]

        class Mensagens:
            def create(self, **kw):
                self.kw = kw
                return Resposta()

        class Cliente:
            messages = Mensagens()

        q = pontuar_com_ia("casa", [], cliente=Cliente(), modelo="modelo-de-teste")
        self.assertEqual(q.nota, 100.0)  # limitada a 100
        self.assertEqual(q.origem, "ia")
        self.assertEqual(Cliente.messages.kw["model"], "modelo-de-teste")

    def test_ia_recusa(self):
        class Resposta:
            stop_reason = "refusal"
            content = []

        class Cliente:
            class messages:
                @staticmethod
                def create(**kw):
                    return Resposta()

        with self.assertRaises(QualidadeIAErro):
            pontuar_com_ia("casa", [], cliente=Cliente(), modelo="m")


class AnuncioTest(unittest.TestCase):
    def test_campos_obrigatorios(self):
        with self.assertRaises(ValueError):
            Anuncio.de_dict({"concelho": "Zona"})

    def test_campo_desconhecido(self):
        with self.assertRaises(ValueError):
            Anuncio.de_dict({"concelho": "Z", "preco_pedido": 1, "area_util_m2": 1, "cor": "azul"})

    def test_valores_nao_positivos(self):
        with self.assertRaises(ValueError):
            Anuncio.de_dict({"concelho": "Z", "preco_pedido": -1, "area_util_m2": 10})

    def test_config_com_parametro_desconhecido(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "c.json"
            f.write_text('{"nao_existe": 1}', encoding="utf-8")
            with self.assertRaises(ValueError):
                Config.de_ficheiro(f)


class CliTest(unittest.TestCase):
    def test_exemplo_de_ponta_a_ponta(self):
        exemplo = Path(__file__).resolve().parent.parent / "examples" / "anuncio_exemplo.json"
        with contextlib.redirect_stdout(io.StringIO()) as saida:
            self.assertEqual(main([str(exemplo), "--data", "2026-11-01", "--json"]), 0)
        resultado = json.loads(saida.getvalue())
        self.assertIn(resultado["veredicto"]["categoria"], {SOBREVALORIZADO, ACEITAVEL, BOM_NEGOCIO, PECHINCHA, INCONCLUSIVO})
        self.assertIn("padrao", resultado)

    def test_erro_devolve_codigo_1(self):
        self.assertEqual(main(["nao_existe.json"]), 1)


class FatoresTest(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.ref = referencia()

    def estimar(self, **kw):
        return estimar(anuncio(**kw), self.ref, self.config, HOJE)

    def test_exposicao_sul_vale_mais_que_norte(self):
        sul = self.estimar(exposicao_solar="sul")
        norte = self.estimar(exposicao_solar="N")
        self.assertGreater(sul.central, norte.central)

    def test_exposicao_invalida(self):
        with self.assertRaises(ValueError):
            anuncio(exposicao_solar="cima")

    def test_acesso_dificil_desvaloriza(self):
        self.assertLess(self.estimar(acesso="dificil").central, self.estimar(acesso="bom").central)
        self.assertEqual(anuncio(acesso="Razoável").acesso, "razoavel")

    def test_anexos_com_area_somam_e_sem_area_ficam_sinalizados(self):
        sem = self.estimar()
        com = self.estimar(anexos=["garagem"], area_anexos_m2=20)
        self.assertGreater(com.central, sem.central)
        sem_area = self.estimar(anexos=["garagem"])
        self.assertEqual(sem_area.central, sem.central)
        self.assertTrue(any("anexos" in x for x in sem_area.extras_nao_valorizados))

    def test_piscina_valorizada_por_fator_por_omissao(self):
        com = self.estimar(extras=["piscina"])
        sem = self.estimar()
        self.assertAlmostEqual(com.central / sem.central, 1 + self.config.piscina_fator_casa, places=6)
        self.assertGreater(com.meia_amplitude, sem.meia_amplitude)

    def test_contribuicoes_somam_ate_ao_valor_central(self):
        e = self.estimar(estado="renovado", exposicao_solar="S", acesso="razoavel",
                         extras=["piscina"], area_terreno_m2=300, anexos=["garagem"], area_anexos_m2=15,
                         ano_construcao=1980)
        soma = e.componentes["base_mediana"] + sum(c["valor"] for c in e.componentes["contribuicoes"])
        self.assertAlmostEqual(soma, e.central, places=4)

    def test_quartos_incoerentes_geram_aviso(self):
        e = self.estimar(area_util_m2=40, quartos=6)
        self.assertTrue(any("quartos" in a for a in e.avisos))
        self.assertFalse(any("quartos" in a for a in self.estimar(area_util_m2=120, quartos=3).avisos))


class ZonasEPadraoTest(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.ref = Referencia({
            "A": serie_crescente(0.05, preco=1000, n=300),
            "B": serie_crescente(0.05, preco=1050, n=280),
            "C": serie_crescente(0.05, preco=1100, n=310),
            "Longe": serie_crescente(0.01, preco=300, n=10),
        })

    def test_zonas_semelhantes_exclui_a_propria_e_ordena_por_proximidade(self):
        nomes = [n for n, _ in self.ref.zonas_semelhantes("A", k=3)]
        self.assertNotIn("A", nomes)
        self.assertEqual(nomes[-1], "Longe")
        self.assertEqual(nomes[0], "B")

    def test_padrao_dentro_e_fora(self):
        a_justo = anuncio(concelho="A", preco_pedido=100 * 1500)
        est = estimar(a_justo, self.ref, self.config, HOJE)
        dentro = analisar(anuncio(concelho="A", preco_pedido=est.preco_m2_base * 100), self.ref, self.config, HOJE)
        acima = analisar(anuncio(concelho="A", preco_pedido=est.preco_m2_base * 100 * 1.6), self.ref, self.config, HOJE)
        self.assertTrue(dentro.padrao.dentro_do_padrao)
        self.assertFalse(acima.padrao.dentro_do_padrao)
        self.assertIn("acima", acima.padrao.leitura)

    def test_historico_comparativo(self):
        a = analisar(anuncio(concelho="A"), self.ref, self.config, HOJE)
        h = a.historico
        self.assertEqual(len(h["trimestres"]), self.config.trimestres_historico)
        self.assertEqual(set(h["preco_m2"]), {"A", *[s["concelho"] for s in a.padrao.semelhantes]})
        for serie in h["indice_base_100"].values():
            self.assertAlmostEqual(serie[0], 100.0)

    def test_horizontes_por_omissao_incluem_20_anos(self):
        self.assertEqual(self.config.horizontes_anos, (5, 10, 20))
        a = analisar(anuncio(concelho="A"), self.ref, self.config, HOJE)
        self.assertEqual(sorted(a.projecao.cenarios[1].valores), [5, 10, 20])
        self.assertEqual(len(a.projecao.cenarios[1].trajetoria), 21)
        self.assertTrue(any("20 anos" in x for x in a.projecao.avisos))

    def test_dict_para_a_app(self):
        from imovel_radar.analise import analise_para_dict
        a = anuncio(concelho="A")
        d = analise_para_dict(analisar(a, self.ref, self.config, HOJE), a, HOJE)
        json.dumps(d)  # tem de ser serializável
        self.assertEqual(d["projecao"]["grafico"]["anos"][-1], 20)
        self.assertEqual(len(d["projecao"]["grafico"]["base"]), 21)


class ServidorTest(unittest.TestCase):
    def test_api_analisar(self):
        import threading
        import urllib.error
        import urllib.request
        from imovel_radar.server import criar_servidor

        servidor = criar_servidor("127.0.0.1", 0, Referencia.carregar(DADOS_POR_OMISSAO), Config())
        threading.Thread(target=servidor.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{servidor.server_address[1]}"
        try:
            corpo = json.dumps({"concelho": "Exemplo-Interior", "preco_pedido": 200000, "area_util_m2": 120,
                                "quartos": 3, "exposicao_solar": "S"}).encode()
            req = urllib.request.Request(base + "/api/analisar", corpo, {"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as r:
                resposta = json.load(r)
            self.assertIn("veredicto", resposta)
            self.assertTrue(resposta["meta"]["sintetico"])
            with urllib.request.urlopen(base + "/api/concelhos") as r:
                self.assertIn("Exemplo-Interior", json.load(r)["concelhos"])
            erro = urllib.request.Request(base + "/api/analisar", b'{"concelho": "Nenhum"}', {"Content-Type": "application/json"})
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                urllib.request.urlopen(erro)
            self.assertEqual(ctx.exception.code, 400)
        finally:
            servidor.shutdown()
            servidor.server_close()


if __name__ == "__main__":
    unittest.main()
