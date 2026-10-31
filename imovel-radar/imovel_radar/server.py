"""Servidor local: serve a app mobile e a API de análise.

    python -m imovel_radar.server --porta 8000

Escuta só em 127.0.0.1 por omissão. Para abrir no telemóvel na mesma rede,
use --host 0.0.0.0 (a app não tem autenticação: não a exponha à internet).
"""
import argparse
import json
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .analise import analisar, analise_para_dict
from .cli import DADOS_POR_OMISSAO
from .config import Config
from .models import Anuncio
from .quality import pontuar_descricao
from .reference import ConcelhoDesconhecido, Referencia

APP = Path(__file__).resolve().parent.parent / "app" / "index.html"
MAX_CORPO = 100_000


def criar_servidor(host, porta, referencia, config):
    class Handler(BaseHTTPRequestHandler):
        def _responder(self, codigo, corpo, tipo="application/json; charset=utf-8"):
            dados = corpo if isinstance(corpo, bytes) else json.dumps(corpo, ensure_ascii=False).encode("utf-8")
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(dados)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(dados)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                self._responder(200, APP.read_bytes(), "text/html; charset=utf-8")
            elif self.path == "/api/concelhos":
                self._responder(200, {"concelhos": referencia.concelhos(), "sintetico": referencia.sintetica})
            else:
                self._responder(404, {"erro": "não encontrado"})

        def do_POST(self):
            if self.path != "/api/analisar":
                return self._responder(404, {"erro": "não encontrado"})
            try:
                tamanho = int(self.headers.get("Content-Length", 0))
                if not 0 < tamanho <= MAX_CORPO:
                    return self._responder(413, {"erro": "corpo do pedido inválido ou demasiado grande"})
                dados = json.loads(self.rfile.read(tamanho))
                anuncio = Anuncio.de_dict(dados)
                qualidade = pontuar_descricao(anuncio.descricao) if anuncio.descricao else None
                data = date.today()
                analise = analisar(anuncio, referencia, config, data, qualidade)
                self._responder(200, analise_para_dict(analise, anuncio, data))
            except (ValueError, ConcelhoDesconhecido, TypeError) as erro:
                self._responder(400, {"erro": str(erro)})

        def log_message(self, formato, *args):
            pass

    return ThreadingHTTPServer((host, porta), Handler)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--porta", type=int, default=8000)
    p.add_argument("--dados", default=str(DADOS_POR_OMISSAO))
    p.add_argument("--config")
    args = p.parse_args(argv)
    config = Config.de_ficheiro(args.config) if args.config else Config()
    servidor = criar_servidor(args.host, args.porta, Referencia.carregar(args.dados), config)
    print(f"Imóvel Radar em http://{args.host}:{args.porta}  (Ctrl+C para parar)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
