"""Nota de apreciação do imóvel a partir da descrição e das fotos.

Sem IA: heurística simples por palavras-chave (só descrição).
Com IA: um modelo da Anthropic vê as fotos e lê a descrição. Requer o pacote
`anthropic`, ANTHROPIC_API_KEY e a variável IMOVEL_RADAR_MODEL com o modelo a usar.
"""
import base64
import json
import mimetypes
import os
import re
from pathlib import Path

from .models import Qualidade
from .reference import normalizar_nome

POSITIVOS = (
    "remodelad", "renovad", "recuperad", "luminos", "vista", "novo", "nova",
    "isolamento", "painéis solares", "paineis solares", "aquecimento central", "cozinha equipada",
)
NEGATIVOS = (
    "para recuperar", "a necessitar de obras", "necessita de obras", "obras", "devolut",
    "ruina", "degradad", "humidade", "infiltra", "abandonad", "estado de conservacao medio",
)
_NEGACOES = ("sem obras", "nao necessita de obras", "sem necessidade de obras", "sem humidade")

FORMATOS_IMAGEM = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
                   ".webp": "image/webp", ".gif": "image/gif"}
MAX_FOTOS = 6


class QualidadeIAErro(Exception):
    pass


def _contem(texto, expressao):
    """Procura a expressão (ou radical) no início de uma palavra: 'novo' não casa com 'renovar'."""
    return re.search(r"\b" + re.escape(normalizar_nome(expressao)), texto) is not None


def pontuar_descricao(texto):
    """Heurística: 50 neutro, +6 por sinal positivo, -8 por sinal negativo."""
    t = normalizar_nome(texto)
    positivos_ao = [p for p in POSITIVOS if _contem(t, p)]
    sem_negacoes = t
    for n in _NEGACOES:
        if n in sem_negacoes:
            positivos_ao.append(n)
            sem_negacoes = sem_negacoes.replace(n, " ")
    negativos_ao = [n for n in NEGATIVOS if _contem(sem_negacoes, n)]
    nota = min(max(50 + 6 * len(positivos_ao) - 8 * len(negativos_ao), 0), 100)
    resumo = "Estimada só pela descrição (palavras-chave); não considera as fotos."
    return Qualidade(nota=nota, resumo=resumo, positivos=positivos_ao, negativos=negativos_ao)


def extrair_json(texto):
    inicio, fim = texto.find("{"), texto.rfind("}")
    if inicio < 0 or fim <= inicio:
        raise QualidadeIAErro("A resposta do modelo não contém JSON.")
    try:
        return json.loads(texto[inicio : fim + 1])
    except json.JSONDecodeError as e:
        raise QualidadeIAErro(f"JSON inválido na resposta do modelo: {e}") from e


def _bloco_imagem(caminho):
    if re.match(r"^https?://", caminho):
        return {"type": "image", "source": {"type": "url", "url": caminho}}
    ficheiro = Path(caminho)
    media = FORMATOS_IMAGEM.get(ficheiro.suffix.lower()) or mimetypes.guess_type(caminho)[0]
    if media not in FORMATOS_IMAGEM.values():
        raise QualidadeIAErro(f"Formato de imagem não suportado: {caminho}")
    dados = base64.standard_b64encode(ficheiro.read_bytes()).decode("ascii")
    return {"type": "image", "source": {"type": "base64", "media_type": media, "data": dados}}


PROMPT = """Avalia o estado e o apelo deste imóvel para compra, usando só as fotos e a descrição.
Responde apenas com um objeto JSON, sem texto à volta:
{"nota": <número de 0 a 100, 50 = imóvel médio para a zona>,
 "resumo": "<2 frases>",
 "positivos": ["..."], "negativos": ["..."]}
Sê conservador: não inventes o que não se vê. Se as fotos forem poucas ou más, diz isso no resumo
e aproxima a nota de 50.

Descrição do anúncio:
"""


def pontuar_com_ia(descricao, fotos, cliente=None, modelo=None):
    modelo = modelo or os.environ.get("IMOVEL_RADAR_MODEL")
    if not modelo:
        raise QualidadeIAErro("Defina IMOVEL_RADAR_MODEL com o modelo a usar.")
    if cliente is None:
        try:
            import anthropic
        except ImportError as e:
            raise QualidadeIAErro("Instale o pacote 'anthropic' (pip install anthropic).") from e
        cliente = anthropic.Anthropic()

    conteudo = [_bloco_imagem(f) for f in list(fotos)[:MAX_FOTOS]]
    conteudo.append({"type": "text", "text": PROMPT + (descricao or "(sem descrição)")})
    resposta = cliente.messages.create(
        model=modelo,
        max_tokens=2000,
        messages=[{"role": "user", "content": conteudo}],
    )
    if resposta.stop_reason == "refusal":
        raise QualidadeIAErro("O modelo recusou analisar este conteúdo.")
    texto = next((b.text for b in resposta.content if b.type == "text"), "")
    dados = extrair_json(texto)
    try:
        nota = float(dados["nota"])
    except (KeyError, TypeError, ValueError) as e:
        raise QualidadeIAErro("Resposta sem 'nota' numérica.") from e
    return Qualidade(
        nota=min(max(nota, 0.0), 100.0),
        resumo=str(dados.get("resumo", "")),
        positivos=[str(x) for x in dados.get("positivos", [])],
        negativos=[str(x) for x in dados.get("negativos", [])],
        origem="ia",
    )
