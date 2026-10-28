---
title: "Análise de Dados — Guia de estudo para o exame de 2 de novembro"
subtitle: "Teste-modelo resolvido e explicado, com exemplos e variações possíveis"
lang: pt-PT
---

# 0. Como usar este guia

**Formato do exame (email da professora):** 60 minutos, cotado para 20 valores, uma folha A4 manuscrita (frente e verso). Pode ter escolha múltipla, resposta aberta, cálculos, interpretação de resultados e justificação. Depois do exame há uma discussão oral individual do trabalho (5 a 10 minutos).

**Estrutura de cada questão**

1. O **enunciado do teste-modelo** aparece em citação no início.
2. A **resposta** e, indentada por baixo, a **razão** (com o documento e a página onde a matéria está).
3. As **variações possíveis**: cada pergunta tem por baixo, indentadas, a **resposta** e a **justificação**.

**Como estão indicadas as fontes**

- Entre parênteses retos aparece o **nome do documento e a página**, por exemplo [Análise Preliminar, p. 29]. As páginas são as do PDF (nos PDFs com rodapé "n / N" coincidem com o número do slide).
- **[complemento]** = conhecimento geral útil que **não** está nos documentos da professora. Na prova, usa de preferência o vocabulário dos documentos.

| Nome usado no guia | Ficheiro |
|---|---|
| Apresentação da UC | 0_Apresentação_da_UC.pdf |
| Análise Preliminar | 1_Analise_Preliminar_de_Dados.pdf |
| Slides 18/09 | Slides_Aula_20260918.pdf (medidas de associação, em inglês) |
| PCA | PCA.pdf |
| ACS_ACM | ACS_ACM.pdf |
| Análise Classificatória | Análise_Classificatória.pdf |
| Análise Discriminante | Análise_Discriminante.pdf |
| Overview | overview.pdf |
| Teste-modelo | Modelo.pdf |

**Ideia que atravessa a UC inteira:** *não começamos pelo método, começamos pela pergunta.* Antes de escolher uma técnica, pergunta-te: que tipo de variáveis tenho? Qual é a pergunta de investigação? Tenho grupos previamente definidos? [Overview, p. 15]

## 0.1 Mapa de decisão: pergunta → método [Overview, p. 13]

| Pergunta | Método |
|---|---|
| Como resumir muitas variáveis quantitativas? | **PCA / ACP** |
| Que associações existem entre categorias? | **Análise de Correspondências** (ACS com 2 variáveis, ACM com várias) |
| Que grupos semelhantes existem (grupos desconhecidos)? | **Análise Classificatória** (clustering, não supervisionada) |
| A que grupo pertence uma nova observação (grupos conhecidos)? | **Análise Discriminante** (supervisionada) |

## 0.2 Mapa de decisão: tipos de variáveis → medida de associação [Slides 18/09, p. 45]

| Variável X | Variável Y | Medida |
|---|---|---|
| Quantitativa | Quantitativa | **Pearson** (associação linear) |
| Ordinal | Ordinal | **Spearman** (associação monótona, usa ordens/ranks) |
| Quantitativa | Binária | **Correlação ponto-bisserial** (Pearson com a binária codificada 0/1) |
| Categórica | Categórica | **Qui-quadrado** de independência **+ V de Cramér** |

Regras de bolso [Slides 18/09, p. 23]: quantitativas → Pearson; rankings → Spearman; outliers extremos → Spearman pode ser mais robusto.

# 1. Grupo I — Escolha múltipla

## Questão 1 — Outlier

> **Enunciado.** Na análise exploratória de dados, um *outlier* corresponde a:\
> **a)** Uma observação que apresenta valores iguais à média.\
> **b)** Uma observação que se distingue significativamente das restantes.\
> **c)** Uma variável categórica com poucas categorias.\
> **d)** Uma observação que deve ser sempre eliminada.

- **Resposta: (b)**
    - **Razão:** um valor extremo é uma observação muito afastada da maioria dos restantes valores [Análise Preliminar, p. 29]. Pode resultar de erro de introdução, erro de medição ou de uma situação pouco frequente mas real [Análise Preliminar, p. 29].
    - **Porque as outras estão erradas:**
        - **a)** valores iguais à média: é um valor central, não um valor extremo.
        - **c)** variável categórica com poucas categorias: não tem relação com outliers.
        - **d)** "deve ser sempre eliminada": **falso**. Um valor extremo não deve ser automaticamente eliminado; primeiro devemos compreender a sua origem e avaliar o impacto na análise [Análise Preliminar, p. 29].

**Exemplo:** rendimentos 1200, 1300, 1400, 1500 e 10000. A média é 3080 e a mediana é 1400. A média é sensível a valores extremos e a mediana é geralmente mais robusta [Análise Preliminar, p. 16].

**Variações possíveis**

- **Pergunta:** "Qual é a medida de tendência central mais adequada se houver outliers?"
    - **Resposta:** a mediana.
    - **Justificação:** a média é sensível a valores extremos; a mediana é geralmente mais robusta [Análise Preliminar, p. 16].
- **Pergunta:** "Idade = 25, 31, 42, −3, 250. O que fazer?"
    - **Resposta:** −3 e 250 são valores impossíveis ou incoerentes; verificar se são erros de registo antes de decidir (corrigir, tratar como omisso ou excluir com justificação).
    - **Justificação:** antes de analisar, é necessário perceber se os valores representam erros de registo ou situações reais [Análise Preliminar, p. 28].
- **Pergunta:** "Num boxplot, como se identificam possíveis valores extremos?"
    - **Resposta:** como pontos isolados afastados da caixa e dos "bigodes".
    - **Justificação:** o boxplot mostra mediana, quartis, dispersão e possíveis valores extremos; no exemplo, 3000 e 3500 são possíveis valores extremos [Análise Preliminar, p. 20 e 21]. A convenção habitual é fora de [Q1 − 1,5·AIQ ; Q3 + 1,5·AIQ] [complemento].
- **Pergunta:** "Numa distribuição com cauda à direita, qual a relação entre média, mediana e moda?"
    - **Resposta:** média > mediana > moda. Com cauda à esquerda: média < mediana < moda. Simétrica: média ≈ mediana ≈ moda.
    - **Justificação:** [Análise Preliminar, p. 26].
- **Pergunta:** "Padronizar as variáveis elimina o efeito dos outliers no clustering?"
    - **Resposta:** não.
    - **Justificação:** a padronização resolve um problema de escala, mas não elimina a influência dos valores extremos [Análise Classificatória, p. 5 e 21].

## Questão 2 — Coeficiente de correlação de Pearson

> **Enunciado.** O coeficiente de correlação de Pearson permite avaliar:\
> **a)** A associação linear entre duas variáveis quantitativas.\
> **b)** A causalidade entre duas variáveis.\
> **c)** A associação entre quaisquer duas variáveis, independentemente do seu tipo.\
> **d)** A diferença entre duas médias.

- **Resposta: (a)**
    - **Razão:** o Pearson usa-se quando ambas as variáveis são quantitativas e o objetivo é medir a associação **linear**; −1 ≤ r ≤ 1 [Slides 18/09, p. 8]. Indica direção e força, mas não capta todos os tipos de relação [Slides 18/09, p. 15].
    - **Porque as outras estão erradas:**
        - **b)** causalidade: uma forte associação não implica causalidade [Slides 18/09, p. 54].
        - **c)** qualquer tipo de variável: a medida depende dos tipos de variáveis (ordinais → Spearman; quantitativa × binária → ponto-bisserial; categóricas → qui-quadrado + V de Cramér) [Slides 18/09, p. 45].
        - **d)** diferença entre médias: não é isso que o r mede.

**Exemplos:** r = 0,90 → associação positiva; r = −0,90 → associação negativa [Slides 18/09, p. 9 e 10].

**Variações possíveis**

- **Pergunta:** "r ≈ 0 significa que não há associação?"
    - **Resposta:** não; significa apenas que a associação **linear** é fraca. Pode haver uma relação não linear.
    - **Justificação:** [Slides 18/09, p. 12 e 13] (os gráficos mostram r = 0,15 e r = −0,002 com relações claras mas não lineares).
- **Pergunta:** "Pearson ou Spearman? (A) idade e salário; (B) ranking de desempenho e ranking de satisfação; (C) horas de estudo e nota final com outliers extremos."
    - **Resposta:** (A) Pearson; (B) Spearman; (C) Spearman.
    - **Justificação:** quantitativas → Pearson; rankings → Spearman; outliers extremos → Spearman pode ser mais robusto [Slides 18/09, p. 22 e 23].
- **Pergunta:** "Qual medida usar para satisfação (0–10) e abandono (Sim/Não)?"
    - **Resposta:** correlação ponto-bisserial.
    - **Justificação:** uma variável é quantitativa e a outra é binária [Slides 18/09, p. 30 e 58 a 61]. É o Pearson entre a quantitativa e a binária codificada (Sim → 1, Não → 0) [Slides 18/09, p. 31 e 32].
- **Pergunta:** "Qual medida usar para género e abandono? E para canal de aquisição e abandono?"
    - **Resposta:** qui-quadrado de independência + V de Cramér, nos dois casos.
    - **Justificação:** são duas variáveis categóricas [Slides 18/09, p. 57, 59, 60 e 61].
- **Pergunta:** "O Pearson assume normalidade?"
    - **Resposta:** sim, os documentos referem que assume distribuição Normal.
    - **Justificação:** [Slides 18/09, p. 15]. Se houver outliers extremos, o Spearman pode ser mais robusto [Slides 18/09, p. 20 e 23].

## Questão 3 — Objetivo principal da PCA

> **Enunciado.** O principal objetivo da Análise de Componentes Principais (PCA) é:\
> **a)** Classificar observações em grupos previamente definidos.\
> **b)** Reduzir a dimensionalidade, preservando tanta variância quanto possível.\
> **c)** Identificar diretamente relações de causalidade.\
> **d)** Prever exclusivamente variáveis categóricas.

- **Resposta: (b)**
    - **Razão:** a PCA transforma X₁,…,Xₚ em componentes C₁,…,Cₚ ordenadas pela variância que explicam; a ideia central é reduzir a dimensionalidade preservando tanta informação quanto possível [PCA, p. 3].
    - **Porque as outras estão erradas:**
        - **a)** classificar em grupos previamente definidos: é a Análise Discriminante [Análise Discriminante, p. 26].
        - **c)** causalidade: a PCA não estabelece causalidade nem demonstra que uma variável causa outra [PCA, p. 22].
        - **d)** prever variáveis categóricas: a PCA não faz previsão; o exemplo trabalha com variáveis quantitativas [PCA, p. 5].

**Variações possíveis**

- **Pergunta:** "A PCA usa informação sobre grupos? O que maximiza, comparada com a Análise Discriminante?"
    - **Resposta:** não usa grupos. A PCA maximiza a **variância explicada**; a Discriminante maximiza a **separação entre grupos**.
    - **Justificação:** [Análise Discriminante, p. 26].
- **Pergunta:** "Quantas componentes principais existem no máximo? Quanto somam os valores próprios, com variáveis padronizadas?"
    - **Resposta:** tantas quantas as variáveis (p). Com variáveis padronizadas somam p (no exemplo, 3,62 + 1,74 + … + 0,18 = 8).
    - **Justificação:** X₁,…,Xₚ → C₁,…,Cₚ [PCA, p. 3]; tabela de valores próprios do exemplo com 8 indicadores [PCA, p. 10]. A soma = p é conhecimento geral [complemento].
- **Pergunta:** "Que tipo de variáveis entram numa PCA?"
    - **Resposta:** variáveis quantitativas.
    - **Justificação:** no exemplo, os oito indicadores são quantitativos e podem ser padronizados [PCA, p. 5].
- **Pergunta:** "Dá um exemplo de pergunta a que a PCA responde."
    - **Resposta:** "Podemos resumir oito variáveis de desempenho em duas ou três dimensões?"
    - **Justificação:** [Overview, p. 4, 5 e 16].

## Questão 4 — Clustering hierárquico aglomerativo

> **Enunciado.** Num método de clustering hierárquico aglomerativo:\
> **a)** Todas as observações começam num único cluster.\
> **b)** O número de clusters tem de ser definido antes de qualquer cálculo.\
> **c)** Cada observação começa num cluster e os clusters são sucessivamente agregados.\
> **d)** As observações são classificadas com base em grupos previamente conhecidos.

- **Resposta: (c)**
    - **Razão:** na abordagem aglomerativa, 1) inicialmente cada observação constitui um grupo; 2) os grupos mais próximos são sucessivamente agregados; 3) o processo continua até existir um único grupo [Análise Classificatória, p. 7]. O resultado representa-se num dendrograma [Análise Classificatória, p. 7 e 8].
    - **Porque as outras estão erradas:**
        - **a)** é o contrário: começa-se com n grupos, não com um.
        - **b)** falso: no hierárquico o k pode ser escolhido depois (corte do dendrograma); é no K-means que o k é normalmente definido antes [Análise Classificatória, p. 19].
        - **d)** é a Análise Discriminante (grupos conhecidos); no clustering a pertença aos grupos não é conhecida [Análise Classificatória, p. 3].

**Variações possíveis**

- **Pergunta:** "Diferenças entre hierárquico e K-means."
    - **Resposta:** estrutura (hierarquia vs partição); k (pode ser escolhido depois vs normalmente definido antes); resultado (dendrograma vs k grupos); cálculo (progressivo vs iterativo); utilidade (explorar estrutura vs obter uma partição).
    - **Justificação:** [Análise Classificatória, p. 19]. Podem ser usados de forma complementar [Análise Classificatória, p. 19].
- **Pergunta:** "O que representa a altura num dendrograma e como se define o número de clusters?"
    - **Resposta:** a altura representa a distância entre os grupos; um corte horizontal define o número de clusters.
    - **Justificação:** [Análise Classificatória, p. 8]. O número de grupos não deve ser escolhido apenas porque o dendrograma "parece" indicar um corte; devem considerar-se distâncias, critérios de validação, interpretabilidade e estabilidade [Análise Classificatória, p. 9].
- **Pergunta:** "O que faz o método de Ward?"
    - **Resposta:** em cada passo junta os grupos cuja fusão provoca o menor aumento da variabilidade interna dos grupos.
    - **Justificação:** [Análise Classificatória, p. 10].
- **Pergunta:** "Como se mede a semelhança e porque convém padronizar?"
    - **Resposta:** com variáveis quantitativas, por medidas de distância (por exemplo a euclidiana); quanto menor a distância, maior a semelhança. Padroniza-se para que variáveis de escala grande (rendimento em euros) não dominem a distância.
    - **Justificação:** [Análise Classificatória, p. 4 e 5].

## Questão 5 — Análise Discriminante

> **Enunciado.** A análise discriminante é utilizada principalmente para:\
> **a)** Reduzir a dimensionalidade sem considerar grupos.\
> **b)** Identificar exclusivamente observações atípicas.\
> **c)** Agrupar observações sem informação prévia sobre os grupos.\
> **d)** Classificar observações em grupos previamente definidos.

- **Resposta: (d)**
    - **Razão:** a Análise Discriminante estuda diferenças entre grupos previamente definidos, identifica as variáveis que mais contribuem para os distinguir e classifica novas observações em grupos conhecidos [Análise Discriminante, p. 3]. É uma abordagem supervisionada [Overview, p. 12].
    - **Porque as outras estão erradas:**
        - **a)** reduzir a dimensionalidade sem grupos: é a PCA [Análise Discriminante, p. 26].
        - **b)** identificar apenas observações atípicas: não é o objetivo da análise.
        - **c)** agrupar sem informação prévia: é a Análise Classificatória [Análise Discriminante, p. 25; Overview, p. 12].

**Quadro comparativo** [Análise Discriminante, p. 25 e 26; Overview, p. 12]

| | Classificatória | Discriminante | PCA |
|---|---|---|---|
| Grupos conhecidos? | Não | Sim | Não |
| Objetivo | Descobrir grupos | Distinguir e classificar | Reduzir dimensão |
| Tipo | Não supervisionada | Supervisionada | — |
| Maximiza | Homogeneidade interna dos grupos | Separação entre grupos | Variância explicada |
| Exemplo | Segmentar clientes | Classificar novos clientes | Resumir 8 indicadores em 2 |

**Variações possíveis**

- **Pergunta:** "Quantas funções discriminantes se podem obter com p = 5 variáveis e K = 3 grupos? E com 2 grupos?"
    - **Resposta:** min(5, 2) = 2 funções com K = 3. Com 2 grupos, 1 função.
    - **Justificação:** o número máximo é min(p, K − 1) [Análise Discriminante, p. 10]. No caso de dois grupos há uma função D = a₀ + a₁X₁ + … + aₚXₚ [Análise Discriminante, p. 7].
- **Pergunta:** "Um cliente tem D = 2,1 e o ponto de corte é D = 0. A que grupo é atribuído?"
    - **Resposta:** ao Grupo 1 (D > 0 → Grupo 1; D < 0 → Grupo 2).
    - **Justificação:** [Análise Discriminante, p. 9]. O ponto de corte depende do procedimento e pode considerar as probabilidades a priori dos grupos.
- **Pergunta:** "Um coeficiente discriminante elevado para o rendimento prova que o rendimento causa a pertença ao grupo?"
    - **Resposta:** não.
    - **Justificação:** a análise discriminante distingue grupos e classifica observações; não estabelece relações causais [Análise Discriminante, p. 24].
- **Pergunta:** "Num problema, os grupos são desconhecidos e queremos descobrir perfis de atletas. Que método?"
    - **Resposta:** Análise Classificatória (clustering).
    - **Justificação:** sem definir previamente os grupos, procuram-se perfis semelhantes [Overview, p. 8 e 16].

# 2. Grupo II — Respostas abertas

## Questão 6 — Classificar variáveis

> **Enunciado.** Classifique cada uma das seguintes variáveis quanto à sua natureza, indicando o tipo de variável mais adequado.\
> **a)** Número de compras efetuadas por um cliente.\
> **b)** Grau de satisfação: baixo, médio ou alto.\
> **c)** Montante gasto por cliente, em euros.\
> **d)** Área de residência: Norte, Centro ou Sul.

- **a) Quantitativa discreta**
    - **Razão:** resulta de uma contagem e assume valores isolados (o exemplo dos documentos é exatamente "número de compras") [Análise Preliminar, p. 10].
- **b) Qualitativa ordinal**
    - **Razão:** as categorias têm uma ordem natural (satisfação: baixa, média, alta) [Análise Preliminar, p. 8].
- **c) Quantitativa contínua**
    - **Razão:** resulta de uma medição e pode assumir qualquer valor num intervalo (rendimento é exemplo de contínua) [Análise Preliminar, p. 10].
- **d) Qualitativa nominal**
    - **Razão:** as categorias não têm ordem natural (região: Norte, Centro, Sul) [Análise Preliminar, p. 8].

**Regra a lembrar:** o tipo da variável não é determinado pela forma como os valores são escritos; números não significam necessariamente variável quantitativa [Análise Preliminar, p. 9].

**Árvore de decisão rápida** [Análise Preliminar, p. 7]: representa categorias → qualitativa (com ordem → ordinal; sem ordem → nominal). Representa quantidades → quantitativa (contagem → discreta; medição → contínua).

**Variações possíveis** (exercício dos documentos: [Análise Preliminar, p. 11])

- **Pergunta:** "Classifica: código postal."
    - **Resposta:** qualitativa nominal.
    - **Justificação:** é um identificador escrito com números; o código do cliente é o exemplo dado de qualitativa nominal [Análise Preliminar, p. 9].
- **Pergunta:** "Classifica: número de filhos; número de reclamações."
    - **Resposta:** quantitativas discretas.
    - **Justificação:** resultam de contagens [Análise Preliminar, p. 10].
- **Pergunta:** "Classifica: nível de risco (1 a 3); avaliação 1 a 5; grau de satisfação 1 a 5."
    - **Resposta:** qualitativas ordinais.
    - **Justificação:** os números codificam categorias com ordem; "Grau de satisfação: 1, 2, 3, 4, 5 → qualitativa ordinal" [Análise Preliminar, p. 8 e 9].
- **Pergunta:** "Classifica: rendimento mensal; tempo como cliente (em anos); idade."
    - **Resposta:** quantitativas contínuas.
    - **Justificação:** resultam de medições; rendimento, idade e tempo de utilização estão listados como contínuas [Análise Preliminar, p. 10].
- **Pergunta:** "Classifica: tipo de contrato; região de residência; sexo."
    - **Resposta:** qualitativas nominais.
    - **Justificação:** categorias sem ordem natural [Análise Preliminar, p. 8].
- **Pergunta:** "Porque é que o código do cliente 10234 não é quantitativo?"
    - **Resposta:** porque não faz sentido operar aritmeticamente com códigos; só identificam o cliente.
    - **Justificação:** as variáveis quantitativas permitem operações aritméticas com significado [Análise Preliminar, p. 10]; o código de cliente é qualitativa nominal [Análise Preliminar, p. 9].

## Questão 7 — Sexo e preferência por compras online

> **Enunciado.** Pretende-se estudar a associação entre o sexo de um cliente e a sua preferência por compras online. Que tipo de tabela e que teste estatístico poderão ser utilizados para analisar esta associação? Justifique brevemente a sua resposta.

- **Resposta:** tabela de contingência (2×2) e teste do qui-quadrado de independência, com H₀: as variáveis são independentes contra H₁: existe associação. Para medir a intensidade da associação, usa-se o V de Cramér.
    - **Razão:** as duas variáveis são qualitativas (categóricas), e para duas variáveis categóricas a medida adequada é o qui-quadrado + V de Cramér [Slides 18/09, p. 38 e 45]. O qui-quadrado testa se há evidência de associação [Slides 18/09, p. 40 e 41]; o V mede a força da associação (0 ≤ V ≤ 1) [Slides 18/09, p. 43].

**Exemplo trabalhado** (dados dos documentos [Slides 18/09, p. 39]; cálculos meus)

| | Comprou | Não comprou | Total |
|---|---|---|---|
| Masculino | 80 | 20 | 100 |
| Feminino | 60 | 40 | 100 |
| Total | 140 | 60 | 200 |

Frequências esperadas sob independência: E = (total da linha × total da coluna) / n [complemento: fórmula]. Compara-se com as observadas [ACS_ACM, p. 8].

- Masculino/Comprou: 100 × 140 / 200 = 70. Masculino/Não comprou: 100 × 60 / 200 = 30.
- Feminino/Comprou: 70. Feminino/Não comprou: 30.

χ² = Σ (O − E)² / E = 10²/70 + 10²/30 + 10²/70 + 10²/30 ≈ **9,52**, com 1 grau de liberdade → p ≈ 0,002, rejeita-se H₀. O documento indica "p-value = 0,001" como valor ilustrativo [Slides 18/09, p. 40]; o cálculo exato dá cerca de 0,002. Em ambos os casos conclui-se que há evidência de associação.

V de Cramér [complemento: fórmula] = √(χ² / (n · min(linhas−1, colunas−1))) = √(9,52 / 200) ≈ **0,22** → associação estatisticamente significativa, mas de intensidade fraca a moderada.

**Variações possíveis**

- **Pergunta:** "p-value < 0,001 e V = 0,08. Interpreta."
    - **Resposta:** estatisticamente significativo, mas praticamente fraco.
    - **Justificação:** [Slides 18/09, p. 44]. O p-value diz se há evidência de associação; o V diz a sua intensidade [Slides 18/09, p. 42 e 43].
- **Pergunta:** "O teste do qui-quadrado diz-nos onde está a associação?"
    - **Resposta:** não; permite avaliar a existência de associação, mas não mostra, por si só, onde ela se encontra.
    - **Justificação:** [ACS_ACM, p. 6]. Para isso usa-se a ACS e o mapa de correspondências [ACS_ACM, p. 9].
- **Pergunta:** "Quantos graus de liberdade tem o teste numa tabela 3×3?"
    - **Resposta:** 4.
    - **Justificação:** df = (linhas − 1)(colunas − 1) [complemento: fórmula]. O exemplo canal × produto (3×3) tem df = 4 [ACS_ACM, p. 7].
- **Pergunta:** "Que medida usar para região e tipo de subscrição? E para canal de aquisição e abandono?"
    - **Resposta:** qui-quadrado + V de Cramér, nos dois casos.
    - **Justificação:** variáveis categóricas [Slides 18/09, p. 38].
- **Pergunta:** "Que condição se deve verificar para aplicar o qui-quadrado?"
    - **Resposta:** frequências esperadas não demasiado pequenas (regra habitual ≥ 5 por célula); com valores muito baixos pode usar-se o teste exato de Fisher.
    - **Justificação:** [complemento]; não está nos documentos da professora.

## Questão 8 — Pearson r = 0,78 (publicidade e vendas)

> **Enunciado.** O coeficiente de correlação de Pearson entre o investimento em publicidade e as vendas de uma empresa é r = 0,78.\
> **a)** Interprete o valor obtido.\
> **b)** É possível concluir que o investimento em publicidade causa o aumento das vendas? Justifique.

- **a) Resposta:** associação linear positiva e forte: valores mais altos de investimento em publicidade tendem a estar associados a vendas mais altas.
    - **Razão:** o r varia entre −1 e 1; o sinal dá a direção e o módulo a força [Slides 18/09, p. 8 a 10]. No exercício análogo (marketing e vendas, r = 0,85) a interpretação correta é "despesas de marketing mais altas tendem a estar associadas a vendas mais altas" [Slides 18/09, p. 11]. (Complemento: r² ≈ 0,61, ou seja, cerca de 61% da variação das vendas é partilhada linearmente com a publicidade.)
- **b) Resposta:** não, não se pode concluir causalidade.
    - **Razão:** a associação responde a "as variáveis movem-se juntas?" e a causalidade a "uma influencia a outra?" [Slides 18/09, p. 47 e 48]. Uma associação positiva pode surgir porque 1) a publicidade influencia as vendas; 2) as vendas influenciam a publicidade; 3) um terceiro fator influencia ambas [Slides 18/09, p. 50]. Exemplo clássico: vendas de gelados e afogamentos, com a temperatura como variável de confundimento [Slides 18/09, p. 51 a 53]. Mensagem-chave: uma associação forte não implica causalidade [Slides 18/09, p. 54].

**Variações possíveis**

- **Pergunta:** "r = 0,80 entre satisfação e retenção. Qual afirmação é adequada: A) aumentar a satisfação aumenta a retenção; B) a satisfação causa a retenção; C) satisfação e retenção estão associadas; D) as variáveis são independentes?"
    - **Resposta:** C.
    - **Justificação:** só se pode afirmar associação, não causalidade [Slides 18/09, p. 62 e 63].
- **Pergunta:** "r = −0,70 entre preço e procura. Interpreta."
    - **Resposta:** associação linear negativa forte: preços mais altos tendem a corresponder a menor procura; sem concluir causalidade.
    - **Justificação:** sinal negativo = direção negativa [Slides 18/09, p. 10].
- **Pergunta:** "r = 0,15. Podemos dizer que não há relação?"
    - **Resposta:** só que a associação linear é fraca; pode haver relação não linear.
    - **Justificação:** [Slides 18/09, p. 12 e 13].
- **Pergunta:** "r_pb = −0,65 entre satisfação e abandono (abandono = 1). O que significa o sinal negativo?"
    - **Resposta:** clientes com maior satisfação tendem a ter menor probabilidade de abandonar.
    - **Justificação:** [Slides 18/09, p. 35 e 36]. O sinal depende da codificação da variável binária [Slides 18/09, p. 33].
- **Pergunta:** "Os rankings de satisfação (1,2,3,4,5,6) e rentabilidade (2,1,4,3,5,6) de seis lojas. Que medida usar e qual a leitura?"
    - **Resposta:** Spearman (≈ 0,89, é o Pearson calculado sobre as ordens, cálculo meu); associação monótona positiva forte.
    - **Justificação:** rankings → Spearman; usa ordens em vez de valores e mede associação monótona [Slides 18/09, p. 17 a 21].

## Questão 9 — PCA com 4 variáveis padronizadas

> **Enunciado.** Uma empresa recolheu quatro variáveis quantitativas relativas ao desempenho dos seus trabalhadores e realizou uma Análise de Componentes Principais (PCA), após a padronização das variáveis.\
> **a)** A primeira componente principal apresenta cargas elevadas e positivas nas quatro variáveis originais. Explique o que poderá representar esta componente e indique uma limitação da sua interpretação.\
> **b)** Considere as seguintes afirmações e indique se cada uma é verdadeira (V) ou falsa (F). Não é necessário justificar.\
> **i)** As componentes principais são combinações lineares das variáveis originais.\
> **ii)** A primeira componente principal explica sempre toda a variância dos dados.\
> **iii)** A PCA pode ser utilizada para reduzir a dimensionalidade dos dados.

- **a) Resposta:** a PC1 representa uma dimensão **geral/global** de desempenho (um "índice geral"): trabalhadores com valores altos nas quatro variáveis têm score alto na PC1. **Limitação:** o nome é uma interpretação substantiva, não automática; a PC1 não explica toda a variância (perde-se informação nas restantes componentes); a PCA não estabelece causalidade.
    - **Razão:** loadings elevados nas mesmas variáveis indicam uma dimensão comum; no exemplo dos municípios, loadings altos em rendimento, escolaridade, emprego, esperança de vida e saúde levam à interpretação "desenvolvimento socioeconómico" [PCA, p. 16]. Os nomes são uma interpretação substantiva e devem ser fundamentados nos loadings mais elevados [PCA, p. 19]. A PCA não determina automaticamente a interpretação substantiva, não estabelece causalidade e scores próximos não implicam observações semelhantes em todas as variáveis [PCA, p. 21 e 22]. Um loading mede a relação entre variável e componente, com magnitude (intensidade) e sinal (direção) [PCA, p. 18].
- **b) i) V**
    - **Razão:** cada componente é uma combinação linear das variáveis originais [PCA, p. 3].
- **b) ii) F**
    - **Razão:** a 1.ª componente explica a maior quantidade possível de variância, não toda; no exemplo explica 45,3% [PCA, p. 3 e 10].
- **b) iii) V**
    - **Razão:** é a ideia central da PCA: reduzir a dimensionalidade preservando tanta informação quanto possível [PCA, p. 3].

**Exemplo trabalhado** (dados em [PCA, p. 10 a 14])

| Comp. | Valor próprio | % variância | % acumulada |
|---|---|---|---|
| 1 | 3,62 | 45,3 | 45,3 |
| 2 | 1,74 | 21,8 | 67,1 |
| 3 | 0,82 | 10,3 | 77,4 |
| 4 | 0,61 | 7,6 | 85,0 |
| … | … | … | … |

- Critério de Kaiser: reter componentes com λ > 1 → **2** componentes [PCA, p. 11].
- Scree plot: o "cotovelo" aparece após a 2.ª componente → 2 componentes [PCA, p. 12 e 13].
- Variância acumulada: 45,3 + 21,8 = 67,1% → 8 variáveis passam a 2 componentes preservando cerca de 67% da variância [PCA, p. 14].
- A decisão deve resultar da análise conjunta de valores próprios, Kaiser, scree plot, variância acumulada e interpretabilidade [PCA, p. 9].

**Variações possíveis**

- **Pergunta:** "Define loading e score."
    - **Resposta:** loading: relaciona variável ↔ componente (magnitude = intensidade; sinal = direção) e ajuda a interpretar a componente. Score: relaciona observação ↔ componente e indica a posição da observação nessa dimensão.
    - **Justificação:** [PCA, p. 18, 20 e 21].
- **Pergunta:** "Porque se padronizam as variáveis antes da PCA?"
    - **Resposta:** para as pôr numa escala comparável (Z = (X − X̄)/s), pois as variáveis estão em escalas diferentes.
    - **Justificação:** [PCA, p. 5].
- **Pergunta:** "Para que servem o KMO e o teste de Bartlett?"
    - **Resposta:** KMO: adequação dos dados (variância partilhada entre variáveis). Bartlett: testa H₀: R = I (matriz de correlações igual à identidade); se p < 0,05 rejeita-se H₀, as variáveis estão suficientemente correlacionadas. O Bartlett não indica quais variáveis estão associadas nem que todas as correlações sejam fortes.
    - **Justificação:** [PCA, p. 7]. Exemplo: KMO = 0,84, χ² = 842,6, gl = 28, p < 0,001 → dados adequados para prosseguir [PCA, p. 8].
- **Pergunta:** "Porque se analisa a matriz de correlações antes da PCA?"
    - **Resposta:** porque a PCA é particularmente útil quando existe estrutura de associação entre as variáveis.
    - **Justificação:** [PCA, p. 6].
- **Pergunta:** "A 2.ª componente tem loadings altos em transportes, internet e cultura. Que nome lhe darias?"
    - **Resposta:** por exemplo "conectividade e participação".
    - **Justificação:** [PCA, p. 17 e 19]; é uma interpretação substantiva.
- **Pergunta:** "V ou F: a PCA permite concluir que uma variável causa outra; dois municípios com scores próximos são semelhantes em todas as variáveis; a PCA cria novas dimensões sintéticas."
    - **Resposta:** F; F; V.
    - **Justificação:** [PCA, p. 21 e 22].
- **Pergunta:** "Valores próprios 2,4; 1,1; 0,3; 0,2 (p = 4, variáveis padronizadas). Quantas componentes pelo Kaiser e que % explica a 1.ª?"
    - **Resposta:** 2 componentes; a 1.ª explica 2,4/4 = 60%.
    - **Justificação:** Kaiser: λ > 1 [PCA, p. 11]; a percentagem é o valor próprio a dividir pelo total, e com variáveis padronizadas o total é p [complemento: soma = p], tal como no exemplo (3,62/8 = 45,3%) [PCA, p. 10].

## Questão 10 — Tipo de atleta e modalidade (qui-quadrado e ACS)

> **Enunciado.** Uma instituição pretende estudar a associação entre o tipo de atleta e a modalidade praticada, recorrendo a uma tabela de contingência e à Análise de Correspondências Simples (ACS).\
> **a)** Explique o objetivo do teste do qui-quadrado de Pearson quando aplicado a duas variáveis categóricas.\
> **b)** Considere as seguintes afirmações e indique se cada uma é verdadeira (V) ou falsa (F). Não é necessário justificar.\
> **i)** Um resultado estatisticamente significativo no teste do qui-quadrado implica que a associação entre as variáveis é forte.\
> **ii)** A ACS permite representar graficamente as categorias de duas variáveis categóricas.\
> **iii)** A proximidade entre categorias num mapa de correspondências permite concluir que existe uma relação de causalidade.\
> **c)** Explique por que razão a existência de uma associação estatisticamente significativa não permite, por si só, concluir que existe uma relação de causalidade entre as variáveis.

- **a) Resposta:** testar se existe associação estatisticamente significativa entre as duas variáveis categóricas (H₀: independentes; H₁: associadas), comparando as frequências observadas com as esperadas sob independência.
    - **Razão:** [ACS_ACM, p. 6 e 8]: quanto maiores as diferenças, no conjunto da tabela, entre observado e esperado, maior a evidência contra a independência. Se p < 0,05, rejeita-se H₀ [ACS_ACM, p. 7].
- **b) i) F**
    - **Razão:** significância estatística não implica intensidade; com p < 0,001 e V = 0,08 a associação é estatisticamente significativa mas praticamente fraca [Slides 18/09, p. 42 a 44].
- **b) ii) V**
    - **Razão:** a ACS representa as categorias num mapa de correspondências [ACS_ACM, p. 9 e 11].
- **b) iii) F**
    - **Razão:** a proximidade no mapa não deve ser interpretada automaticamente como medida direta de associação [ACS_ACM, p. 12], e a ACS não estabelece causalidade [ACS_ACM, p. 15].
- **c) Resposta:** o teste e a ACS só mostram que as variáveis variam em conjunto, não porquê nem em que sentido. Pode dever-se a um fator de confundimento, a causalidade inversa ou ao acaso; afirmar causalidade exige evidência adicional.
    - **Razão:** [Slides 18/09, p. 47 a 54 e 63]. A associação responde a "movem-se juntas?"; a causalidade a "uma influencia a outra?" [Slides 18/09, p. 47 e 48]. São necessárias mais evidências antes de afirmações causais [Slides 18/09, p. 54].

**Exemplo trabalhado** (tabela em [ACS_ACM, p. 5]; cálculo dos esperados meu)

| | Alimentação | Tecnologia | Moda | Total |
|---|---|---|---|---|
| Loja | 80 | 20 | 50 | 150 |
| Online | 30 | 90 | 60 | 180 |
| Misto | 40 | 50 | 30 | 120 |
| Total | 150 | 160 | 140 | 450 |

Esperado (Loja/Alimentação) = 150 × 150 / 450 = 50; observado = 80, muito acima do esperado. Esperado (Online/Tecnologia) = 180 × 160 / 450 = 64; observado = 90, acima do esperado. df = (3−1)(3−1) = 4. O documento apresenta χ² = 72,4 como valor "suponha" [ACS_ACM, p. 7]; aplicando a fórmula à tabela obtém-se cerca de 67,6. Os valores dos documentos são ilustrativos; o que interessa é interpretar (p < 0,05 → rejeitar a independência).

**Variações possíveis**

- **Pergunta:** "Define inércia na análise de correspondências."
    - **Resposta:** mede a variabilidade da tabela e está relacionada com a distância entre frequências observadas e esperadas sob independência; as dimensões ordenam-se pela inércia que explicam, como a PCA com a variância.
    - **Justificação:** [ACS_ACM, p. 10].
- **Pergunta:** "Define coordenadas, contribuição e qualidade de representação (cos²)."
    - **Resposta:** coordenada: posição da categoria na dimensão; contribuição: quanto a categoria contribui para construir a dimensão; cos²: quão bem a categoria é representada nas dimensões consideradas.
    - **Justificação:** [ACS_ACM, p. 13]. Uma coordenada de grande magnitude não significa necessariamente grande contribuição [ACS_ACM, p. 14].
- **Pergunta:** "Online tem coordenada 0,72, contribuição 31,5% e cos² 0,82; Loja tem −0,18, 2,8% e 0,35. Interpreta."
    - **Resposta:** Online está bem representada e contribui muito para a dimensão; Loja contribui pouco e está pior representada.
    - **Justificação:** [ACS_ACM, p. 14].
- **Pergunta:** "ACS ou ACM?"
    - **Resposta:** ACS: duas variáveis categóricas (tabela de contingência). ACM: várias variáveis categóricas analisadas simultaneamente.
    - **Justificação:** [ACS_ACM, p. 22]. Variáveis quantitativas não entram diretamente na ACM; só se categorizadas, com decisão justificada [ACS_ACM, p. 18].
- **Pergunta:** "Um mapa de ACM é uma segmentação de clientes?"
    - **Resposta:** não.
    - **Justificação:** ACS e ACM exploram associações e não são clustering [ACS_ACM, p. 23].
- **Pergunta:** "O que a ACS não permite?"
    - **Resposta:** não estabelece causalidade, não cria automaticamente grupos de indivíduos e não transforma a associação em previsão.
    - **Justificação:** [ACS_ACM, p. 15].
- **Pergunta:** "V ou F: o teste do qui-quadrado mostra onde está a associação; a ACS reduz a informação da tabela a poucas dimensões; categorias próximas no mapa estão sempre fortemente associadas."
    - **Resposta:** F; V; F.
    - **Justificação:** [ACS_ACM, p. 6, 9 e 12].
- **Pergunta:** "Como se interpretam as dimensões da ACM?"
    - **Resposta:** como contrastes entre conjuntos de categorias (por exemplo 50+ e Premium contra 35–49 e Standard), considerando as contribuições.
    - **Justificação:** [ACS_ACM, p. 19].

## Questão 11 — Silhouette e K-means

> **Enunciado.** Pretende-se agrupar clientes utilizando o rendimento anual, em euros, e a idade, em anos. Foram obtidos os seguintes valores médios do *silhouette score*:
>
> | Número de clusters | Silhouette score |
> |---|---|
> | K = 2 | 0,44 |
> | K = 3 | 0,61 |
> | K = 4 | 0,52 |
>
> **c)** Que número de clusters escolheria com base nestes resultados? Justifique a sua resposta.\
> **d)** Indique uma limitação do método K-means.
>
> *(No PDF só aparecem as alíneas c) e d).)*

- **c) Resposta:** K = 3.
    - **Razão:** tem o silhouette médio mais alto (0,61), o que indica, em geral, melhor coesão e separação dos grupos [Análise Classificatória, p. 13 e 14]. Como nos documentos, o k com a silhouette mais elevada é o escolhido no exemplo [Análise Classificatória, p. 13]; ainda assim a escolha de k não deve depender de um único indicador [Análise Classificatória, p. 15].
- **d) Resposta:** é preciso definir k à partida (o K-means não determina o número correto de grupos); o resultado depende da inicialização; e, como usa distâncias, é sensível à escala das variáveis e a valores extremos. Aqui, rendimento (€) e idade (anos) têm escalas muito diferentes, por isso há que padronizar.
    - **Razão:** [Análise Classificatória, p. 11 e 12] (k definido antes e dependência da inicialização); [Análise Classificatória, p. 5] (escala e padronização); [Análise Classificatória, p. 21] (os métodos baseados em distâncias podem ser sensíveis a valores extremos). Outras limitações habituais, como assumir clusters esféricos e só funcionar com variáveis quantitativas, são conhecimento geral [complemento].

**Como se calcula a silhouette:** s(i) = (b(i) − a(i)) / max{a(i), b(i)}, onde a(i) é a distância média da observação ao seu próprio grupo e b(i) a distância média ao grupo alternativo mais próximo [Análise Classificatória, p. 14]. Exemplo (meu): a = 2 e b = 5 → s = 3/5 = 0,6 (bem integrada); a = 5 e b = 2 → s = −0,6 (provavelmente mal classificada); a = b → s = 0 (fronteira).

**Como funciona o K-means:** 1) escolher k; 2) definir centros iniciais; 3) atribuir cada observação ao centro mais próximo; 4) recalcular os centros; 5) repetir até estabilizar [Análise Classificatória, p. 12].

**Variações possíveis**

- **Pergunta:** "Silhouette: k = 2 → 0,28; k = 3 → 0,55; k = 4 → 0,50. Que k escolhes e o que mais verificarias?"
    - **Resposta:** k = 3; verificar também o dendrograma, a estabilidade, o tamanho dos grupos, a interpretabilidade e o contexto.
    - **Justificação:** [Análise Classificatória, p. 13 a 15].
- **Pergunta:** "Silhouette: k = 2 → 0,30; k = 3 → 0,28; k = 4 → 0,29. O que concluir?"
    - **Resposta:** valores baixos e muito próximos: não há evidência forte de uma estrutura de grupos; a decisão deve apoiar-se noutros critérios.
    - **Justificação:** a escolha de k não depende só de um indicador e deve considerar interpretabilidade e estabilidade [Análise Classificatória, p. 15]; o clustering não garante uma segmentação natural [Análise Classificatória, p. 22].
- **Pergunta:** "Como caracterizar os grupos obtidos?"
    - **Resposta:** comparar as variáveis entre grupos, ver o tamanho dos grupos e a variabilidade dentro de cada um; não caracterizar só pela média.
    - **Justificação:** [Análise Classificatória, p. 17].
- **Pergunta:** "Os clusters diferem no abandono (variável não usada no clustering). Isso prova que o clustering está correto?"
    - **Resposta:** não, nem estabelece causalidade.
    - **Justificação:** [Análise Classificatória, p. 18].
- **Pergunta:** "Hierárquico (silhouette 0,39) e K-means (0,42) dão grupos de tamanhos semelhantes. O que concluir?"
    - **Resposta:** a semelhança é evidência complementar, mas não significa automaticamente que a solução seja robusta.
    - **Justificação:** [Análise Classificatória, p. 20].
- **Pergunta:** "Porque padronizar antes do clustering? Resolve os outliers?"
    - **Resposta:** para a distância não ser dominada pela variável de maior escala; não resolve os outliers.
    - **Justificação:** [Análise Classificatória, p. 5 e 21].
- **Pergunta:** "O clustering descobre uma 'verdade' única sobre os dados?"
    - **Resposta:** não; um cluster é uma estrutura definida pelas variáveis, medida de distância e método utilizados.
    - **Justificação:** [Análise Classificatória, p. 22].

## Questão 12 — Matriz de confusão

> **Enunciado.** Um hospital desenvolveu um modelo de classificação para identificar pacientes com uma determinada doença. Considerando a classe positiva como "Com doença", obteve-se a seguinte matriz de confusão:
>
> | | Previsto: Com doença | Previsto: Sem doença |
> |---|---|---|
> | **Real: Com doença** | 30 | 20 |
> | **Real: Sem doença** | 10 | 40 |
>
> **a)** Identifique os valores de verdadeiros positivos (TP), falsos negativos (FN), falsos positivos (FP) e verdadeiros negativos (TN).\
> **b)** Calcule a accuracy.\
> **c)** Calcule o recall (sensibilidade) para a classe "Com doença".\
> **d)** Calcule a precision para a classe "Com doença".

- **a) Resposta:** TP = 30; FN = 20; FP = 10; TN = 40.
    - **Razão:** TP: prevê positivo e é positivo (doente previsto doente); FN: prevê negativo mas é positivo (doente previsto sem doença); FP: prevê positivo mas é negativo (sem doença previsto doente); TN: prevê negativo e é negativo [Análise Discriminante, p. 13]. As linhas são a realidade e as colunas a previsão [Análise Discriminante, p. 11].
- **b) Resposta:** accuracy = (30 + 40) / 100 = **0,70 (70%)**.
    - **Razão:** accuracy = classificações corretas / total de observações [Análise Discriminante, p. 12].
- **c) Resposta:** recall = TP / (TP + FN) = 30 / 50 = **0,60 (60%)**.
    - **Razão:** proporção das observações do grupo que foram corretamente identificadas [Análise Discriminante, p. 14].
- **d) Resposta:** precision = TP / (TP + FP) = 30 / 40 = **0,75 (75%)**.
    - **Razão:** proporção das observações classificadas nesse grupo que lá pertencem efetivamente [Análise Discriminante, p. 14].

**Variações possíveis**

- **Pergunta:** "Calcula o F1-score da classe 'Com doença'."
    - **Resposta:** F1 = 2 · (0,75 · 0,60) / (0,75 + 0,60) ≈ **0,667**.
    - **Justificação:** F1 = 2 · (Precision · Recall) / (Precision + Recall) [Análise Discriminante, p. 15].
- **Pergunta:** "Calcula a balanced accuracy."
    - **Resposta:** recall "Com doença" = 0,60; recall "Sem doença" = 40/50 = 0,80; balanced accuracy = (0,60 + 0,80)/2 = **0,70**. Coincide com a accuracy porque os dois grupos têm o mesmo tamanho (50 e 50).
    - **Justificação:** é a média dos recalls dos grupos [Análise Discriminante, p. 18].
- **Pergunta:** "Troca a classe positiva para 'Sem doença'. Recalcula recall e precision."
    - **Resposta:** TP = 40, FN = 10, FP = 20, TN = 30; recall = 40/50 = 0,80; precision = 40/60 ≈ 0,667. A accuracy não muda (0,70).
    - **Justificação:** recall e precision são calculados "para um determinado grupo" [Análise Discriminante, p. 14]; mudar a classe positiva muda TP, FN e FP.
- **Pergunta:** "Que tipo de erro são os FP e os FN?"
    - **Resposta:** FP: erro do Tipo I ou falso alarme; FN: erro do Tipo II ou omissão. Em contexto médico os FN (doentes não detetados) são normalmente os mais graves, por isso olha-se para o recall.
    - **Justificação:** [Análise Discriminante, p. 13]; a leitura clínica é interpretação [complemento].
- **Pergunta:** "Uma accuracy elevada significa um bom modelo?"
    - **Resposta:** não necessariamente: com grupos de tamanhos muito diferentes pode esconder um desempenho muito fraco num dos grupos. Exemplo: accuracy 84,3% mas recall do Grupo 1 de 2% e balanced accuracy 50,4%.
    - **Justificação:** [Análise Discriminante, p. 12 e 23].
- **Pergunta:** "Exemplo para treinar: real Não 210/26; real Sim 18/26 (positiva = Sim). Calcula as métricas."
    - **Resposta:** TP = 26, FN = 18, FP = 26, TN = 210; accuracy = 236/280 = 0,843; recall = 26/44 = 0,591; precision = 26/52 = 0,50; F1 ≈ 0,542.
    - **Justificação:** [Análise Discriminante, p. 11, 12, 16 e 17].
- **Pergunta:** "Porque se valida o modelo fora da amostra de estimação?"
    - **Resposta:** avaliar só na amostra usada para estimar o modelo é demasiado otimista; usa-se validação cruzada ou amostra de teste para avaliar a capacidade de generalização.
    - **Justificação:** [Análise Discriminante, p. 19].
- **Pergunta:** "Que pressupostos tem a Análise Discriminante Linear e para que serve o teste de Box?"
    - **Resposta:** variáveis quantitativas adequadas; sem multicolinearidade grave; normalidade multivariada dentro dos grupos; matrizes de covariância aproximadamente iguais; sem observações excessivamente influentes. O teste de Box testa H₀: Σ₁ = … = Σ_K; p < 0,05 → evidência contra a igualdade; p ≥ 0,05 → não se rejeita H₀ (o que não "prova" a igualdade).
    - **Justificação:** [Análise Discriminante, p. 20 e 21].

# 3. Outros pontos do programa que podem aparecer

## 3.1 Análise preliminar

- **Pergunta:** "O que é a matriz de dados?"
    - **Resposta:** linhas = unidades estatísticas; colunas = variáveis.
    - **Justificação:** [Análise Preliminar, p. 4].
- **Pergunta:** "Distingue população, amostra e unidade estatística."
    - **Resposta:** população: conjunto de unidades sobre as quais se pretende informação; amostra: subconjunto efetivamente observado; unidade estatística: elemento individual sobre o qual se recolhem dados (exemplo: todos os clientes; os clientes do conjunto de dados; cada cliente).
    - **Justificação:** [Análise Preliminar, p. 5].
- **Pergunta:** "Como se descreve uma variável qualitativa?"
    - **Resposta:** frequência absoluta e relativa; gráfico de barras (mais fácil de comparar) ou circular (poucas categorias).
    - **Justificação:** [Análise Preliminar, p. 13 e 14].
- **Pergunta:** "Dados 2, 3, 3, 4, 5, 3, 6. Calcula moda, mediana e média."
    - **Resposta:** moda = 3; mediana = 3 (ordenados: 2, 3, 3, 3, 4, 5, 6); média = 26/7 ≈ 3,71.
    - **Justificação:** moda = valor mais frequente [Análise Preliminar, p. 17] (o exemplo dos documentos dá moda = 3); mediana = valor central dos dados ordenados e média = soma/n [Análise Preliminar, p. 15]. A média e a mediana são cálculos meus.
- **Pergunta:** "Quais são as medidas de dispersão?"
    - **Resposta:** amplitude (máx − mín), variância, desvio-padrão e amplitude interquartil (AIQ = Q3 − Q1).
    - **Justificação:** [Análise Preliminar, p. 18 e 19].
- **Pergunta:** "Num boxplot Q1 = 1400, mediana = 1600, Q3 = 1800. Calcula a AIQ e interpreta."
    - **Resposta:** AIQ = 400; 25% dos rendimentos são inferiores a 1400, 50% a 1600 e 75% a 1800.
    - **Justificação:** [Análise Preliminar, p. 19 e 21].
- **Pergunta:** "O que é um histograma e como se lê?"
    - **Resposta:** representa a distribuição de uma variável quantitativa; os valores agrupam-se em classes (intervalos consecutivos), a altura da barra é a frequência e as barras são contíguas. Lê-se concentração, dispersão, assimetria e valores muito afastados.
    - **Justificação:** [Análise Preliminar, p. 22 a 24].
- **Pergunta:** "Que problemas de qualidade dos dados se devem verificar?"
    - **Resposta:** valores omissos (quantos, em que variáveis, ocorrem aleatoriamente?), valores impossíveis, categorias escritas de formas diferentes, unidades inconsistentes, duplicados e valores fora dos limites esperados.
    - **Justificação:** [Análise Preliminar, p. 27 e 28].

## 3.2 Bivariada

- **Pergunta:** "Uma correlação forte e significativa basta para concluir?"
    - **Resposta:** não; significância estatística não implica relevância prática nem causalidade, e a interpretação é mais importante do que o cálculo.
    - **Justificação:** [Slides 18/09, p. 63].
- **Pergunta:** "Como se calcula a correlação ponto-bisserial e de que depende o sinal?"
    - **Resposta:** codifica-se a binária numericamente (por exemplo Churn = Sim → 1, Não → 0) e calcula-se o Pearson entre a quantitativa e a binária codificada; o sinal depende da codificação.
    - **Justificação:** [Slides 18/09, p. 31, 32 e 33].

## 3.3 ACM

- **Pergunta:** "Que variáveis podem entrar numa ACM?"
    - **Resposta:** categóricas; as quantitativas só se forem categorizadas, com decisão justificada.
    - **Justificação:** [ACS_ACM, p. 18].
- **Pergunta:** "Como se avalia a inércia na ACM?"
    - **Resposta:** pela inércia corrigida por dimensão e acumulada (exemplo: 57,3%, 15,6%, 13,8% e 8,3%; acumulada 72,9% nas duas primeiras).
    - **Justificação:** [ACS_ACM, p. 20].

# 4. Banco de treino — variações para resolveres sozinho

*(Cada pergunta traz por baixo a resposta e a justificação.)*

## Escolha múltipla

- **Pergunta 1.** Num boxplot, um ponto isolado acima do bigode superior indica: (a) a mediana; (b) um possível valor extremo; (c) a moda; (d) um valor omisso.
    - **Resposta:** (b).
    - **Justificação:** o boxplot mostra possíveis valores extremos [Análise Preliminar, p. 20 e 21].
- **Pergunta 2.** O Spearman é adequado quando: (a) ambas as variáveis são nominais; (b) as variáveis são ordinais ou há outliers extremos; (c) uma variável é binária e a outra qualitativa; (d) se quer testar a causalidade.
    - **Resposta:** (b).
    - **Justificação:** ordinal × ordinal → Spearman; com outliers extremos pode ser mais robusto [Slides 18/09, p. 20, 23 e 24].
- **Pergunta 3.** Num dendrograma, um corte horizontal serve para: (a) eliminar outliers; (b) definir o número de clusters; (c) calcular o silhouette; (d) padronizar as variáveis.
    - **Resposta:** (b).
    - **Justificação:** [Análise Classificatória, p. 8].
- **Pergunta 4.** O critério de Kaiser recomenda reter as componentes com: (a) λ > 1; (b) λ < 1; (c) variância acumulada > 50%; (d) loadings > 0,5.
    - **Resposta:** (a).
    - **Justificação:** [PCA, p. 11].
- **Pergunta 5.** Na ACM podem entrar diretamente: (a) idade e rendimento; (b) região, sexo e canal de compra; (c) apenas uma variável; (d) apenas variáveis binárias.
    - **Resposta:** (b).
    - **Justificação:** a ACM analisa várias variáveis categóricas; quantitativas só categorizadas [ACS_ACM, p. 16 a 18].
- **Pergunta 6.** Uma accuracy de 90% garante que: (a) o modelo identifica bem todos os grupos; (b) não há erros do tipo II; (c) nada, se os grupos forem muito desequilibrados; (d) o recall é 90%.
    - **Resposta:** (c).
    - **Justificação:** [Análise Discriminante, p. 12].

## Resposta curta e cálculo

- **Pergunta 7.** Classifica: número de reclamações; nível de escolaridade (básico/secundário/superior); temperatura em °C; tipo de contrato.
    - **Resposta:** quantitativa discreta; qualitativa ordinal; quantitativa contínua; qualitativa nominal.
    - **Justificação:** [Análise Preliminar, p. 8 e 10]. Escolaridade (básico, secundário, superior) é exemplo de ordinal [Análise Preliminar, p. 8]; a temperatura é uma medição, logo contínua.
- **Pergunta 8.** Que medida de associação usarias para: (i) idade × rendimento; (ii) ranking de fornecedores × ranking de preço; (iii) satisfação (0–10) × abandono (Sim/Não); (iv) região × tipo de produto?
    - **Resposta:** (i) Pearson; (ii) Spearman; (iii) ponto-bisserial; (iv) qui-quadrado + V de Cramér.
    - **Justificação:** [Slides 18/09, p. 45].
- **Pergunta 9.** r = −0,70 entre preço e procura. Interpreta e discute causalidade.
    - **Resposta:** associação linear negativa forte: preços mais altos tendem a corresponder a menor procura; não implica causalidade (confundimento, causalidade inversa).
    - **Justificação:** [Slides 18/09, p. 10, 50 e 54].
- **Pergunta 10.** Dados: 4, 6, 6, 7, 9, 40. Calcula média e mediana e indica qual representa melhor o valor típico.
    - **Resposta:** média = 72/6 = 12; mediana = (6 + 7)/2 = 6,5. A mediana representa melhor o valor típico.
    - **Justificação:** o 40 é um valor extremo e a média é sensível a extremos [Análise Preliminar, p. 16].
- **Pergunta 11.** Tabela 2×2: linha 1 = 30 e 30 (total 60), linha 2 = 10 e 30 (total 40), n = 100. Calcula as frequências esperadas.
    - **Resposta:** totais das colunas = 40 e 60. Linha 1: 60·40/100 = 24 e 60·60/100 = 36. Linha 2: 40·40/100 = 16 e 40·60/100 = 24.
    - **Justificação:** frequência esperada = situação sob independência [ACS_ACM, p. 8]; a fórmula (total linha × total coluna / n) é conhecimento geral [complemento].
- **Pergunta 12.** Valores próprios (p = 5, variáveis padronizadas): 2,5; 1,2; 0,6; 0,4; 0,3. Quantas componentes pelo Kaiser? Qual a % de variância acumulada com 2 componentes?
    - **Resposta:** 2 componentes (2,5 e 1,2); variância acumulada = (2,5 + 1,2)/5 = 74%.
    - **Justificação:** Kaiser λ > 1 [PCA, p. 11]; percentagem = valor próprio / total [PCA, p. 10 e 14], com total = p [complemento].
- **Pergunta 13.** Silhouette: k = 2 → 0,28; k = 3 → 0,55; k = 4 → 0,50. Que k escolhes e o que mais verificarias?
    - **Resposta:** k = 3; verificar também dendrograma, estabilidade, tamanho dos grupos, interpretabilidade e padronização/outliers.
    - **Justificação:** [Análise Classificatória, p. 13 a 15].
- **Pergunta 14.** Matriz de confusão (positiva = Fraude): real Fraude: 15 previstos Fraude e 5 previstos Não; real Não fraude: 10 previstos Fraude e 170 previstos Não. Calcula accuracy, recall, precision, F1 e balanced accuracy. Comenta.
    - **Resposta:** TP = 15, FN = 5, FP = 10, TN = 170, total = 200. Accuracy = 185/200 = 0,925. Recall = 15/20 = 0,75. Precision = 15/25 = 0,60. F1 = 2·0,60·0,75/1,35 ≈ 0,667. Recall do grupo "Não fraude" = 170/180 ≈ 0,944; balanced accuracy = (0,75 + 0,944)/2 ≈ 0,847. A accuracy (92,5%) é inflacionada pelo grupo maioritário; identificam-se 75% das fraudes e 40% dos alertas são falsos alarmes.
    - **Justificação:** [Análise Discriminante, p. 12 a 15 e 18]; o comentário sobre grupos desequilibrados segue [Análise Discriminante, p. 12 e 23].
- **Pergunta 15.** V/F: (i) a ACM é um método de clustering; (ii) a Análise Discriminante é supervisionada; (iii) o K-means determina automaticamente o número de grupos; (iv) padronizar as variáveis elimina o efeito dos outliers; (v) a PCA exige variáveis qualitativas.
    - **Resposta:** (i) F; (ii) V; (iii) F; (iv) F; (v) F.
    - **Justificação:** (i) [ACS_ACM, p. 23]; (ii) [Overview, p. 12]; (iii) [Análise Classificatória, p. 12]; (iv) [Análise Classificatória, p. 5 e 21]; (v) a PCA usa variáveis quantitativas [PCA, p. 5].
- **Pergunta 16.** p = 4 variáveis e K = 5 grupos. Quantas funções discriminantes no máximo?
    - **Resposta:** 4.
    - **Justificação:** min(p, K − 1) = min(4, 4) = 4 [Análise Discriminante, p. 10].

# 5. Frases-chave para memorizar

- "Não começamos pelo método. Começamos pela pergunta." [Overview, p. 15]
- Os dados, por si só, não são informação; uma análise termina quando conseguimos interpretar o que o resultado significa [Apresentação da UC, p. 2 e 4].
- **Correlação não implica causalidade**; associação ≠ causalidade [Slides 18/09, p. 54 e 63].
- **Significância estatística ≠ relevância prática** (p < 0,001 com V = 0,08 → fraca) [Slides 18/09, p. 44 e 63].
- **Padronizar** resolve a escala, **não** os outliers [Análise Classificatória, p. 5 e 21].
- Um valor extremo **não se elimina automaticamente**: percebe-se a origem [Análise Preliminar, p. 29].
- **PCA:** reduzir dimensão preservando variância; as componentes são combinações lineares; os nomes são interpretação [PCA, p. 3 e 19].
- **ACS/ACM:** exploram associações entre categorias; **não** são clustering; proximidade no mapa não se interpreta isoladamente [ACS_ACM, p. 12 e 23].
- **Clustering:** grupos desconhecidos; k tem de ser justificado (silhouette + interpretabilidade + estabilidade) [Análise Classificatória, p. 15].
- **Discriminante:** grupos conhecidos; avaliar **por grupo**, não só a accuracy; validar fora da amostra [Análise Discriminante, p. 12, 19 e 28].
- Um bom resultado na amostra de estimação não garante bom desempenho em novos casos [Análise Discriminante, p. 19].
