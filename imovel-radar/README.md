# Imóvel Radar

Dado um anúncio de imóvel, a app calcula:

1. uma **estimativa indicativa** do valor, com intervalo e nível de confiança;
2. um **veredicto** sobre o preço pedido: *Sobrevalorizado*, *Aceitável*, *Bom negócio*, *Pechincha* ou *Inconclusivo*;
3. uma **projeção de valorização** a 3, 5 e 10 anos em três cenários, com o retorno líquido de custos de compra;
4. opcionalmente, uma **nota de apreciação** (0-100) a partir das fotos e da descrição, com IA.

> **Aviso.** É uma estimativa estatística, não uma avaliação oficial (que cabe a um perito avaliador) nem aconselhamento financeiro. Os dados incluídos são **sintéticos**: os números de exemplo não são reais.

## Como correr

Só precisa de Python 3.10+ (sem dependências para o modo base).

```bash
python3 -m imovel_radar examples/anuncio_exemplo.json --data 2026-11-01
python3 -m imovel_radar examples/anuncio_exemplo.json --config examples/config_exemplo.json
python3 -m unittest discover -s tests -t .
```

Opções: `--dados` (CSV de preços), `--data` (data de referência), `--config` (pressupostos em JSON), `--com-ia`, `--json`.

## Anúncio (JSON)

Obrigatórios: `concelho`, `preco_pedido`, `area_util_m2`. Opcionais: `tipologia`, `ano_construcao`, `estado` (`novo`, `renovado`, `bom`, `razoavel`, `para_recuperar`), `area_terreno_m2`, `extras` (lista), `descricao`, `fotos` (caminhos ou URLs), `titulo`.

O anúncio é fornecido por quem usa a app. **Não há *scraping* de portais**: ver "Fonte dos anúncios" abaixo.

## Como funciona

**Estimativa.** Preço mediano por m² do concelho (último trimestre, extrapolado até 4 trimestres com metade da tendência) × área útil × fatores de idade, estado e apreciação. Terreno e piscina só entram se definir `terreno_eur_m2` e `valor_piscina` na configuração; caso contrário ficam **sinalizados como não valorizados**.

**Intervalo e confiança.** Cresce quando há poucas transações na zona e quando há extras por valorizar.

**Veredicto.** Compara o *preço efetivo* (pedido menos a margem de negociação, 5% por omissão, porque os dados medem vendas e os anúncios mostram pedidos) com a estimativa. Se o preço parece alto mas há extras não valorizados, o resultado é *Inconclusivo*, não *Sobrevalorizado*. A diferença só é "significativa" se exceder a margem de incerteza. Uma *Pechincha* vem sempre com um aviso de cautela.

**Projeção.** Parte do crescimento histórico anual da zona e converge para um crescimento de longo prazo (2% por omissão). Os cenários deslocam o crescimento em ±meio desvio-padrão histórico. O retorno desconta custos de compra e inflação. Não inclui rendas, IMI, condomínio, obras nem mais-valias. Se a estimativa ignora extras, o retorno é omitido, porque seria enganador.

## Pressupostos que tem de rever

Estes valores são pontos de partida, **não vêm de fonte oficial**: margem de negociação, custos de compra (7%), fatores de estado e idade, limites do veredicto, crescimento de longo prazo, inflação, e os valores do `examples/config_exemplo.json` (terreno e piscina), que são ilustrativos. Todos se alteram num JSON de configuração (`Config` em `imovel_radar/config.py`).

## Dados

`data/sample/preco_m2_concelho_SINTETICO.csv` é **fictício**, gerado por `scripts/gerar_dados_sinteticos.py`, com concelhos de nome "Exemplo-…". Para usar dados reais, crie um CSV com as colunas

```
concelho,trimestre,preco_m2_mediano,n_transacoes,fonte
```

a partir das estatísticas de preços da habitação do INE (preço mediano de venda por m² e número de transações, por município e trimestre) e passe-o com `--dados`. Confirme no site do INE os nomes exatos dos indicadores e as condições de reutilização. O INE publica agregados, não vendas individuais, e com atraso, por isso a mediana municipal esconde diferenças entre bairros e entre tipos de imóvel.

## Análise com IA (`--com-ia`)

```bash
pip install anthropic
export ANTHROPIC_API_KEY=...        # chave da API
export IMOVEL_RADAR_MODEL=...       # modelo a usar
python3 -m imovel_radar anuncio.json --com-ia
```

Envia as fotos (até 6) e a descrição para o modelo, que devolve nota, resumo e pontos positivos e negativos. As fotos saem da sua máquina para a API: não use imagens com dados pessoais. Sem `--com-ia`, a nota vem de uma heurística por palavras-chave da descrição.

## Fonte dos anúncios

O MVP não faz *scraping*: os termos de uso de muitos portais proíbem a extração automática, há direitos sobre bases de dados e fotos, e podem existir dados pessoais nos anúncios (RGPD). O caminho mais seguro para um produto é uma API oficial ou uma parceria. A fonte está isolada (`Anuncio.de_dict`), por isso pode ser substituída sem mexer no modelo.

## Próximos passos

- Script de descarga dos dados reais do INE (precisa de acesso de rede ao domínio do INE).
- Calibrar a margem de negociação e os fatores com dados reais.
- Segunda âncora de preço: avaliação bancária do INE.
- Interface web simples (formulário + resultado) e mapa de preços por concelho.
