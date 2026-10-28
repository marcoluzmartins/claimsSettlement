---
title: "Análise de Dados — Guia de estudo para o exame de 2 de novembro"
subtitle: "Teste-modelo resolvido e explicado, com exemplos e variações possíveis"
lang: pt-PT
---

# 0. Como usar este guia

**Formato do exame (email da professora):** 60 minutos, cotado para 20 valores, uma folha A4 manuscrita (frente e verso). Pode ter escolha múltipla, resposta aberta, cálculos, interpretação de resultados e justificação. Depois do exame há uma discussão oral individual do trabalho (5 a 10 minutos).

**Legenda de fontes**

- **[slides]** = está nos PDFs da professora.
- **[complemento]** = conhecimento geral útil, mas **não** está nos slides. Usa com cuidado e, de preferência, com o vocabulário dos slides.

**Estrutura de cada secção:** o que o teste-modelo pergunta → resposta → porquê → exemplo → variações possíveis (com resposta curta).

**Ideia que atravessa a UC inteira [slides]:** *não começamos pelo método, começamos pela pergunta.* Antes de escolher uma técnica, pergunta-te: que tipo de variáveis tenho? Qual é a pergunta de investigação? Tenho grupos previamente definidos?

## 0.1 Mapa de decisão: pergunta → método [slides: Overview]

| Pergunta | Método |
|---|---|
| Como resumir muitas variáveis quantitativas? | **PCA / ACP** |
| Que associações existem entre categorias? | **Análise de Correspondências** (ACS com 2 variáveis, ACM com várias) |
| Que grupos semelhantes existem (grupos desconhecidos)? | **Análise Classificatória** (clustering, não supervisionada) |
| A que grupo pertence uma nova observação (grupos conhecidos)? | **Análise Discriminante** (supervisionada) |

## 0.2 Mapa de decisão: tipos de variáveis → medida de associação [slides 18/09]

| Variável X | Variável Y | Medida |
|---|---|---|
| Quantitativa | Quantitativa | **Pearson** (associação linear) |
| Ordinal | Ordinal | **Spearman** (associação monótona, usa ordens/ranks) |
| Quantitativa | Binária | **Correlação ponto-bisserial** (Pearson com a binária codificada 0/1) |
| Categórica | Categórica | **Qui-quadrado** de independência **+ V de Cramér** |

Regras de bolso: quantitativas → Pearson; rankings → Spearman; outliers extremos → Spearman pode ser mais robusto.

# 1. Grupo I — Escolha múltipla

## Questão 1 — Outlier

**Resposta: (b)** Uma observação que se distingue significativamente das restantes.

**Porquê as outras estão erradas**

- \(a) valores iguais à média: não é um valor extremo, é um valor central.
- \(c) variável categórica com poucas categorias: não tem nada a ver com outliers.
- \(d) "deve ser sempre eliminada": **falso**. Os slides dizem que um valor extremo **não deve ser automaticamente eliminado**; primeiro procura-se perceber a origem (erro de introdução, erro de medição, ou situação rara mas real) e avalia-se o impacto na análise.

**Exemplo [slides]:** rendimentos 1200, 1300, 1400, 1500 e 10000. A média é 3080 e a mediana é 1400. A média é sensível a valores extremos; a mediana é mais robusta.

**Variações possíveis**

- *"Qual é a medida de tendência central mais adequada se houver outliers?"* → a mediana.
- *"Idade = 25, 31, 42, −3, 250. O que fazer?"* → −3 e 250 são impossíveis/incoerentes; verificar se são erros de registo antes de decidir (corrigir, tratar como omisso, ou excluir justificadamente).
- *"Num boxplot, como se identificam possíveis valores extremos?"* → pontos isolados fora dos "bigodes". Convenção habitual: fora de [Q1 − 1,5·AIQ ; Q3 + 1,5·AIQ] **[complemento]**.
- *"Distribuição com cauda à direita, qual a relação média/mediana/moda?"* → média > mediana > moda [slides]. Cauda à esquerda: média < mediana < moda.
- *"Padronizar elimina o efeito dos outliers no clustering?"* → **não**; resolve a escala, não os extremos [slides].

## Questão 2 — Coeficiente de correlação de Pearson

**Resposta: (a)** A associação **linear** entre duas variáveis **quantitativas**.

**Porquê**

- \(b) causalidade: correlação não implica causalidade.
- \(c) qualquer tipo de variável: não; para ordinais usa-se Spearman, para quantitativa × binária a ponto-bisserial, para categóricas o qui-quadrado.
- \(d) diferença entre médias: isso é outro tipo de comparação, não é correlação.

**Propriedades [slides]:** −1 ≤ r ≤ 1; o sinal dá a direção; o módulo dá a força; não captura relações não lineares.

**Exemplo [slides]:** r = 0,90 → associação positiva forte; r = −0,90 → associação negativa forte.

**Armadilha clássica [slides]:** *r ≈ 0 não significa ausência de associação.* Pode haver uma relação **não linear** (por exemplo em forma de U) com r ≈ 0.

**Variações possíveis**

- *Pearson ou Spearman?* Idade e salário → Pearson. Ranking de desempenho e ranking de satisfação → Spearman. Horas de estudo e nota com outliers extremos → Spearman.
- *Satisfação (0-10) e abandono (Sim/Não)?* → ponto-bisserial.
- *Género e abandono?* → qui-quadrado + V de Cramér.
- *"Os slides dizem que o Pearson assume normalidade."* → sim, é uma das condições referidas; se não se verificar ou houver outliers extremos, Spearman é mais robusto.

## Questão 3 — Objetivo principal da PCA

**Resposta: (b)** Reduzir a dimensionalidade, preservando tanta variância quanto possível.

**Porquê**

- \(a) classificar em grupos previamente definidos: isso é Análise Discriminante.
- \(c) causalidade: a PCA não estabelece causalidade [slides].
- \(d) prever variáveis categóricas: a PCA não prevê nada; trabalha com variáveis quantitativas.

**Ideia [slides]:** transformar X₁,…,Xₚ em componentes C₁,…,Cₚ que são combinações lineares das variáveis originais, ordenadas pela variância que explicam (a 1.ª explica o máximo possível, a 2.ª o máximo da variância restante, e assim por diante).

**Variações possíveis**

- *"A PCA é supervisionada?"* → não; não usa grupos. Maximiza **variância explicada**, enquanto a Discriminante maximiza **separação entre grupos** [slides].
- *"Quantas componentes existem no máximo?"* → p (tantas quanto variáveis). Com variáveis padronizadas, os valores próprios somam p (no exemplo dos municípios, 3,62 + 1,74 + … + 0,18 = 8).
- *"Que tipo de variáveis entram na PCA?"* → quantitativas.

## Questão 4 — Clustering hierárquico aglomerativo

**Resposta: (c)** Cada observação começa num cluster e os clusters são sucessivamente agregados.

**Porquê**

- \(a) é o contrário: começa-se com n clusters, não com um.
- \(b) falso: no hierárquico o número de clusters **pode ser escolhido depois**, cortando o dendrograma. É no K-means que k é definido antes.
- \(d) é Análise Discriminante (grupos conhecidos).

**Como funciona [slides]:** 1) cada observação é um grupo; 2) agregam-se sucessivamente os grupos mais próximos; 3) continua até existir um único grupo. O resultado representa-se num **dendrograma**, onde a altura é a distância entre grupos e um corte horizontal define o número de clusters.

**Método de Ward [slides]:** em cada passo junta os grupos cuja fusão provoca o **menor aumento da variabilidade interna**.

**Variações possíveis**

- *Hierárquico vs K-means [slides]:*

| | Hierárquico | K-means |
|---|---|---|
| Estrutura | Hierarquia | Partição |
| k | Pode ser escolhido depois | Normalmente definido antes |
| Resultado | Dendrograma | k grupos |
| Cálculo | Progressivo | Iterativo |

- *"Onde cortar o dendrograma?"* → não só porque "parece"; considerar distâncias, critérios de validação (silhouette), interpretabilidade e estabilidade.
- *"Como se mede a semelhança?"* → com variáveis quantitativas, distância (euclidiana). Quanto menor a distância, maior a semelhança. Convém padronizar para evitar que uma variável com escala grande (rendimento) domine a distância.

## Questão 5 — Análise Discriminante

**Resposta: (d)** Classificar observações em grupos previamente definidos.

**Porquê**

- \(a) reduzir dimensionalidade sem grupos: é a PCA.
- \(b) identificar apenas outliers: não é o objetivo.
- \(c) agrupar sem informação prévia: é a Análise Classificatória.

**Quadro comparativo [slides]**

| | Classificatória | Discriminante | PCA |
|---|---|---|---|
| Grupos conhecidos? | Não | Sim | Não |
| Objetivo | Descobrir grupos | Distinguir e classificar | Reduzir dimensão |
| Tipo | Não supervisionada | Supervisionada | — |
| Maximiza | Homogeneidade interna | Separação entre grupos | Variância explicada |
| Exemplo | Segmentar clientes | Classificar novos clientes | Resumir 8 indicadores em 2 |

**Variações possíveis**

- *"Quantas funções discriminantes no máximo?"* → min(p, K−1). Exemplo: p = 5 variáveis e K = 3 grupos → min(5, 2) = **2**. Com 2 grupos há **1** função.
- *"Cliente com D = 2,1 e corte em 0?"* → D > 0 → Grupo 1; D < 0 → Grupo 2. O corte depende do procedimento e pode considerar probabilidades a priori.
- *"A função discriminante prova que o rendimento causa a pertença ao grupo?"* → não; classificação não é causalidade.

# 2. Grupo II — Respostas abertas

## Questão 6 — Classificar variáveis

**Resposta**

| Variável | Tipo |
|---|---|
| a) Número de compras | Quantitativa **discreta** (contagem) |
| b) Grau de satisfação (baixo/médio/alto) | Qualitativa **ordinal** (há ordem) |
| c) Montante gasto em euros | Quantitativa **contínua** (medição) |
| d) Área de residência (Norte/Centro/Sul) | Qualitativa **nominal** (sem ordem) |

**Regra [slides]:** o tipo da variável **não depende da forma como os valores são escritos**. Números não significam necessariamente variável quantitativa.

**Árvore de decisão rápida**

1. Representa categorias? → qualitativa. Tem ordem natural? Sim → ordinal; não → nominal.
2. Representa quantidades? → quantitativa. Resulta de contagem (valores isolados)? → discreta. Resulta de medição (qualquer valor num intervalo)? → contínua.

**Variações possíveis (exercício dos slides e outras)**

| Variável | Tipo |
|---|---|
| Código postal / código de cliente | Qualitativa **nominal** (é um identificador, mesmo escrito com números) |
| Número de filhos | Quantitativa discreta |
| Nível de risco 1–3 | Qualitativa **ordinal** |
| Rendimento mensal | Quantitativa contínua |
| Tipo de contrato | Qualitativa nominal |
| Tempo como cliente (anos) | Quantitativa contínua |
| Número de reclamações | Quantitativa discreta |
| Região de residência | Qualitativa nominal |
| Avaliação 1 a 5 | Qualitativa ordinal (nos slides) |
| Idade | Quantitativa contínua (nos slides) |

*Nota:* uma pergunta típica é "porque é que o código do cliente 10234 não é quantitativo?" → porque não faz sentido somar ou calcular médias de códigos; só identifica.

## Questão 7 — Associação entre sexo e preferência por compras online

**Resposta:** os dois são variáveis qualitativas (nominais; a segunda é binária). Usa-se uma **tabela de contingência** (2×2) e o **teste do qui-quadrado de independência**, com H₀: as variáveis são independentes contra H₁: existe associação. Se o p-value for < 0,05, rejeita-se a independência. Para medir a **intensidade** da associação, usa-se o **V de Cramér**.

**Exemplo trabalhado [slides: dados; cálculos: meus]**

| | Comprou | Não comprou | Total |
|---|---|---|---|
| Masculino | 80 | 20 | 100 |
| Feminino | 60 | 40 | 100 |
| Total | 140 | 60 | 200 |

Frequências esperadas sob independência: E = (total da linha × total da coluna) / n **[complemento: fórmula]**.

- Masculino/Comprou: 100 × 140 / 200 = 70. Masculino/Não comprou: 100 × 60 / 200 = 30.
- Feminino/Comprou: 70. Feminino/Não comprou: 30.

χ² = Σ (O − E)² / E = 10²/70 + 10²/30 + 10²/70 + 10²/30 ≈ **9,52**, com 1 grau de liberdade → p ≈ 0,002 (rejeita-se H₀). Nota: o slide indica "p-value = 0,001" como valor ilustrativo; o cálculo exato dá cerca de 0,002. Em ambos os casos conclui-se que há evidência de associação.

V de Cramér **[complemento: fórmula]**: V = √(χ² / (n · min(linhas−1, colunas−1))) = √(9,52 / 200) ≈ **0,22** → associação estatisticamente significativa, mas de intensidade fraca a moderada.

**Variações possíveis**

- *"Graus de liberdade?"* → (linhas − 1)(colunas − 1) **[complemento: fórmula]**. Na tabela 3×3 da ACS, df = 4.
- *"O p-value é < 0,001 e V = 0,08. Interpreta."* → [slides] estatisticamente significativo, mas **praticamente fraco**.
- *"Qual é a diferença entre significância estatística e relevância prática?"* → o p-value diz se há evidência de associação; o V diz a intensidade. Com amostras grandes, associações muito fracas podem ser significativas.
- *"O teste do qui-quadrado diz-nos onde está a associação?"* → não [slides ACS]; para isso usa-se a ACS e o mapa de correspondências.
- *Outras combinações:* canal de aquisição × abandono → qui-quadrado + V de Cramér; região × tipo de subscrição → idem.
- *Condição de aplicação [complemento]:* em geral exigem-se frequências esperadas razoáveis (regra habitual ≥ 5 por célula); com frequências muito baixas pode usar-se o teste exato de Fisher. Isto **não** está nos slides.

## Questão 8 — Pearson r = 0,78 (publicidade e vendas)

**a) Interpretação:** associação linear **positiva e forte**: valores mais altos de investimento em publicidade tendem a estar associados a vendas mais altas. (Complemento: r² ≈ 0,61, isto é, cerca de 61% da variação das vendas é partilhada linearmente com a publicidade.)

**b) Causalidade:** **não** se pode concluir. Associação responde a "movem-se juntas?"; causalidade responde a "uma influencia a outra?". Um r alto pode surgir porque [slides]:

1. a publicidade influencia as vendas;
2. as vendas influenciam a publicidade (empresas com mais vendas investem mais);
3. um **terceiro fator** influencia ambas (variável de confundimento).

**Exemplo clássico [slides]:** vendas de gelados e afogamentos têm correlação alta; o fator comum é a temperatura. Comprar gelados não causa afogamentos.

**Variações possíveis**

- *r = 0,80 entre satisfação e retenção. Qual afirmação é adequada?* [slides] → "Satisfação e retenção estão **associadas**" (não "aumentar a satisfação aumenta a retenção", nem "a satisfação causa a retenção").
- *r = −0,9?* → associação negativa forte.
- *r = 0,15 ou r ≈ 0: não há relação?* → só podemos dizer que a associação **linear** é fraca; pode existir relação não linear.
- *Satisfação × abandono com r_pb = −0,65, abandono = 1?* → clientes mais satisfeitos tendem a ter **menor** probabilidade de abandonar (o sinal depende da codificação).
- *Ordenações de lojas (ranks) satisfação vs rentabilidade [slides]:* os rankings (1,2,3,4,5,6) e (2,1,4,3,5,6) dão Spearman ≈ 0,89 (é o Pearson aplicado às ordens). Associação monótona positiva forte.

## Questão 9 — PCA aplicada a 4 variáveis padronizadas

**a) A PC1 tem cargas (loadings) elevadas e positivas nas quatro variáveis.**

*Interpretação:* a PC1 representa um fator **geral/global** de desempenho (um "índice geral"): trabalhadores com valores altos nas quatro variáveis têm score alto na PC1; os de valores baixos, score baixo. Exemplo semelhante nos slides: "desenvolvimento socioeconómico" para a 1.ª componente dos municípios.

*Limitação:* o nome atribuído à componente é uma **interpretação substantiva**, não automática; a PCA não determina o significado. Além disso, a PC1 não retém toda a informação (perde-se a variância das restantes componentes), a PCA **não estabelece causalidade**, e scores próximos numa componente **não** implicam observações semelhantes em todas as variáveis originais [slides].

**b) Verdadeiro/Falso**

| Afirmação | Resposta | Porquê |
|---|---|---|
| i) As componentes são combinações lineares das variáveis originais | **V** | É a definição |
| ii) A 1.ª componente explica sempre toda a variância | **F** | Explica a maior parte possível, mas não toda (só se houvesse uma única dimensão efetiva) |
| iii) A PCA pode reduzir a dimensionalidade | **V** | É o objetivo principal |

**Exemplo trabalhado [slides: dados; cálculos de percentagem: meus]**

| Comp. | Valor próprio | % variância | % acumulada |
|---|---|---|---|
| 1 | 3,62 | 45,3 | 45,3 |
| 2 | 1,74 | 21,8 | 67,1 |
| 3 | 0,82 | 10,3 | 77,4 |
| 4 | 0,61 | 7,6 | 85,0 |
| … | … | … | … |

- Critério de Kaiser: reter componentes com λ > 1 → reter **2** (3,62 e 1,74).
- Scree plot: procurar o "cotovelo"; aqui após a 2.ª componente → 2 componentes.
- Variância acumulada: 45,3 + 21,8 = 67,1% → 8 variáveis passam a 2 componentes preservando cerca de 67% da variância.
- A decisão deve resultar da análise **conjunta** de valores próprios, Kaiser, scree plot, variância acumulada e interpretabilidade.

**Variações possíveis**

- *"Define loading e score."* [slides] **Loading:** relaciona variável ↔ componente (magnitude = intensidade; sinal = direção); ajuda a interpretar o significado da componente. **Score:** relaciona observação ↔ componente; indica a posição da observação nessa dimensão.
- *"Porque se padronizam as variáveis?"* → para as pôr numa escala comparável: Z = (X − média)/desvio-padrão. Sem padronizar, variáveis com variância grande dominam.
- *"Para que servem o KMO e o teste de Bartlett?"* [slides] **KMO:** adequação dos dados (variância partilhada entre variáveis). **Bartlett:** H₀: R = I (matriz de correlações igual à identidade). Se p < 0,05, rejeita-se H₀ → as variáveis estão suficientemente correlacionadas. Exemplo dos slides: KMO = 0,84 (boa adequação), χ² = 842,6, gl = 28, p < 0,001 → prosseguir com a PCA. Atenção: o Bartlett não diz quais variáveis estão associadas nem que todas as correlações sejam fortes.
- *"Para quê analisar antes a matriz de correlações?"* → a PCA é útil quando há estrutura de correlação; se as variáveis forem independentes, não há nada a resumir.
- *"Variação: 2.ª componente com loadings altos em transportes, internet e cultura."* → "conectividade e participação" (exemplo dos slides). Dar nome é interpretação.
- *Variação de V/F:* "a PCA permite concluir que uma variável causa outra" → **F**. "Dois municípios com scores próximos são semelhantes em todas as variáveis" → **F**. "A PCA cria novas dimensões sintéticas" → **V**.
- *Possível cálculo:* "valores próprios 2,4; 1,1; 0,3; 0,2 (p = 4). Quantas componentes pelo Kaiser? Qual a % explicada pela 1.ª?" → 2 componentes; 2,4/4 = **60%** (com variáveis padronizadas, a soma dos valores próprios é p = 4) **[complemento: soma = p]**.

## Questão 10 — Associação tipo de atleta × modalidade (qui-quadrado e ACS)

**a) Objetivo do teste do qui-quadrado de Pearson:** testar se existe **associação estatisticamente significativa** entre as duas variáveis categóricas, comparando as frequências **observadas** com as frequências **esperadas sob independência**. H₀: independentes; H₁: associadas. Quanto maiores as diferenças (no conjunto da tabela) entre observado e esperado, maior a evidência contra H₀.

**b) Verdadeiro/Falso**

| Afirmação | Resposta | Porquê |
|---|---|---|
| i) Resultado significativo ⇒ associação forte | **F** | Significância ≠ intensidade (p < 0,001 e V = 0,08 → fraca) |
| ii) A ACS representa graficamente as categorias das duas variáveis | **V** | Produz o mapa de correspondências |
| iii) Proximidade no mapa ⇒ causalidade | **F** | A proximidade nem sequer deve ser interpretada isoladamente como medida de associação; e a ACS não estabelece causalidade |

**c) Associação significativa não implica causalidade** porque o teste e a ACS só mostram que as variáveis variam em conjunto, não **porquê** nem em que sentido. Pode dever-se a um fator de confundimento, a causalidade inversa ou ao acaso. Para afirmar causalidade são necessários desenho experimental/evidência adicional.

**Exemplo trabalhado [slides: tabela; cálculos de esperados: meus]**

| | Alimentação | Tecnologia | Moda | Total |
|---|---|---|---|---|
| Loja | 80 | 20 | 50 | 150 |
| Online | 30 | 90 | 60 | 180 |
| Misto | 40 | 50 | 30 | 120 |
| Total | 150 | 160 | 140 | 450 |

Esperado (Loja/Alimentação) = 150 × 150 / 450 = 50; observado = 80 → muito acima do esperado → "Loja" e "Alimentação" associadas. Esperado (Online/Tecnologia) = 180 × 160 / 450 = 64; observado = 90 → acima do esperado. df = (3−1)(3−1) = 4. O slide apresenta χ² = 72,4 como valor "suponha"; aplicando a fórmula à tabela obtém-se cerca de 67,6. Não te preocupes: os valores dos slides são ilustrativos; o que interessa é interpretar (p < 0,05 → rejeitar independência).

**Variações possíveis**

- *"Define inércia."* [slides] Mede a variabilidade da tabela; está relacionada com a distância entre frequências observadas e esperadas sob independência. As dimensões ordenam-se pela inércia que explicam (como a PCA com a variância).
- *"Coordenadas, contribuição e qualidade de representação (cos²)."* [slides] **Coordenada:** posição da categoria na dimensão. **Contribuição:** quanto a categoria contribui para construir a dimensão. **cos²:** quão bem a categoria é representada nas dimensões consideradas. *Uma coordenada grande não implica grande contribuição.*
- *Exemplo de leitura [slides]:* Online (coord. 0,72; contrib. 31,5%; cos² 0,82) → boa representação e contribuição importante; Loja (coord. −0,18; contrib. 2,8%; cos² 0,35) → pouca contribuição e representação mais fraca.
- *"ACS ou ACM?"* ACS: 2 variáveis categóricas (tabela de contingência). ACM: várias variáveis categóricas simultaneamente. Variáveis quantitativas não entram diretamente na ACM; só se categorizadas, com justificação.
- *"Um mapa de ACM é uma segmentação de clientes?"* → **não**; ACS e ACM exploram associações, não são clustering.
- *"O que a ACS não faz?"* → não estabelece causalidade, não cria grupos de indivíduos, não transforma associação em previsão.
- *V/F possíveis:* "O teste do qui-quadrado mostra onde está a associação" → **F**. "A ACS reduz a informação da tabela a poucas dimensões" → **V**. "Categorias próximas no mapa estão sempre fortemente associadas" → **F** (considerar coordenadas, contribuições e qualidade).

## Questão 11 — Silhouette e K-means

*(No PDF só aparecem as alíneas c) e d).)*

| k | Silhouette |
|---|---|
| 2 | 0,44 |
| 3 | 0,61 |
| 4 | 0,52 |

**c) Número de clusters:** **k = 3**, porque tem o silhouette médio mais alto (0,61), o que indica clusters mais coesos e mais bem separados.

**d) Uma limitação do K-means** [slides]: tem de se definir k à partida (não o determina automaticamente); o resultado depende da inicialização; é sensível a valores extremos e à escala das variáveis (rendimento em euros e idade em anos têm escalas muito diferentes → padronizar). **[complemento]:** assume clusters aproximadamente esféricos e de tamanho semelhante; só funciona com variáveis quantitativas.

**Como se calcula a silhouette [slides]:** s(i) = (b(i) − a(i)) / max{a(i), b(i)}, onde a(i) é a distância média da observação ao seu próprio grupo e b(i) a distância média ao grupo alternativo mais próximo. Valores mais altos indicam melhor coesão e separação.

**Exemplo numérico [meu]:** a(i) = 2 e b(i) = 5 → s(i) = (5 − 2)/5 = **0,6** (bem integrada). Se a(i) = 5 e b(i) = 2 → s(i) = (2 − 5)/5 = **−0,6** (provavelmente mal classificada). Se a(i) = b(i) → s(i) = 0 (na fronteira).

**Como funciona o K-means [slides]:** 1) escolher k; 2) definir centros iniciais; 3) atribuir cada observação ao centro mais próximo; 4) recalcular os centros; 5) repetir até estabilizar.

**Variações possíveis**

- *"Silhouette: k=2 → 0,30; k=3 → 0,28; k=4 → 0,29. O que concluir?"* → valores baixos e muito próximos: não há evidência forte de estrutura de grupos; a escolha deve considerar dendrograma, estabilidade, tamanho dos grupos e interpretabilidade. Não decidir só por um indicador.
- *"A escolha de k deve depender apenas da silhouette?"* → não [slides]: considerar também dendrograma, estabilidade, tamanho dos grupos, interpretabilidade e conhecimento do contexto.
- *"Tens 3 clusters com médias de idade e rendimento. Como caracterizas?"* → comparar variáveis entre grupos, mas **não só pelas médias**: ver dispersão e distribuição, tamanho dos grupos, variabilidade dentro de cada grupo.
- *"Se os clusters diferem no abandono (variável não usada no clustering), prova que o clustering está certo?"* → **não**; nem estabelece causalidade [slides].
- *"Dois métodos dão soluções semelhantes (hierárquico 0,39, K-means 0,42)."* → semelhança é evidência complementar, mas não garante robustez absoluta.
- *"Porque padronizar antes do clustering?"* → para a distância não ser dominada pela variável de maior escala; **mas não resolve outliers**.
- *"O clustering garante que há uma segmentação natural?"* → não; um cluster é uma estrutura definida de acordo com as variáveis, a medida de distância e o método usados.

## Questão 12 — Matriz de confusão

| | Previsto: Com doença | Previsto: Sem doença |
|---|---|---|
| **Real: Com doença** | 30 | 20 |
| **Real: Sem doença** | 10 | 40 |

Classe positiva = "Com doença".

**a)** TP = 30 (doente previsto doente); FN = 20 (doente previsto sem doença); FP = 10 (sem doença previsto doente); TN = 40.

**b) Accuracy** = (TP + TN) / total = (30 + 40) / 100 = **0,70 (70%)**.

**c) Recall (sensibilidade)** = TP / (TP + FN) = 30 / 50 = **0,60 (60%)**: dos doentes reais, o modelo identificou 60%.

**d) Precision** = TP / (TP + FP) = 30 / 40 = **0,75 (75%)**: dos classificados como doentes, 75% são efetivamente doentes.

**Como ler a matriz sem te enganares:** as **linhas** são a realidade, as **colunas** a previsão. TP e TN estão na diagonal principal (acertos).

**Variações possíveis**

- *F1-score* [slides] = 2 · (Precision · Recall) / (Precision + Recall) = 2 · 0,75 · 0,60 / 1,35 ≈ **0,667**.
- *Balanced accuracy* [slides] = média dos recalls dos grupos. Recall "Com doença" = 0,60; recall "Sem doença" = 40/50 = 0,80 → (0,60 + 0,80)/2 = **0,70**. Aqui coincide com a accuracy porque os grupos têm o mesmo tamanho (50 e 50).
- *Trocar a classe positiva para "Sem doença":* TP = 40, FN = 10, FP = 20, TN = 30 → recall = 40/50 = 0,80; precision = 40/60 ≈ 0,667. Isto mostra que **recall e precision dependem de qual é a classe positiva**; a accuracy não.
- *Erros:* FP = erro do tipo I (falso alarme); FN = erro do tipo II (omissão) [slides]. Em contexto médico, os FN (doentes não detetados) são normalmente os mais graves → olhar para o **recall**.
- *"Accuracy alta significa bom modelo?"* [slides] Não necessariamente: com grupos muito desequilibrados, uma accuracy alta pode esconder um desempenho muito fraco num grupo. Exemplo dos slides: accuracy 84,3%, mas recall do Grupo 1 de 2% e balanced accuracy 50,4%.
- *Exemplo dos slides para treinar:* real Não: 210/26; real Sim: 18/26 (positiva = Sim) → TP = 26, FN = 18, FP = 26, TN = 210; accuracy = 236/280 = 0,843; recall = 26/44 = 0,591; precision = 26/52 = 0,50; F1 ≈ 0,542.
- *Treino e validação [slides]:* avaliar só na amostra usada para estimar o modelo é demasiado otimista; usar validação cruzada ou amostra de teste.
- *Pressupostos da Discriminante Linear [slides]:* variáveis quantitativas adequadas, sem multicolinearidade grave, normalidade multivariada dentro dos grupos, matrizes de covariância aproximadamente iguais, sem observações excessivamente influentes. **Teste de Box:** H₀: Σ₁ = Σ₂ = … = Σ_K; se p < 0,05, há evidência contra a igualdade das matrizes de covariância; um resultado não significativo não "prova" igualdade.

# 3. Outros pontos do programa que podem aparecer (fora do teste-modelo)

## 3.1 Análise preliminar

- **Matriz de dados:** linhas = unidades estatísticas; colunas = variáveis. **População** vs **amostra** vs **unidade estatística** (exemplo: população = todos os clientes; amostra = os do conjunto de dados; unidade = cada cliente).
- **Qualitativas:** frequência absoluta e relativa; gráfico de barras (mais fácil de comparar) e circular (poucas categorias).
- **Quantitativas:** tendência central (média, mediana, moda), dispersão (amplitude, variância, desvio-padrão, AIQ = Q3 − Q1), quartis, boxplot, histograma (classes de intervalos consecutivos, barras contíguas).
- **Simetria:** simétrica → média ≈ mediana ≈ moda; cauda à direita → média > mediana > moda; cauda à esquerda → média < mediana < moda.
- **Qualidade dos dados:** valores omissos (porquê? ocorrem ao acaso?), inconsistências (valores impossíveis, categorias escritas de formas diferentes, unidades inconsistentes, duplicados, valores fora dos limites).
- **Exemplo de cálculo:** dados 2, 3, 3, 4, 5, 3, 6 → moda = 3; ordenados 2, 3, 3, 3, 4, 5, 6 → mediana = 3 (4.º valor); média = 26/7 ≈ 3,71.
- **Exemplo de leitura de boxplot [slides]:** Q1 = 1400, mediana = 1600, Q3 = 1800 → AIQ = 400; 3000 e 3500 são possíveis valores extremos.

## 3.2 Análise bivariada

- **Medidas de associação ≠ causalidade.** A significância estatística não implica relevância prática. A interpretação é mais importante do que o cálculo.
- **Ponto-bisserial:** codificar a binária (por exemplo Abandono = Sim → 1, Não → 0); é o Pearson entre a quantitativa e a binária codificada. O **sinal** depende da codificação.

## 3.3 ACM

- Inércia corrigida por dimensão (exemplo dos slides: 57,3%, 15,6%, 13,8%, 8,3%; acumulada 72,9% nas duas primeiras).
- Interpretação das dimensões como **contrastes** entre conjuntos de categorias (por exemplo 50+ e Premium contra 35–49 e Standard).
- Variáveis quantitativas só entram se categorizadas, com justificação.

# 4. Banco de treino — variações para resolveres sozinho

*(Respostas no fim.)*

**Escolha múltipla**

1. Num boxplot, um ponto isolado acima do bigode superior indica: (a) a mediana; (b) um possível valor extremo; (c) a moda; (d) um valor omisso.
2. O Spearman é adequado quando: (a) ambas as variáveis são nominais; (b) as variáveis são ordinais ou há outliers extremos; (c) uma variável é binária e a outra qualitativa; (d) se quer testar a causalidade.
3. Num dendrograma, um corte horizontal serve para: (a) eliminar outliers; (b) definir o número de clusters; (c) calcular o silhouette; (d) padronizar as variáveis.
4. O critério de Kaiser recomenda reter as componentes com: (a) λ > 1; (b) λ < 1; (c) variância acumulada > 50%; (d) loadings > 0,5.
5. Na ACM podem entrar diretamente: (a) idade e rendimento; (b) região, sexo e canal de compra; (c) apenas uma variável; (d) apenas variáveis binárias.
6. Uma accuracy de 90% garante que: (a) o modelo identifica bem todos os grupos; (b) não há erros do tipo II; (c) nada, se os grupos forem muito desequilibrados; (d) o recall é 90%.

**Resposta curta / cálculo**

7. Classifica: número de reclamações; nível de escolaridade (básico/secundário/superior); temperatura em °C; tipo de contrato.
8. Qual medida de associação usarias para: (i) idade × rendimento; (ii) ranking de fornecedores × ranking de preço; (iii) satisfação (0-10) × abandono (Sim/Não); (iv) região × tipo de produto?
9. r = −0,70 entre preço e procura de um produto. Interpreta e discute causalidade.
10. Dados: 4, 6, 6, 7, 9, 40. Calcula média e mediana e indica qual representa melhor o valor típico.
11. Tabela de contingência 2×2 com totais: linha 1 = 60 (30 e 30), linha 2 = 40 (10 e 30), n = 100. Calcula as frequências esperadas de cada célula.
12. Valores próprios (p = 5, variáveis padronizadas): 2,5; 1,2; 0,6; 0,4; 0,3. Quantas componentes pelo Kaiser? Qual a % de variância acumulada com 2 componentes?
13. Silhouette: k = 2 → 0,28; k = 3 → 0,55; k = 4 → 0,50. Que k escolhes e que mais verificarias?
14. Matriz de confusão (positiva = Fraude): real Fraude: 15 previstos Fraude e 5 previstos Não; real Não fraude: 10 previstos Fraude e 170 previstos Não. Calcula accuracy, recall, precision, F1 e balanced accuracy. Comenta.
15. V/F: (i) a ACM é um método de clustering; (ii) a Análise Discriminante é supervisionada; (iii) o K-means determina automaticamente o número de grupos; (iv) padronizar as variáveis elimina o efeito dos outliers; (v) a PCA exige variáveis qualitativas.
16. p = 4 variáveis e K = 5 grupos. Quantas funções discriminantes no máximo?

## Respostas

1. (b).
2. (b).
3. (b).
4. (a).
5. (b).
6. (c).
7. Reclamações: quantitativa discreta. Escolaridade: qualitativa ordinal. Temperatura: quantitativa contínua. Tipo de contrato: qualitativa nominal.
8. (i) Pearson; (ii) Spearman; (iii) ponto-bisserial; (iv) qui-quadrado + V de Cramér.
9. Associação linear negativa forte: preços mais altos tendem a corresponder a menor procura. Não implica causalidade (podem existir variáveis de confundimento, causalidade inversa, etc.).
10. Média = 72/6 = 12; mediana = (6 + 7)/2 = 6,5. A mediana representa melhor o valor típico (o 40 é um valor extremo que puxa a média).
11. Totais das colunas: 40 e 60. Esperados: linha 1 → 60·40/100 = 24 e 60·60/100 = 36; linha 2 → 40·40/100 = 16 e 40·60/100 = 24.
12. Kaiser: 2 componentes (2,5 e 1,2). Variância acumulada = (2,5 + 1,2)/5 = 74%.
13. k = 3 (silhouette 0,55 mais alto); verificar também dendrograma, estabilidade, tamanho dos grupos, interpretabilidade e padronização/outliers.
14. TP = 15, FN = 5, FP = 10, TN = 170, total = 200. Accuracy = 185/200 = 0,925. Recall = 15/20 = 0,75. Precision = 15/25 = 0,60. F1 = 2·0,60·0,75/1,35 ≈ 0,667. Recall do grupo "Não fraude" = 170/180 ≈ 0,944; balanced accuracy = (0,75 + 0,944)/2 ≈ 0,847. Comentário: a accuracy (92,5%) é inflacionada pelo grupo maioritário; para a fraude identificam-se 75% dos casos e 40% dos alertas são falsos alarmes.
15. (i) F; (ii) V; (iii) F; (iv) F; (v) F (usa variáveis quantitativas).
16. min(4, 5 − 1) = min(4, 4) = 4.

# 5. Frases-chave para memorizar [slides]

- "Não começamos pelo método. Começamos pela pergunta."
- Os dados, por si só, não são informação; a análise termina quando interpretamos o resultado.
- **Correlação não implica causalidade**; associação ≠ causalidade.
- **Significância estatística ≠ relevância prática** (p < 0,001 com V = 0,08 → fraca).
- **Padronizar** resolve a escala, **não** os outliers.
- Um valor extremo **não se elimina automaticamente**: percebe-se a origem.
- **PCA:** reduzir dimensão preservando variância; as componentes são combinações lineares; os nomes são interpretação.
- **ACS/ACM:** exploram associações entre categorias; **não** são clustering; proximidade no mapa não se interpreta isoladamente.
- **Clustering:** grupos desconhecidos; k tem de ser justificado (silhouette + interpretabilidade + estabilidade).
- **Discriminante:** grupos conhecidos; avaliar **por grupo**, não só a accuracy; validar fora da amostra.
- Um bom resultado na amostra de estimação não garante bom desempenho em novos casos.
