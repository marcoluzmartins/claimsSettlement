# Valores de referência para validar o Power BI

Calculados à parte (Python) **apenas para conferires os teus resultados**. O enunciado exige que os cálculos
do trabalho estejam no Power BI: reproduz tudo lá com as medidas de `02_modelo_e_medidas_dax.dax` e
compara. Se um número não bater, procura o erro (grão, relação, filtro) antes de avançar.

## Verificações de qualidade dos dados (já feitas)
- `encomendas` 10 693 | `entregas` 10 693 (1:1 por `id_encomenda`) | `linha_encomenda` 22 974.
- Sem nulos, sem duplicados, sem chaves órfãs; expedição ≥ encomenda e entrega ≥ expedição em todas as linhas.
- Encomendas de **01/01/2025 a 31/08/2026**; calendário vai até 04/10/2026; objetivos só **jan–ago 2026**.
  => período comparável = **1 jan–31 ago** de cada ano. 2025 completo (6 000 enc.) NÃO é comparável.
- Há 2 130 encomendas feitas ao fim de semana; todas as expedições são em dias úteis.
- Dias úteis de processamento (encomenda → expedição): 1:2 015 | 2:3 321 | 3:2 819 | 4:1 582 | 5:660 | 6:217 | 7:65 | 8:14.

## Q4 – Jan–Ago 2025 vs Jan–Ago 2026
| Indicador | 2025 | 2026 |
|---|---|---|
| Nº encomendas | 3 697 | 4 693 (+26,9 %) |
| Valor encomendas | 1 189 502 € | 1 493 004 € (+25,5 %) |
| Margem de contribuição | 472 078 € | 597 473 € |
| Taxa de margem | 39,69 % | 40,02 % |
| Custo logístico médio / enc. | 9,15 € | 8,71 € (−4,8 %) |
| % processadas ≤ 4 dias úteis | 91,2 % | 90,7 % |
| % entregas até data prometida | 88,4 % | 88,4 % |
| Atraso médio (dias, só atrasadas) | 2,55 | 2,55 |

Leitura: atividade e economia melhoram; qualidade de serviço **estagnada** (processamento ligeiramente pior).

## Q3/Q5 – pontos de atenção (jan–ago 2026)
- **Centro Interior (C08)**: processadas no prazo 83,0 % (90,4 % em 2025); é o único centro cujo custo médio (9,06 €)
  fica **acima** do objetivo (8,74 €).
- Volume acima do objetivo em **todos** os centros (Lisboa +43 %; Interior +5 %).
- Taxa de entrega no prazo abaixo do objetivo em 6 de 8 centros (Norte −3,5 pp; Alentejo −3,2 pp; Interior −2,5 pp);
  só o Litoral supera o objetivo. O ranking dos centros muda conforme o indicador (Lisboa: 1.º em volume, ~no objetivo na taxa).
- Custo médio abaixo do objetivo em 6 de 8 centros.
- Transportadoras: LusoExpress é a mais cara (10,10 €/enc.), ViaNorte a mais barata (7,64 €) e com menos atrasos;
  diferenças entre transportadoras na taxa de entrega são pequenas (87,4 %–89,4 %).
- Economy: 83,2 % entregues no prazo em 2026 (85,2 % em 2025) enquanto Express sobe para 93,7 %.

## Q7 – afirmação da Direção (sugestão: **qualificada**)
- Verdadeiro: mais encomendas (+26,9 %) e custo logístico médio menor (−4,8 %, e desce **dentro de cada** tipo de serviço, logo não é só mix).
- Insuficiente: não mede qualidade (prazo de processamento e de entrega sem melhoria), nem a margem total (que sobe),
  nem a concentração de problemas (Centro Interior; clientes do Interior).

## Q9 – Key Influencers (atraso = data_entrega > data_prometida; 12,3 % das entregas)
- Taxa de atraso 2025: 12,8 % | 2026: 11,6 %.
- **Região do cliente = Interior: 23,5 %** vs ~10,6 % no resto (1 393 enc.; 328 das 1 310 atrasadas).
  Mantém-se dentro de cada serviço, transportadora e centro (nenhum explica o efeito) -> candidato a fator principal.
- Serviço Economy 16,7 % | Standard 11,8 % | Express 7,5 %. Prioridade Normal 12,9 % vs Alta 9,4 %.
- Peso da encomenda > 20 kg: ~16,9 % vs ~11–12 % abaixo.
- **Fugas de informação** (excluir em 9.2): `tentativas_entrega` (2 tentativas: 56,6 % atrasadas; 3: 100 %) – é consequência da
  entrega falhada, só conhecida depois; `data_entrega` / atraso em dias (circular, definem a variável); idealmente `data_expedicao`
  e dias de processamento só se a decisão for tomada após a expedição.
- Causalidade (9.4): "Interior" é um proxy (distância, densidade de rotas, janelas de entrega) que **não está nos dados**; a mesma
  região não é a causa por si. A associação não depende da transportadora nem do centro, mas há fatores não observados.

## Q8 – candidatos a prioridade (escolhe UM e justifica a alternativa)
1. **Entregas a clientes do Interior** (taxa de atraso ~2×; a piorar: 22,0 % → 25,6 % em jan–ago).
2. **Centro Interior** – processamento no prazo 90,4 % → 83,0 % e custo médio acima do objetivo.
3. **Serviço Economy** – 83,2 % no prazo e a descer.
