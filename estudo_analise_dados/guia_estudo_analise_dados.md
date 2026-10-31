---
title: "Análise de Dados — Guia de estudo para o exame de 2 de novembro"
subtitle: "Teste-modelo e Modelo de Exame 2 resolvidos e explicados, exercícios resolvidos, exemplos e variações possíveis"
lang: pt-PT
---

# 0. Como usar este guia

**Formato do exame (email da professora):** 60 minutos, cotado para 20 valores, uma folha A4 manuscrita (frente e verso). Pode ter escolha múltipla, resposta aberta, cálculos, interpretação de resultados e justificação. Avalia-se **escolher e aplicar o método certo** e **interpretar criticamente**. Depois do exame há uma discussão oral individual do trabalho (5 a 10 minutos).

**Como o guia está organizado**

| Parte | Conteúdo |
|---|---|
| 1 e 2 | **Teste-modelo** (12 questões): enunciado, resposta, razão e variações. Confirmado pela solução oficial. |
| 3 | **Modelo de Exame 2** (12 questões, 90 min sugeridos): enunciado, resposta, razão e variações. |
| 4 | **Exercícios resolvidos** das aulas: associação, Wooclap, PCA, ACS/ACM e Análise Classificatória. |
| 5 | **Outros pontos do programa** (análise preliminar, dispersão, distâncias e ligações, ACM). |
| 6 | **Banco de treino** com respostas. |
| 7 | **Erros mais comuns** e **frases-chave**. |

**Formato de cada questão**

1. O **enunciado** aparece em citação no início.
2. A **resposta** e, indentada por baixo, a **razão** (com o documento e a página onde a matéria está).
3. As **variações possíveis**: cada pergunta tem por baixo, indentadas, a **resposta** e a **justificação**.

**Como estão indicadas as fontes**

- Entre parênteses retos aparece o **nome do documento e a página** (ou o número do exercício), por exemplo [Análise Preliminar, p. 29]. As páginas são as do PDF; nos PDFs com rodapé "n / N" coincidem com o número do slide.
- **[complemento]** = conhecimento geral útil que **não** está nos documentos da professora. Na prova, usa de preferência o vocabulário dos documentos.
- Os cálculos marcados "meu cálculo" são meus, não vêm dos documentos.

| Nome usado no guia | Ficheiro |
|---|---|
| Apresentação da UC | Apresentação da UC |
| Análise Preliminar | 1_Analise_Preliminar_de_Dados |
| Slides 18/09 | Slides_Aula_20260918 (medidas de associação, em inglês) |
| PCA | PCA |
| ACS_ACM | ACS_ACM |
| Análise Classificatória | Análise_Classificatória |
| Clustering | Clustering (Cluster Analysis, em inglês, 26 pp.) |
| Análise Discriminante | Análise_Discriminante |
| Overview | overview |
| Teste-modelo / Modelo_solucao | Modelo / Modelo_solucao |
| Modelo de Exame 2 / Resolução | Modelo_Exame_2_Analise_de_Dados / Modelo_Exame_2_Resolucao |
| Ficha de exercícios | Exercícios (medidas de associação, com soluções) |
| Exercícios PCA / ACS_ACM / Classificatória | PCA_exercicios / ACS_ACM_exercicios / Analise_Classificatoria_exercicios (e respetivas soluções) |
| Wooclap | Wooclap_pdf (quiz de Análise Preliminar) |
| Artigo de dispersão | artigo_medidas_de_dispersao (Bastos e Duquia, 2007; páginas da revista: 40 a 44) |

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


# 1. Parte I — Teste-modelo: Grupo I (escolha múltipla)

> **O que a solução oficial do teste-modelo (Modelo_solucao) confirma e acrescenta**
>
> - Grupo I: **1 = B, 2 = A, 3 = B, 4 = C, 5 = D** (igual às respostas abaixo).
> - Q7: o qui-quadrado de Pearson aplica-se "desde que os pressupostos relativos às frequências esperadas sejam satisfeitos"; H₀ = independência, H₁ = associação.
> - Q8b: as vendas podem ser influenciadas por outros fatores, como preço, sazonalidade, concorrência ou condições de mercado.
> - Q9a: a C1 "poderá representar uma dimensão global de desempenho"; a limitação é que a interpretação depende do significado das variáveis e das cargas, e a componente não demonstra um fator causal comum.
> - Q10c: identificar causalidade exige um desenho de investigação e pressupostos adicionais.
> - Q11d: o K-means exige definir previamente o número de clusters, é sensível à inicialização dos centroides e a valores extremos, e pode dar resultados menos adequados quando os grupos têm formas ou densidades muito diferentes.
> - Q12: TP = 30, FN = 20, FP = 10, TN = 40; accuracy 70%, recall 60%, precision 75%.



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

# 2. Parte I — Teste-modelo: Grupo II (respostas abertas)

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
    - **Justificação:** a solução oficial exige que os pressupostos relativos às frequências esperadas sejam satisfeitos [Modelo_solucao, Q7]. A regra habitual (≥ 5 por célula) e o teste exato de Fisher são [complemento].

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
    - **Razão:** [Análise Classificatória, p. 11 e 12] (k definido antes e dependência da inicialização); [Análise Classificatória, p. 5] (escala e padronização); [Análise Classificatória, p. 21] (os métodos baseados em distâncias podem ser sensíveis a valores extremos). Os slides de Clustering acrescentam: só dados numéricos (variáveis padronizadas), assume clusters de tamanho e variância semelhantes e funciona bem com clusters esféricos [Clustering, p. 18 e 20]. Solução oficial: [Modelo_solucao, Q11].

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


# 3. Parte II — Modelo de Exame 2

*(Duração sugerida: 90 minutos; 20 valores. Parte A: 6 valores; Parte B: 14 valores. O exame real tem 60 minutos, por isso usa este modelo como treino com margem. Instrução do enunciado: apresentar os cálculos, justificar as escolhas metodológicas e interpretar no contexto; associação não deve ser apresentada como causalidade [Modelo de Exame 2, p. 1].)*

## Parte A — Conceitos e escolha de métodos

### M2-1 — Ordinal vs discreta (1,0 valor)

> **Enunciado.** Distinga uma variável qualitativa ordinal de uma variável quantitativa discreta e apresente um exemplo de cada.

- **Resposta:** **ordinal** = categorias com ordem natural (exemplo: satisfação baixa/média/alta). **Quantitativa discreta** = contagem com valores inteiros (exemplo: número de compras).
    - **Razão:** ordinais têm ordem natural; discretas resultam de contagens e assumem valores isolados [Análise Preliminar, p. 8 e 10]. Os números não definem o tipo: "grau de satisfação 1 a 5" é ordinal, "número de compras" é discreta [Análise Preliminar, p. 9]. Solução oficial: [Modelo de Exame 2, Resolução, Q1].

**Variações possíveis**

- **Pergunta:** "Distinga variável quantitativa contínua de discreta e dê exemplos."
    - **Resposta:** contínua resulta de uma medição e pode tomar qualquer valor num intervalo (rendimento, idade, tempo); discreta resulta de contagem (número de reclamações).
    - **Justificação:** [Análise Preliminar, p. 10].
- **Pergunta:** "Distinga nominal de ordinal e explique porque a distinção é relevante."
    - **Resposta:** nominal não tem ordem (sexo, região); ordinal tem ordem natural. É relevante porque a ordem permite usar medidas diferentes (por exemplo Spearman para duas ordinais).
    - **Justificação:** [Análise Preliminar, p. 8]; [Exercícios ACS_ACM, Ex. 1.3]; [Slides 18/09, p. 45].

### M2-2 — Mediana vs média (1,0 valor)

> **Enunciado.** Explique por que motivo a mediana pode ser preferível à média quando existem valores extremos.

- **Resposta:** a média é influenciada por valores extremos; a mediana depende da posição ordenada, é mais robusta e representa melhor o centro quando a distribuição é assimétrica ou contém outliers.
    - **Razão:** [Análise Preliminar, p. 16] (rendimentos 1200, 1300, 1400, 1500, 10000: média 3080 e mediana 1400). Solução oficial: [Modelo de Exame 2, Resolução, Q2].

**Variações possíveis**

- **Pergunta:** "Tempos de espera 4, 5, 6, 7, 8 e 40. Qual afirmação é correta: a média é pouco afetada pelo 40; a mediana é mais sensível que a média; a média é mais influenciada que a mediana; o 40 deve ser eliminado?"
    - **Resposta:** "a média é mais influenciada pelo valor 40 do que a mediana" (média ≈ 11,7; mediana = 6,5, cálculo meu).
    - **Justificação:** [Wooclap, pergunta 7]; [Análise Preliminar, p. 16 e 29].

### M2-3 — Medida de associação (1,0 valor)

> **Enunciado.** Para estudar a relação entre satisfação numa escala de 1 a 5 e intenção de recompra numa escala de 1 a 5, indique uma medida de associação adequada e justifique.

- **Resposta:** **Spearman**.
    - **Razão:** as duas variáveis são ordinais; o Spearman usa ordens (ranks), mede associação monótona e é adequado a variáveis ordinais [Slides 18/09, p. 20 e 45]. Solução oficial: [Modelo de Exame 2, Resolução, Q3].

**Variações possíveis**

- **Pergunta:** "Que medida usar para satisfação (0–10) e churn (Sim/Não)? E para género e churn?"
    - **Resposta:** ponto-bisserial; qui-quadrado + V de Cramér.
    - **Justificação:** [Slides 18/09, p. 30, 45 e 57 a 61].

### M2-4 — PCA (1,0 valor)

> **Enunciado.** Indique o principal objetivo da PCA e explique a diferença entre loading e score.

- **Resposta:** reduzir a dimensionalidade, resumindo variáveis correlacionadas em componentes que preservam variância. **Loading:** relação entre uma variável e uma componente. **Score:** posição de uma observação nessa componente.
    - **Razão:** [PCA, p. 3, 18, 20 e 21]. Solução oficial: [Modelo de Exame 2, Resolução, Q4].

**Variações possíveis**

- **Pergunta:** "Dois municípios têm scores próximos na C1. São semelhantes em todas as variáveis?"
    - **Resposta:** não; a proximidade numa dimensão não garante proximidade no espaço multivariado completo.
    - **Justificação:** [PCA, p. 21]; [Exercícios PCA, Ex. 11c].

### M2-5 — Classificatória vs discriminante (1,0 valor)

> **Enunciado.** Diferencie análise classificatória de análise discriminante quanto ao conhecimento prévio dos grupos.

- **Resposta:** na classificatória (clustering, não supervisionada) os grupos **não** são conhecidos e procuram-se; na discriminante (supervisionada) os grupos **são** conhecidos e pretende-se separar e classificar observações.
    - **Razão:** [Análise Discriminante, p. 3 e 25]; [Overview, p. 12]. Solução oficial: [Modelo de Exame 2, Resolução, Q5].

### M2-6 — Silhouette (1,0 valor)

> **Enunciado.** Explique o significado de um valor de silhouette próximo de 1 e de um valor negativo.

- **Resposta:** **próximo de 1:** observação bem integrada no seu cluster e afastada dos restantes. **Negativo:** pode estar mal atribuída, mais próxima de outro cluster.
    - **Razão:** s(i) = (b(i) − a(i))/max{a(i), b(i)}, com a(i) distância média ao próprio grupo e b(i) distância média ao grupo alternativo mais próximo [Análise Classificatória, p. 14]. Leitura: s ≈ 1 bem agrupada, s ≈ 0 clusters sobrepostos, s ≈ −1 mal classificada [Clustering, p. 25]. Solução oficial: [Modelo de Exame 2, Resolução, Q6].

## Parte B — Aplicação e interpretação

### M2-7 — Variáveis categóricas (2,0 valores)

> **Enunciado.** Uma empresa pretende avaliar se o canal de compra está associado ao nível de satisfação. Obteve a tabela seguinte:
>
> | Canal | Baixa | Média | Alta | Total |
> |---|---|---|---|---|
> | Loja física | 18 | 32 | 50 | 100 |
> | Online | 30 | 40 | 30 | 100 |
> | Total | 48 | 72 | 80 | 200 |
>
> **a)** Formule H₀ e H₁ e indique o teste adequado.\
> **b)** Se p = 0,002 e V de Cramér = 0,21, interprete os resultados.

- **a) Resposta:** H₀: canal e satisfação são independentes; H₁: existe associação. Teste: **qui-quadrado de independência** sobre a tabela de contingência.
    - **Razão:** duas variáveis categóricas → qui-quadrado + V de Cramér [Slides 18/09, p. 45]; H₀ independência e H₁ associação [Slides 18/09, p. 40; ACS_ACM, p. 6]. A satisfação é ordinal, mas na tabela de contingência as suas categorias são analisadas como categorias [complemento].
- **b) Resposta:** como p = 0,002 < 0,05, rejeita-se H₀: há evidência de associação entre canal e satisfação. V = 0,21 indica intensidade **fraca a moderada**; a relevância prática deve ser avaliada no contexto. Não se conclui causalidade.
    - **Razão:** o qui-quadrado diz *se* há associação; o V diz *quão forte* (0 ≤ V ≤ 1) [Slides 18/09, p. 40 a 44; Ficha de exercícios, Ex. 10]. Solução oficial: [Modelo de Exame 2, Resolução, Q7].

**Verificação com os dados do enunciado (meu cálculo):** frequências esperadas = 24, 36 e 40 em cada linha; χ² = 2 × (6²/24 + 4²/36 + 10²/40) ≈ 8,89 com gl = (2−1)(3−1) = 2; V = √(8,89/200) ≈ 0,21, o que coincide com o V dado.

**Variações possíveis**

- **Pergunta:** "Se p = 0,40 e V = 0,05, o que concluir?"
    - **Resposta:** não se rejeita H₀: não há evidência de associação; V muito baixo.
    - **Justificação:** p ≥ 0,05 não rejeita H₀ [ACS_ACM, p. 7]; V próximo de 0 → associação fraca [Slides 18/09, p. 43].
- **Pergunta:** "Qual é a frequência esperada de Loja física/Alta?"
    - **Resposta:** 100 × 80/200 = 40.
    - **Justificação:** esperada = situação sob independência [ACS_ACM, p. 8]; fórmula (total da linha × total da coluna)/n [complemento].

### M2-8 — Correlação (2,0 valores)

> **Enunciado.** Entre tempo de espera e satisfação obteve-se r = −0,64, com p < 0,001. Interprete direção, intensidade, significância e limite causal.

- **Resposta:** **direção** negativa (maiores tempos de espera acompanham menor satisfação); **intensidade** moderada a relativamente forte; **significância:** p < 0,001 dá evidência estatística contra a ausência de correlação linear; **limite causal:** não demonstra causalidade nem exclui confundimento.
    - **Razão:** sinal = direção, módulo = força [Slides 18/09, p. 8 a 10]; associação ≠ causalidade [Slides 18/09, p. 47 a 54]. Solução oficial: [Modelo de Exame 2, Resolução, Q8].

**Variações possíveis**

- **Pergunta:** "r = 0,82 (marketing e vendas), r = −0,75 (preço e quantidade) e r = 0,03 (antiguidade e satisfação). Direção, intensidade, uma conclusão correta e uma incorreta."
    - **Resposta:** A: positiva, forte; correta: mais marketing tende a estar associado a mais vendas; incorreta: aumentar o marketing causará necessariamente mais vendas. B: negativa, forte; correta: preços mais altos tendem a estar associados a menores quantidades vendidas; incorreta: a relação é necessariamente causal. C: praticamente inexistente, muito fraca; correta: pouca evidência de associação linear; incorreta: não existe qualquer relação.
    - **Justificação:** [Ficha de exercícios, Ex. 3].

### M2-9 — PCA (3,0 valores)

> **Enunciado.** Foi aplicada PCA a quatro variáveis padronizadas. KMO = 0,76 e Bartlett p < 0,001. Os valores próprios são 2,60; 0,82; 0,38; 0,20. Os loadings da Componente 1 são:
>
> | Variável | Loading C1 |
> |---|---|
> | Qualidade | 0,91 |
> | Durabilidade | 0,87 |
> | Satisfação | 0,89 |
> | Preço percebido | −0,72 |
>
> **a)** Avalie a adequação da PCA.\
> **b)** Pelo critério de Kaiser, quantas componentes reteria?\
> **c)** Calcule a variância explicada por C1.\
> **d)** Proponha uma interpretação para C1.

- **a) Resposta:** KMO = 0,76 sugere adequação razoável/boa; Bartlett p < 0,001 rejeita H₀: R = I, logo há correlação suficiente entre as variáveis. Os dois indicam que a PCA é adequada.
    - **Razão:** [PCA, p. 7 e 8]. O Bartlett não indica quais variáveis estão associadas, nem que todas as correlações sejam fortes [PCA, p. 7].
- **b) Resposta:** **1 componente**, porque só 2,60 > 1.
    - **Razão:** critério de Kaiser: reter componentes com λ > 1 [PCA, p. 11].
- **c) Resposta:** variância de C1 = 2,60/4 × 100 = **65%**.
    - **Razão:** o valor próprio representa a variância explicada pela componente [PCA, p. 10]; com variáveis padronizadas o total é p = 4 (a soma dos valores próprios é 4,00). A divisão por p é [complemento]; no exemplo dos slides, 3,62/8 = 45,3% [PCA, p. 10].
- **d) Resposta:** C1 opõe qualidade, durabilidade e satisfação elevadas a preço percebido elevado; um nome possível é "valor/qualidade global percebida", sendo uma dimensão sintética.
    - **Razão:** loadings com sinais opostos descrevem um contraste; o nome é uma interpretação substantiva baseada nos loadings mais elevados [PCA, p. 18 e 19]. Solução oficial: [Modelo de Exame 2, Resolução, Q9].

**Variações possíveis**

- **Pergunta:** "Que % de variância explica C2 e qual a acumulada com C1 e C2?"
    - **Resposta:** C2 = 0,82/4 = 20,5%; acumulada = 65% + 20,5% = 85,5% (meu cálculo).
    - **Justificação:** variância acumulada = soma das % das componentes [PCA, p. 14].
- **Pergunta:** "Reteria 2 componentes? Quando poderia fazê-lo?"
    - **Resposta:** o Kaiser aponta 1; poderia justificar-se 2 se o objetivo exigisse mais informação (85,5% acumulada) e a C2 fosse interpretável, mas a decisão deve combinar vários critérios.
    - **Justificação:** [PCA, p. 9]; comparação de soluções com 1 e 2 componentes [Exercícios PCA, Ex. 10].

### M2-10 — ACS/ACM (2,0 valores)

> **Enunciado.** Num mapa de correspondências, as categorias "Premium" e "Muito satisfeito" surgem próximas, afastadas da origem, ambas com cos² elevado. A Dimensão 1 explica 62% da inércia. Interprete estes resultados e indique duas cautelas necessárias antes de concluir que existe uma associação forte.

- **Resposta:** a proximidade sugere associação entre "Premium" e "Muito satisfeito" e o cos² elevado indica boa representação no mapa. **Duas cautelas:** (1) a proximidade visual não basta sem analisar as **contribuições** das categorias; (2) o plano representa 62% da inércia, **omitindo 38%**. Além disso, depende do contexto e não prova causalidade.
    - **Razão:** a proximidade não se interpreta como medida direta de associação sem coordenadas, contribuições e qualidade de representação [ACS_ACM, p. 12 e 13]; cos² mede a qualidade de representação [ACS_ACM, p. 13]; as dimensões explicam partes da inércia [ACS_ACM, p. 10]. Solução oficial: [Modelo de Exame 2, Resolução, Q10].

**Variações possíveis**

- **Pergunta:** "Estar longe da origem significa que a categoria contribui muito?"
    - **Resposta:** não; uma coordenada de grande magnitude não implica grande contribuição nem boa representação.
    - **Justificação:** [ACS_ACM, p. 13 e 14]; [Exercícios ACS_ACM, Ex. 4.3, 4.4 e 5.3g].

### M2-11 — Clustering (2,0 valores)

> **Enunciado.** Foram comparadas soluções de K-means:
>
> | K | Silhouette média | Menor cluster |
> |---|---|---|
> | 2 | 0,43 | 38% |
> | 3 | 0,57 | 18% |
> | 4 | 0,49 | 4% |
>
> **a)** Qual solução escolheria? Justifique.\
> **b)** Indique duas limitações do K-means.

- **a) Resposta:** **K = 3**: tem a maior silhouette (0,57) e o menor cluster ainda tem 18%. K = 4 tem pior silhouette e um cluster de apenas 4%, que exige cautela.
    - **Razão:** escolhe-se o k com silhouette mais alta, mas a decisão deve considerar também o tamanho dos grupos, a estabilidade e a interpretabilidade [Análise Classificatória, p. 13 a 15; Exercícios Classificatória, Ex. 5d].
- **b) Resposta:** (1) requer k definido previamente; (2) depende da inicialização dos centroides. Também: sensível a escala e a outliers; favorece clusters aproximadamente compactos e de forma semelhante.
    - **Razão:** [Análise Classificatória, p. 11, 12 e 21]; [Clustering, p. 18 a 20]. Solução oficial: [Modelo de Exame 2, Resolução, Q11].

**Variações possíveis**

- **Pergunta:** "Com os mesmos dados, a maior silhouette fosse K = 4 (0,60) mas com um cluster de 4%. Escolheria K = 4 automaticamente?"
    - **Resposta:** não; um cluster muito pequeno pode indicar uma solução pouco útil ou instável; devem ponderar-se tamanho, estabilidade e interpretação.
    - **Justificação:** [Exercícios Classificatória, Ex. 5d].

### M2-12 — Discriminante e classificação (3,0 valores)

> **Enunciado.** Considere "Cliente em risco" como classe positiva. O modelo produziu:
>
> | | Previsto: risco | Previsto: sem risco |
> |---|---|---|
> | **Real: risco** | 36 | 14 |
> | **Real: sem risco** | 9 | 41 |
>
> **a)** Identifique TP, FN, FP e TN.\
> **b)** Calcule accuracy, recall e precision.\
> **c)** Explique por que razão a avaliação apenas nos dados de treino pode ser otimista.

- **a) Resposta:** TP = 36; FN = 14; FP = 9; TN = 41; N = 100.
    - **Razão:** linhas = real, colunas = previsto; TP e TN são os acertos [Análise Discriminante, p. 11 e 13].
- **b) Resposta:** accuracy = (36 + 41)/100 = **77%**; recall = 36/(36 + 14) = **72%**; precision = 36/(36 + 9) = **80%**.
    - **Razão:** [Análise Discriminante, p. 12 e 14].
- **c) Resposta:** porque o modelo foi ajustado aos mesmos dados; deve usar-se uma amostra de teste independente ou validação cruzada para estimar a capacidade de generalização.
    - **Razão:** [Análise Discriminante, p. 19]. Solução oficial: [Modelo de Exame 2, Resolução, Q12].

**Variações possíveis**

- **Pergunta:** "Calcule o F1-score e a balanced accuracy."
    - **Resposta:** F1 = 2 · 0,80 · 0,72/(0,80 + 0,72) ≈ 0,758. Recall do grupo "sem risco" = 41/50 = 82%; balanced accuracy = (72% + 82%)/2 = 77% (meu cálculo).
    - **Justificação:** [Análise Discriminante, p. 15 e 18].
- **Pergunta:** "Que tipo de erro é um FN neste contexto e porque é relevante?"
    - **Resposta:** erro do tipo II (omissão): um cliente em risco não é identificado; é relevante porque a empresa não atua sobre ele, e traduz-se num recall mais baixo.
    - **Justificação:** [Análise Discriminante, p. 13]; a leitura de negócio é [complemento].

# 4. Exercícios resolvidos das aulas

*(As respostas seguem as soluções fornecidas pela professora. Quando uma resposta foi deduzida por mim, está indicado.)*

## 4.1 Ficha de exercícios — Medidas de associação

- **Pergunta (Ex. 1):** Medida mais apropriada em: a) salário anual e anos de experiência; b) ranking de satisfação e ranking de qualidade; c) rendimento mensal e incumprimento (Sim/Não); d) género e preferência por produto (A, B ou C); e) visitas ao website e valor gasto.
    - **Resposta:** a) Pearson; b) Spearman; c) ponto-bisserial; d) qui-quadrado + V de Cramér; e) Pearson.
    - **Justificação:** quantitativa × quantitativa → Pearson; ordinais/rankings → Spearman; quantitativa × binária → ponto-bisserial; categórica × categórica → qui-quadrado + V [Slides 18/09, p. 45].
- **Pergunta (Ex. 2):** Idade, rendimento, satisfação (0–10), canal de aquisição, género e churn (Sim/Não). Medida para: 1) idade e rendimento; 2) satisfação e churn; 3) género e churn; 4) canal de aquisição e churn.
    - **Resposta:** 1) Pearson; 2) ponto-bisserial; 3) qui-quadrado + V; 4) qui-quadrado + V.
    - **Justificação:** [Slides 18/09, p. 56 a 61].
- **Pergunta (Ex. 3):** Caso A: r = 0,82 (marketing e vendas); Caso B: r = −0,75 (preço e quantidade); Caso C: r = 0,03 (antiguidade e satisfação). Direção, intensidade, uma conclusão correta e uma incorreta.
    - **Resposta:** A: positiva, forte; correta: mais investimento tende a estar associado a mais vendas; incorreta: aumentar o marketing causará necessariamente mais vendas. B: negativa, forte; correta: preços mais altos tendem a estar associados a menores quantidades; incorreta: a relação é necessariamente causal. C: praticamente inexistente, muito fraca; correta: pouca evidência de associação linear; incorreta: não existe qualquer relação.
    - **Justificação:** [Slides 18/09, p. 9 a 13 e 47 a 54].
- **Pergunta (Ex. 4):** r = 0,01 entre duas variáveis. Pode concluir-se que não existe qualquer relação?
    - **Resposta:** não; r ≈ 0 só indica ausência de associação **linear**; pode existir uma relação não linear forte, por exemplo em U.
    - **Justificação:** [Slides 18/09, p. 12 e 13].
- **Pergunta (Ex. 5):** Seis lojas ordenadas por limpeza (1 a 6) e satisfação (A: 1 e 2; B: 2 e 1; C: 3 e 4; D: 4 e 3; E: 5 e 5; F: 6 e 6). Sem calcular: a associação é positiva ou negativa? O Spearman seria elevado ou reduzido?
    - **Resposta:** positiva; Spearman elevado.
    - **Justificação:** os rankings são muito semelhantes: lojas bem posicionadas numa variável tendem a estar bem posicionadas na outra [Slides 18/09, p. 17 a 21]. (Meu cálculo: ρ ≈ 0,89.)
- **Pergunta (Ex. 6):** Medida para: a) ranking de desempenho × ranking de satisfação dos clientes; b) despesa em publicidade × vendas; c) horas de estudo × classificação, com alguns valores extremos.
    - **Resposta:** a) Spearman; b) Pearson; c) Spearman.
    - **Justificação:** em c) o Spearman é mais robusto à presença de outliers [Slides 18/09, p. 22 e 23].
- **Pergunta (Ex. 7):** r_pb = −0,58, com churn = 1 e não churn = 0, e a variável quantitativa é a satisfação. Interprete.
    - **Resposta:** clientes com maior satisfação tendem a ter menor probabilidade de churn; associação moderada a forte.
    - **Justificação:** [Slides 18/09, p. 33, 35 e 36].
- **Pergunta (Ex. 8):** Se a codificação for invertida (churn = 0, não churn = 1), o valor absoluto da correlação altera-se? E o sinal?
    - **Resposta:** o valor absoluto **não** se altera; o **sinal muda** (negativa passa a positiva e vice-versa).
    - **Justificação:** o sinal depende da codificação da variável binária [Slides 18/09, p. 33].
- **Pergunta (Ex. 9):** p < 0,001 e V = 0,08 (género e compra). Interpretação mais adequada: A) associação forte; B) evidência estatística de associação, mas fraca; C) o género causa o comportamento; D) não existe associação.
    - **Resposta:** **B**.
    - **Justificação:** p < 0,001 indica evidência de associação; V = 0,08 indica intensidade fraca [Slides 18/09, p. 42 a 44].
- **Pergunta (Ex. 10):** Complete: o qui-quadrado responde à pergunta ___; o V de Cramér responde à pergunta ___.
    - **Resposta:** qui-quadrado: existe evidência estatística de associação entre as variáveis? V de Cramér: qual é a intensidade da associação?
    - **Justificação:** [Slides 18/09, p. 40 a 43].
- **Pergunta (Ex. 11):** r = 0,70 entre satisfação dos colaboradores e retenção. Quais afirmações são corretas?
    - **Resposta:** corretas: colaboradores mais satisfeitos tendem a permanecer mais tempo; as variáveis estão associadas; pode existir uma terceira variável a influenciar ambas. Incorreta: aumentar a satisfação aumentará necessariamente a retenção.
    - **Justificação:** [Slides 18/09, p. 49, 50 e 62].
- **Pergunta (Ex. 12):** Forte associação entre vendas de guarda-chuvas e de chocolate quente. Explicação plausível sem relação causal direta?
    - **Resposta:** a temperatura ou a estação do ano: em períodos frios aumenta simultaneamente a procura de ambos; a variável meteorológica é uma variável de confusão.
    - **Justificação:** mesma lógica de gelados × afogamentos e temperatura [Slides 18/09, p. 51 a 53].
- **Pergunta (Ex. 13):** Caso integrador (telecomunicações): medida para idade × rendimento; satisfação × churn; género × churn; canal de aquisição × tipo de plano; rendimento × satisfação.
    - **Resposta:** Pearson; ponto-bisserial; qui-quadrado + V; qui-quadrado + V; Pearson.
    - **Justificação:** [Slides 18/09, p. 45 e 61]. O Pearson mede direção e intensidade da associação linear; o Spearman a associação monótona entre rankings; o ponto-bisserial a associação entre quantitativa e binária; o qui-quadrado avalia se existe evidência de associação e o V a sua força.
- **Pergunta (Ex. 14):** O diretor diz: "Como a satisfação está fortemente correlacionada com a retenção, devemos aumentar a satisfação para reduzir o churn". Como responde, enquanto analista?
    - **Resposta:** os resultados indicam que satisfação e retenção estão associadas, mas correlação elevada não demonstra causalidade; os clientes mais satisfeitos podem permanecer mais tempo, mas uma terceira variável pode influenciar ambas; antes de decidir são necessários estudos adicionais sobre a causalidade.
    - **Justificação:** [Slides 18/09, p. 49, 50 e 54].

## 4.2 Wooclap — Quiz de Análise Preliminar

*(O PDF só traz as perguntas, todas com 0 votos e sem chave de respostas; as respostas abaixo foram deduzidas por mim a partir dos slides.)*

- **Pergunta 1:** Base com informação sobre 500 clientes. Cada linha representa: uma variável, uma observação/unidade estatística, uma categoria ou uma população?
    - **Resposta:** uma observação/unidade estatística.
    - **Justificação:** linhas = unidades estatísticas; colunas = variáveis [Análise Preliminar, p. 4 e 5].
- **Pergunta 2:** "Sexo" (masculino/feminino) é: discreta, contínua, nominal ou ordinal?
    - **Resposta:** qualitativa nominal.
    - **Justificação:** categorias sem ordem natural [Análise Preliminar, p. 8].
- **Pergunta 3:** "Grau de concordância" (escala 1 a 5) é: discreta, contínua, nominal ou ordinal?
    - **Resposta:** qualitativa ordinal.
    - **Justificação:** a escala tem ordem; "Grau de satisfação 1 a 5 → qualitativa ordinal" [Análise Preliminar, p. 9].
- **Pergunta 4:** "Número de compras realizadas por um cliente" é: nominal, ordinal, discreta ou contínua?
    - **Resposta:** quantitativa discreta.
    - **Justificação:** [Análise Preliminar, p. 9 e 10].
- **Pergunta 5:** A idade de uma pessoa é, conceptualmente: ordinal, discreta, contínua ou nominal?
    - **Resposta:** quantitativa contínua.
    - **Justificação:** a idade surge como exemplo de contínua [Análise Preliminar, p. 10].
- **Pergunta 6:** Código numérico para tipo de cliente (1 = Particular, 2 = Empresarial, 3 = Institucional). A variável é: discreta, contínua, nominal ou ordinal?
    - **Resposta:** qualitativa nominal.
    - **Justificação:** números não significam necessariamente variável quantitativa [Análise Preliminar, p. 9].
- **Pergunta 7:** Tempos de espera 4, 5, 6, 7, 8 e 40. Qual afirmação é correta?
    - **Resposta:** a média é mais influenciada pelo valor 40 do que a mediana.
    - **Justificação:** [Análise Preliminar, p. 16]; o 40 não deve ser eliminado automaticamente [Análise Preliminar, p. 29].
- **Pergunta 8:** Qual é uma medida de dispersão: média, mediana, moda ou amplitude interquartil?
    - **Resposta:** amplitude interquartil.
    - **Justificação:** [Análise Preliminar, p. 18 e 19].
- **Pergunta 9:** Boxplot com Q1 = 1400, mediana = 1600 e Q3 = 1800. Qual afirmação é correta?
    - **Resposta:** 50% dos clientes têm rendimento entre 1400 € e 1800 €.
    - **Justificação:** 50% central entre Q1 e Q3; AIQ = 400 [Análise Preliminar, p. 19 e 21].
- **Pergunta 10:** Tempos de atendimento agrupados em intervalos de 5 minutos. Representação mais adequada?
    - **Resposta:** histograma, porque os intervalos correspondem a valores consecutivos de uma variável quantitativa.
    - **Justificação:** [Análise Preliminar, p. 22 e 23].
- **Pergunta 11:** Um cliente com rendimento muito superior ao dos restantes. Atitude mais adequada?
    - **Resposta:** verificar a origem e o impacto do valor antes de decidir como proceder.
    - **Justificação:** [Análise Preliminar, p. 29].
- **Pergunta 12:** Rendimento mensal sem valor registado para alguns clientes. Afirmação correta?
    - **Resposta:** os valores em falta devem ser identificados e a sua origem e impacto avaliados antes de decidir como tratá-los.
    - **Justificação:** [Análise Preliminar, p. 27].

## 4.3 Exercícios de PCA

*(Contexto: quatro medidas quantitativas — preço, qualidade percebida, durabilidade e satisfação — de oito produtos; pretende-se verificar se se resumem a menos dimensões.)*

- **Pergunta (Ex. 1):** Qual afirmação é mais adequada para uma PCA: todas qualitativas; quantitativas com estrutura de correlação que justifique a PCA; apenas uma variável; variáveis independentes entre si?
    - **Resposta:** as variáveis devem ser quantitativas e ter uma estrutura de correlação que justifique a PCA.
    - **Justificação:** [PCA, p. 5 e 6].
- **Pergunta (Ex. 2):** V ou F: variáveis qualitativas (região, tipo de produto) podem entrar diretamente numa PCA convencional como as quantitativas.
    - **Resposta:** **Falso**.
    - **Justificação:** [PCA, p. 5] (os indicadores do exemplo são quantitativos).
- **Pergunta (Ex. 3 e 4):** Porque padronizar antes da PCA? V ou F: se o Preço varia entre 20 e 1000 e as restantes entre 1 e 10, a PCA sem padronizar pode dar ao Preço influência desproporcional.
    - **Resposta:** para colocar as variáveis numa escala comparável e evitar que a escala de uma variável domine as componentes; a segunda afirmação é **Verdadeira**.
    - **Justificação:** [PCA, p. 5].
- **Pergunta (Ex. 5):** Principal objetivo da PCA?
    - **Resposta:** reduzir o número de dimensões preservando tanto quanto possível a informação da variabilidade.
    - **Justificação:** [PCA, p. 3].
- **Pergunta (Ex. 6):** KMO = 0,78; Bartlett χ² = 31,42, gl = 6, p < 0,001. Interprete o KMO, o Bartlett e o conjunto.
    - **Resposta:** KMO indica adequação razoável/boa; Bartlett rejeita H₀ (matriz de correlações não é a identidade), logo há associações entre algumas variáveis; em conjunto, há estrutura de correlações suficiente para a PCA.
    - **Justificação:** [PCA, p. 7 e 8]. (gl = p(p − 1)/2 = 6 com p = 4 [complemento].)
- **Pergunta (Ex. 7):** Valores próprios 3,18; 0,48; 0,25; 0,09 (variâncias 79,5%, 12,0%, 6,3%, 2,2%). Que representa um valor próprio? % da 1.ª? Acumulada das duas primeiras? Kaiser? Quantas reter?
    - **Resposta:** valor próprio = variância explicada pela componente; 1.ª = 79,5%; acumulada = 79,5 + 12,0 = 91,5%; Kaiser retém 1 componente; reter 1 é razoável porque só a 1.ª tem λ > 1 e explica 79,5% da variância total.
    - **Justificação:** [PCA, p. 10, 11 e 14].
- **Pergunta (Ex. 8):** Loadings da C1: preço 0,91; qualidade 0,94; durabilidade 0,93; satisfação 0,90. O que representa um loading? Variáveis mais associadas? Interpretação? Seria adequado chamar-lhe "qualidade global do produto"?
    - **Resposta:** loading = relação entre uma variável original e uma componente, indicando intensidade e direção; as quatro variáveis, sobretudo qualidade (0,94) e durabilidade (0,93); C1 = dimensão de qualidade global do produto; o nome é adequado se se deixar claro que é uma interpretação sintética e não uma variável observada.
    - **Justificação:** [PCA, p. 16 a 19].
- **Pergunta (Ex. 9):** Scores na C1: A = −2,10; B = −1,45; C = −0,80; D = −0,20; E = 0,55; F = 0,95; G = 1,35; H = 1,70. Maior e menor score? Comparar A e H? Um score positivo implica valores altos em todas as variáveis? Loading vs score?
    - **Resposta:** maior = H (1,70); menor = A (−2,10); H tem perfil muito mais associado à dimensão (qualidade global) do que A; **não**, o score resulta da combinação das variáveis e depende dos loadings; loading = variável ↔ componente; score = observação ↔ componente.
    - **Justificação:** [PCA, p. 20 e 21].
- **Pergunta (Ex. 10):** Solução A: 1 componente, 79,5%, complexidade muito baixa; Solução B: 2 componentes, 91,5%, complexidade baixa. Qual preserva mais informação? Qual é mais simples? Qual para um único indicador? Qual para compreender dimensões?
    - **Resposta:** B preserva mais informação; A é mais simples; A serve melhor para um indicador sintético que ordene os produtos; B é mais informativa para compreender várias dimensões.
    - **Justificação:** [PCA, p. 9 e 14].
- **Pergunta (Ex. 11):** Avalie: (a) a PCA permite concluir que a qualidade causa maior satisfação; (b) a C1 pode ser um indicador sintético das características globais; (c) dois produtos com scores próximos na C1 são necessariamente semelhantes em tudo; (d) a redução de dimensionalidade facilita a análise mas implica perda de informação.
    - **Resposta:** (a) inadequada: a PCA identifica uma dimensão comum associada a qualidade, durabilidade e satisfação; (b) adequada, com cautela; (c) inadequada: scores próximos numa componente não garantem proximidade no espaço multivariado completo; (d) adequada.
    - **Justificação:** [PCA, p. 21 e 22].

## 4.4 Exercícios de ACS e ACM

*(Contexto do Ex. 1 a 4: tabela de contingência produto preferido (Tecnologia, Casa, Lazer) × faixa etária (18–34, 35–49, 50+), n = 263.)*

- **Pergunta (Ex. 1.1 a 1.3):** "Faixa etária" é: quantitativa discreta, nominal, ordinal ou contínua? E "tipo de produto"? V ou F: por serem ambas qualitativas, a distinção nominal/ordinal não é relevante.
    - **Resposta:** faixa etária = **qualitativa ordinal**; tipo de produto = **qualitativa nominal**; **Falso**: a distinção é relevante porque as ordinais têm uma ordem natural e as nominais não.
    - **Justificação:** [Análise Preliminar, p. 8].
- **Pergunta (Ex. 1.4 e 1.5):** Que afirmação descreve a relação (existem diferenças nas preferências por faixa etária, sugerindo associação)? V ou F: a associação permite concluir que a idade determina a preferência.
    - **Resposta:** opção B (existem diferenças, sugerindo possível associação); **Falso**: associação não permite concluir que uma variável determine ou cause a outra.
    - **Justificação:** [Slides 18/09, p. 47 a 54].
- **Pergunta (Ex. 2.1 a 2.5):** Qui-quadrado de independência com χ² = 28,64, gl = 4, p < 0,001. Hipóteses? Decisão? Significado? O teste identifica as categorias responsáveis? Permite concluir causalidade?
    - **Resposta:** H₀: faixa etária e tipo de produto são independentes; H₁: existe associação. Como p < 0,001, rejeita-se H₀ (5%): há evidência de associação. **Não** identifica as categorias responsáveis (só a associação global; para isso, por exemplo, resíduos ajustados). **Não** permite concluir causalidade.
    - **Justificação:** [ACS_ACM, p. 6 e 7].
    - **Nota (meu cálculo):** aplicando a fórmula à tabela do enunciado obtém-se χ² ≈ 17,0, e não 28,64; os valores do exercício são ilustrativos.
- **Pergunta (Ex. 3.1 a 3.5):** Inércia total 0,109; Dimensão 1 = 0,081; Dimensão 2 = 0,028. O que representa a inércia? Quantas dimensões para toda a inércia? % da 1.ª? Acumulada das duas? Quantas dimensões num mapa 2D?
    - **Resposta:** inércia = medida da associação, relacionada com o afastamento em relação à independência (opção B); são necessárias 2 dimensões; 1.ª = 0,081/0,109 ≈ 74,3%; as duas somam 100%; o mapa representa 2 dimensões.
    - **Justificação:** [ACS_ACM, p. 10]. (Observação minha: 28,64/263 ≈ 0,109, ou seja, inércia total = χ²/n [complemento].)
- **Pergunta (Ex. 4.1 e 4.2):** Coordenadas (Dim. 1, Dim. 2): Tecnologia (0,72; 0,08), Casa (−0,18; −0,61), Lazer (−0,51; 0,48), 18–34 (0,65; 0,14), 35–49 (−0,10; −0,55), 50+ (−0,72; 0,43). Quais as mais positivas e negativas na dimensão 1 e como interpretá-la? Que categorias no lado positivo da dimensão 2?
    - **Resposta:** mais positivas: Tecnologia (0,72) e 18–34 (0,65); mais negativas: 50+ (−0,72) e Lazer (−0,51). A dimensão 1 opõe um perfil de clientes mais jovens com Tecnologia a um perfil de clientes mais velhos com Lazer. No lado positivo da dimensão 2: Lazer (0,48) e 50+ (0,43), sugerindo associação entre 50+ e Lazer (com cautela quanto às contribuições e à qualidade da representação).
    - **Justificação:** [ACS_ACM, p. 12 e 13].
- **Pergunta (Ex. 4.3 e 4.4):** Contribuições: Tecnologia 31,5% e 1,2%; Casa 2,8% e 35,4%; Lazer 18,6% e 24,7%; 18–34 27,1% e 4,8%; 35–49 1,4% e 29,6%; 50+ 18,6% e 4,3%. Que categoria mais contribui para cada dimensão? A contribuição interpreta-se como a coordenada? Diferença?
    - **Resposta:** dimensão 1: Tecnologia (31,5%); dimensão 2: Casa (35,4%). Não: a coordenada indica a posição e a direção da categoria na dimensão; a contribuição indica a importância da categoria na construção da dimensão. Uma coordenada elevada em valor absoluto não implica elevada contribuição.
    - **Justificação:** [ACS_ACM, p. 13 e 14].
- **Pergunta (Ex. 4.5):** Conclusão de um analista: "Categorias próximas no mapa estão diretamente associadas; logo os clientes 18–34 preferem Tecnologia e os 50+ preferem Casa". Concorda?
    - **Resposta:** não integralmente: a proximidade pode sugerir padrões de associação, mas a posição visual não basta para estabelecer associação direta ou causal; deve analisar-se também a contribuição e o cos², as restantes categorias e a informação estatística subjacente. Aqui as coordenadas sugerem proximidade entre 18–34 e Tecnologia e entre 50+ e Lazer (não Casa).
    - **Justificação:** [ACS_ACM, p. 12 e 13].
- **Pergunta (Ex. 5.1):** Variáveis: faixa etária, canal de compra, rendimento mensal, tipo de plano, método de pagamento, idade, região, frequência de utilização, nº de produtos. Quais são adequadas para uma ACM?
    - **Resposta:** faixa etária, canal de compra, tipo de plano, método de pagamento e região (qualitativas). Rendimento, idade, frequência de utilização e nº de produtos são quantitativas e, em geral, não entram diretamente numa ACM convencional.
    - **Justificação:** [ACS_ACM, p. 18].
- **Pergunta (Ex. 5.2):** Inércia corrigida: dim. 1 = 38,6%, 2 = 24,7%, 3 = 15,2%, 4 = 9,1%, 5 = 6,4% (acumuladas 38,6; 63,3; 78,5; 87,6; 94,0). Quanto explica a 1.ª e as duas primeiras? Quantas dimensões no mapa 2D? Que informação fica por representar?
    - **Resposta:** 38,6% e 63,3%; 2 dimensões; 100% − 63,3% = **36,7%** fica por representar.
    - **Justificação:** [ACS_ACM, p. 20].
- **Pergunta (Ex. 5.3):** Coordenadas, contribuições e cos² da dimensão 1 de várias categorias (50+: 0,91; Plano Premium: 0,88; Compra Loja: 0,71 do lado positivo; 18–34: −0,82; Plano Básico: −0,74; Compra Online: −0,65 do lado negativo). Que categorias se destacam? Interpretação da dimensão 1? Que categorias mais contribuem? Diferença entre contribuição e cos²? Qual a melhor representada? Porque é enganador olhar só para a distância à origem?
    - **Resposta:** lado positivo: 50+, Plano Premium, Compra Loja; lado negativo: 18–34, Plano Básico, Compra Online. Dimensão 1 = contraste entre clientes mais velhos com Premium e compras em loja e clientes mais jovens com Básico e compras online (síntese minha dos padrões, não uma característica fornecida pela ACM). Maior contribuição: 50+ (22,7%), Plano Premium (20,5%), 18–34 (18,4%), Plano Básico (15,3%). **Contribuição** = importância na construção da dimensão; **cos²** = qualidade da representação da categoria nessa dimensão. Melhor representada: Plano Premium (cos² = 0,91). Uma categoria afastada da origem tem coordenada grande, mas isso não implica contribuição elevada nem boa representação.
    - **Justificação:** [ACS_ACM, p. 13, 14 e 19].
- **Pergunta (Ex. 5.4):** Um analista conclui que "a ACM identificou três segmentos (jovens digitais, tradicionais e premium) que podem ser usados diretamente em campanhas". Concorda?
    - **Resposta:** não integralmente: a ACM analisa a estrutura de associação entre categorias de várias variáveis qualitativas e identifica padrões ou perfis nas categorias, mas não identifica diretamente segmentos de clientes; para criar segmentos usa-se análise classificatória (hierárquico ou K-means). A ACM pode ser etapa exploratória ou de redução da informação antes do agrupamento.
    - **Justificação:** [ACS_ACM, p. 22 e 23].

## 4.5 Exercícios de Análise Classificatória

- **Pergunta (Ex. 1a a 1c):** Clientes A (25 anos; 1200 €; 45; 6,2), B (28; 1350; 50; 6,8), C (52; 3200; 120; 8,4), D (55; 3400; 125; 8,7). Entre A e B e entre A e C, qual terá menor distância? Porque padronizar? A padronização elimina a influência de valores extremos?
    - **Resposta:** A e B (valores mais semelhantes em todas as variáveis); padroniza-se para pôr as variáveis numa escala comparável e evitar que uma de valores numericamente elevados domine a distância; **não** elimina a influência de extremos (resolve a escala; K-means e outros métodos baseados em distâncias continuam sensíveis).
    - **Justificação:** [Análise Classificatória, p. 4, 5 e 21].
- **Pergunta (Ex. 2a a 2d):** Dendrograma de oito clientes (A a H). Quantos grupos no início? Que acontece em cada etapa? Cortando em dois grupos, quais? A escolha do corte deve ser só visual?
    - **Resposta:** 8 grupos; em cada etapa agregam-se dois grupos suficientemente próximos segundo a distância e o critério de ligação, e o número de grupos diminui; com dois grupos: {A, B, C, D} e {E, F, G, H}; **não**: a inspeção visual deve ser complementada com critérios de validação (silhouette), estabilidade, dimensão dos grupos e interpretabilidade.
    - **Justificação:** [Análise Classificatória, p. 7 a 9].
- **Pergunta (Ex. 3a a 3d):** Silhouette por número de grupos: ligação simples 0,21; 0,18; 0,15; 0,12 (2 a 5 grupos); Ward 0,35; 0,41; 0,37; 0,29. Melhor solução de Ward? O maior silhouette prova que é a única solução correta? Distância entre grupos na ligação simples? Porque comparar métodos?
    - **Resposta:** Ward com 3 grupos (0,41); **não**: o silhouette é um critério importante, mas não determina uma única solução verdadeira (ver estabilidade, dimensão, interpretabilidade, contexto); na ligação simples a distância entre dois grupos é a **menor distância entre duas observações, uma de cada grupo** (opção C); comparar métodos permite ver se a estrutura é semelhante com procedimentos diferentes, o que dá evidência complementar, não prova de robustez.
    - **Justificação:** [Análise Classificatória, p. 10, 13 a 15 e 20; Clustering, p. 16].
- **Pergunta (Ex. 4a a 4e):** K-means: hierárquico ou não? Informação a definir antes? Etapas? V ou F: inicializações diferentes podem dar soluções diferentes; V ou F: o K-means pode ser aplicado diretamente a nominais com distância euclidiana.
    - **Resposta:** não hierárquico; o número de clusters k; (1) definir k, (2) inicializar centros, (3) atribuir cada observação ao centro mais próximo, (4) recalcular centros, (5) repetir até convergir; **Verdadeiro**; **Falso** (a distância euclidiana não é diretamente adequada a nominais; é preciso uma medida de proximidade adequada).
    - **Justificação:** [Análise Classificatória, p. 11 e 12; Clustering, p. 18 a 20].
- **Pergunta (Ex. 5a a 5d):** Silhouette K-means: 2 → 0,36; 3 → 0,42; 4 → 0,35; 5 → 0,29. Melhor solução? Que significa silhouette mais alto? Duas outras questões antes de escolher k? Com k = 3 e grupos de 120, 110 e 3 observações, escolhe-se automaticamente?
    - **Resposta:** 3 clusters (0,42); em geral, observações mais próximas das do seu próprio cluster do que das dos outros (melhor separação e coesão); outras questões: estabilidade, dimensão dos clusters, interpretabilidade, comparação com outras soluções ou métodos, sensibilidade a extremos; **não**: um cluster com 3 observações pode indicar uma solução pouco útil ou instável.
    - **Justificação:** [Análise Classificatória, p. 13 a 15].
- **Pergunta (Ex. 6a a 6c):** Médias por cluster (idade, rendimento, despesa, satisfação): C1 (52; 3500; 145; 8,7); C2 (31; 1800; 65; 7,8); C3 (46; 1500; 48; 6,2). Caracterize. Basta analisar médias? Que outras informações?
    - **Resposta:** C1: clientes mais velhos, rendimento e despesa elevados, satisfação alta; C2: mais jovens, rendimento e despesa intermédios, satisfação relativamente elevada; C3: idade intermédia, rendimento e despesa mais baixos, menor satisfação. **Não** basta: as médias podem esconder grande variabilidade dentro de cada cluster; analisar dispersão, tamanho, distribuições, variáveis qualitativas e externas e estabilidade.
    - **Justificação:** [Análise Classificatória, p. 16 e 17].
- **Pergunta (Ex. 7a a 7c):** Três clusters (80, 120 e 100 clientes) com taxas de abandono 7,5%, 10,0% e 21,0%; a variável abandono não foi usada no clustering; teste de associação com p = 0,012. O abandono é variável interna ou externa? O teste sugere associação? Pode afirmar-se que o Cluster 3 representa necessariamente os clientes com maior risco individual?
    - **Resposta:** **externa** (não foi usada para construir os clusters); **sim**, p = 0,012 < 0,05 rejeita a independência; **não necessariamente**: 21% é a taxa observada no conjunto do cluster, não o risco individual de cada cliente nem um modelo preditivo.
    - **Justificação:** [Análise Classificatória, p. 18].
- **Pergunta (Ex. 8a a 8c):** Hierárquico (silhouette 0,39; grupos 62, 84, 134) e K-means (0,42; 60, 87, 133). O que sugere a semelhança? Prova a robustez? Outras formas de avaliar a estabilidade?
    - **Resposta:** sugere estrutura de agrupamento semelhante nos dois métodos (evidência complementar); **não** prova robustez; avaliar estabilidade com diferentes inicializações do K-means, reamostragem, comparação de métodos, estabilidade das atribuições, sensibilidade a extremos e outros critérios de validação.
    - **Justificação:** [Análise Classificatória, p. 19, 20 e 24; Clustering, p. 26].
- **Pergunta (Ex. 9a a 9d):** Analista: "K-means identificou três grupos; como a silhouette foi mais alta para k = 3, são os três grupos verdadeiros; o Cluster 3 tem maior taxa de abandono, logo cada cliente tem maior probabilidade individual; a empresa deve direcionar já as campanhas para todos". V ou F: (a) silhouette mais alta para k = 3 prova três grupos verdadeiros; (b) o número de clusters deve considerar também estabilidade, dimensão e interpretabilidade; (c) 21% de abandono é a probabilidade individual; (d) associação entre cluster e abandono implica que o cluster é a causa.
    - **Resposta:** (a) **Falso**; (b) **Verdadeiro**; (c) **Falso**; (d) **Falso**.
    - **Justificação:** [Análise Classificatória, p. 15, 18 e 22].

# 5. Outros pontos do programa que podem aparecer

## 5.1 Análise preliminar

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

## 5.2 Bivariada

- **Pergunta:** "Uma correlação forte e significativa basta para concluir?"
    - **Resposta:** não; significância estatística não implica relevância prática nem causalidade, e a interpretação é mais importante do que o cálculo.
    - **Justificação:** [Slides 18/09, p. 63].
- **Pergunta:** "Como se calcula a correlação ponto-bisserial e de que depende o sinal?"
    - **Resposta:** codifica-se a binária numericamente (por exemplo Churn = Sim → 1, Não → 0) e calcula-se o Pearson entre a quantitativa e a binária codificada; o sinal depende da codificação.
    - **Justificação:** [Slides 18/09, p. 31, 32 e 33].

## 5.3 ACM

- **Pergunta:** "Que variáveis podem entrar numa ACM?"
    - **Resposta:** categóricas; as quantitativas só se forem categorizadas, com decisão justificada.
    - **Justificação:** [ACS_ACM, p. 18].
- **Pergunta:** "Como se avalia a inércia na ACM?"
    - **Resposta:** pela inércia corrigida por dimensão e acumulada (exemplo: 57,3%, 15,6%, 13,8% e 8,3%; acumulada 72,9% nas duas primeiras).
    - **Justificação:** [ACS_ACM, p. 20].


## 5.4 Medidas de dispersão (artigo e slides)

- **Pergunta:** "Duas distribuições com a mesma média podem ser diferentes?"
    - **Resposta:** sim; podem ter dispersões muito diferentes (por exemplo, notas médias de 5 em Biologia e em Matemática, mas muito mais variáveis em Matemática).
    - **Justificação:** [Artigo de dispersão, p. 40 e 41]; [Análise Preliminar, p. 18].
- **Pergunta:** "Como se calculam a amplitude, a variância, o desvio-padrão e o coeficiente de variação?"
    - **Resposta:** amplitude = máximo − mínimo; variância amostral s² = Σ(x − x̄)²/(n − 1); desvio-padrão s = √s² (mantém a unidade original); coeficiente de variação = s/x̄ (habitualmente em %).
    - **Justificação:** [Artigo de dispersão, p. 41 a 43 (numeração da revista)]. A amplitude não considera os valores intermédios; a variância usa todas as observações [Artigo de dispersão, p. 41].
- **Pergunta:** "Notas de Biologia e Matemática: amplitudes 4 e 8, variâncias 1,09 e 8,54. O que concluir?"
    - **Resposta:** Matemática tem maior dispersão (maior amplitude e variância).
    - **Justificação:** [Artigo de dispersão, p. 41 e 42].

## 5.5 Distâncias, ligações e K-means (slides de Clustering)

- **Pergunta:** "Calcule as distâncias de Manhattan, euclidiana e de Chebyshev entre p = (1, 0, 2) e q = (6, 0, 3)."
    - **Resposta:** Manhattan = |1−6| + |0−0| + |2−3| = 6; euclidiana = √(25 + 0 + 1) = √26 ≈ 5,10; Chebyshev = máx(5, 0, 1) = 5.
    - **Justificação:** Minkowski com r = 1, 2 e r → ∞ [Clustering, p. 7 a 9].
- **Pergunta:** "Que distância usar para variáveis categóricas e binárias? Calcule: p = (Vermelho, Pequeno, Gasolina) e q = (Azul, Pequeno, Elétrico); p = (1, 0, 1, 1) e q = (1, 1, 0, 1)."
    - **Resposta:** categóricas: distância de *matching* (nº de discordâncias/n) → 2/3; binárias: Hamming (nº de posições diferentes) → 2.
    - **Justificação:** [Clustering, p. 5, 10 e 11].
- **Pergunta:** "Defina ligação simples, completa e método de Ward."
    - **Resposta:** simples: distância entre os pontos mais próximos dos dois grupos; completa: distância entre os pontos mais afastados; Ward: minimiza a variância dentro dos grupos (menor aumento da variabilidade interna).
    - **Justificação:** [Clustering, p. 16]; [Análise Classificatória, p. 10]; [Exercícios Classificatória, Ex. 3c].
- **Pergunta:** "Agregativo vs divisivo?"
    - **Resposta:** aglomerativo (bottom-up): cada observação começa num grupo e juntam-se os mais próximos até restar um; divisivo (top-down): começa-se com tudo num grupo e dividem-se; o aglomerativo é o mais usado e ambos dão um dendrograma.
    - **Justificação:** [Clustering, p. 15].
- **Pergunta:** "Que requisitos tem o K-means e como se pode escolher k?"
    - **Resposta:** dados numéricos e variáveis padronizadas (z-score ou min-max); k pelo método do cotovelo (WSS em função de k, escolher o "cotovelo") ou pela silhouette média mais alta.
    - **Justificação:** [Clustering, p. 18, 22, 24 e 25].
- **Pergunta:** "Como preparar variáveis nominais ou ordinais para o clustering?"
    - **Resposta:** nominais: codificação *one-hot*; ordinais: codificação ordinal (ex.: Baixo = 1, Médio = 2, Alto = 3).
    - **Justificação:** [Clustering, p. 22].
- **Pergunta:** "Passos de um projeto de clustering?"
    - **Resposta:** preparação dos dados; seleção e transformação de variáveis; escolha do algoritmo; escolha do número de clusters; avaliação e interpretação.
    - **Justificação:** [Clustering, p. 21].

# 6. Banco de treino — variações para resolveres sozinho

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


# 7. Erros mais comuns e frases-chave

## 7.1 Erros mais comuns

1. Dizer que correlação ou associação **causa** algo.
2. Dizer que r ≈ 0 significa "não há relação" (só não há relação **linear**).
3. Escolher Pearson para rankings/ordinais (é Spearman) ou ponto-bisserial para duas categóricas (é qui-quadrado + V).
4. Dizer que p < 0,05 implica associação *forte* (a intensidade mede-se com o V de Cramér).
5. Dizer que padronizar resolve outliers.
6. Dizer que o K-means escolhe o k sozinho ou que a silhouette mais alta prova o número "verdadeiro" de grupos.
7. Confundir recall com precision (recall: dividir pelos **reais** positivos; precision: dividir pelos **previstos** positivos).
8. Dizer que accuracy alta significa bom desempenho em todos os grupos.
9. Dizer que ACS/ACM são clustering, ou que proximidade no mapa prova associação.
10. Dizer que a PCA prova que uma variável causa outra, ou que scores próximos implicam observações iguais.
11. Eliminar outliers ou substituir omissos pela média sem ver a origem.
12. Chamar contínua a uma contagem, ou quantitativa a um código.
13. Esquecer a justificação e a interpretação **no contexto**, que os modelos pedem sempre.
14. Aceitar o cluster com 3 observações só porque tem a silhouette mais alta.

## 7.2 Frases-chave para memorizar

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
