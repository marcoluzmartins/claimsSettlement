---
title: "Análise de Dados — Resumo do que é importante"
subtitle: "Exame de 2 de novembro (60 min, 20 valores, uma folha A4 manuscrita)"
lang: pt-PT
---

# 1. O que o exame vai pedir

- **Formato** (email da professora): 60 minutos, 20 valores; escolha múltipla, resposta aberta, cálculos, interpretação de resultados e justificação. Avalia-se **escolher e aplicar o método certo** e **interpretar criticamente**, não só saber fórmulas.
- **O teste-modelo** tem 5 questões de escolha múltipla (Grupo I) e 7 questões de resposta curta (Grupo II). Tempo médio por questão: cerca de 5 minutos. A solução oficial (Modelo_solucao) confirma as respostas que tinha no guia anterior: Grupo I = B, A, B, C, D.
- **O Modelo de Exame 2** é mais longo (90 minutos sugeridos): Parte A (6 conceitos curtos) e Parte B (6 problemas de aplicação). Serve como treino extra; o exame real tem 60 minutos.
- **Instrução que se repete** em todos os modelos: *apresentar os cálculos, justificar as escolhas e interpretar no contexto; associação não é causalidade*.

**Os 6 tipos de pergunta que se repetem**

| Tipo | Exemplo | O que fazer |
|---|---|---|
| Classificar variáveis | número de compras, grau de satisfação, montante, região | Nominal / ordinal / discreta / contínua |
| Escolher a medida ou o método | satisfação 1–5 × intenção de recompra 1–5 | Ver os tipos de variáveis e justificar |
| Interpretar um coeficiente ou teste | r = −0,64; p = 0,002 e V = 0,21 | Direção, força, significância, limite causal |
| Calcular | variância explicada, accuracy, recall, precision | Escrever a fórmula e o resultado |
| V/F | PCA, ACS, K-means | Atenção a "sempre", "necessariamente", "causa" |
| Avaliar uma conclusão | "o cluster 3 abandona mais, logo cada cliente…" | Dizer onde está o erro e reformular |

# 2. Escolher o método (começar pela pergunta)

| Pergunta | Método | Tipo |
|---|---|---|
| Como resumir muitas variáveis quantitativas? | **PCA** | — |
| Que associações existem entre categorias? | **ACS** (2 variáveis) / **ACM** (várias) | — |
| Que grupos existem (desconhecidos)? | **Análise Classificatória** | Não supervisionada |
| A que grupo pertence um novo caso (grupos conhecidos)? | **Análise Discriminante** | Supervisionada |

[Overview, p. 13 e 15]. Maximizam coisas diferentes: PCA → variância explicada; Discriminante → separação entre grupos; Clustering → homogeneidade dentro dos grupos [Análise Discriminante, p. 25 e 26].

# 3. Análise preliminar e estatística descritiva

**Essencial**

- **Tipos de variáveis:** qualitativa nominal (sem ordem: sexo, região, código de cliente), ordinal (com ordem: satisfação baixa/média/alta, escala 1–5, faixa etária); quantitativa discreta (contagem) e contínua (medição). *O tipo não depende de como os valores são escritos* [Análise Preliminar, p. 7 a 11].
- **Tendência central:** média (sensível a extremos), mediana (robusta), moda. **Dispersão:** amplitude, variância, desvio-padrão, AIQ = Q3 − Q1 [Análise Preliminar, p. 15 a 19]. A variância amostral é Σ(x − x̄)²/(n − 1) e o coeficiente de variação é s/x̄ [artigo "Medidas de dispersão", numeração da revista, p. 41 a 43].
- **Gráficos:** barras/circular para qualitativas; histograma (classes consecutivas, barras contíguas) para quantitativas; boxplot para mediana, quartis e extremos [Análise Preliminar, p. 13, 14, 20 e 22 a 24].
- **Forma:** cauda à direita → média > mediana > moda; cauda à esquerda → média < mediana < moda [Análise Preliminar, p. 26].
- **Qualidade dos dados:** valores omissos (quantos, onde, aleatórios?), inconsistências, duplicados, unidades; **valores extremos não se eliminam automaticamente**, verifica-se a origem e o impacto [Análise Preliminar, p. 27 a 29]. O quiz do Wooclap segue a mesma lógica: verificar origem e impacto antes de decidir; não substituir sempre pela média.

**Cálculos típicos**

- Tempos de espera 4, 5, 6, 7, 8, 40 → média = 70/6 ≈ 11,7; mediana = (6 + 7)/2 = 6,5 → a média é mais influenciada pelo 40 [Wooclap, pergunta 7].
- Boxplot com Q1 = 1400, mediana = 1600, Q3 = 1800 → AIQ = 400; **50% dos clientes têm rendimento entre 1400 € e 1800 €** [Wooclap, pergunta 9; Análise Preliminar, p. 21].

**Erros a evitar:** dizer que o código do cliente é quantitativo; dizer que se elimina sempre o outlier; confundir "50% acima da mediana" com "50% entre Q2 e Q3".

# 4. Medidas de associação (bivariada)

| X | Y | Medida |
|---|---|---|
| Quantitativa | Quantitativa | **Pearson** (associação linear) |
| Ordinal | Ordinal | **Spearman** (ordens/ranks; associação monótona; mais robusta a outliers) |
| Quantitativa | Binária | **Ponto-bisserial** (Pearson com a binária codificada 0/1) |
| Categórica | Categórica | **Qui-quadrado + V de Cramér** |

[Slides 18/09, p. 45; Ficha de exercícios, ex. 1 e 2]

**Essencial**

- **Pearson:** −1 ≤ r ≤ 1; o sinal dá a direção e o módulo a força [Slides 18/09, p. 8 a 10]. **r ≈ 0 não significa ausência de relação**, só de relação *linear*; pode existir uma relação em U (ficha, ex. 4) [Slides 18/09, p. 12 e 13].
- **Ponto-bisserial:** o sinal depende da codificação; **inverter 0/1 muda o sinal mas não o valor absoluto** (ficha, ex. 8) [Slides 18/09, p. 33]. Ex.: r = −0,58 com churn = 1 → clientes mais satisfeitos têm menor probabilidade de churn (ficha, ex. 7).
- **Qui-quadrado:** H₀ independência, H₁ associação; compara observadas com esperadas; p < 0,05 rejeita H₀ [ACS_ACM, p. 6 a 8]. **O qui-quadrado diz *se* há associação; o V de Cramér diz *quão forte*** (ficha, ex. 10) [Slides 18/09, p. 40 a 44].
- **p < 0,001 e V = 0,08** → estatisticamente significativa, mas fraca (ficha, ex. 9, resposta B).
- **Associação ≠ causalidade:** a relação pode ser inversa, ter um terceiro fator (confundimento) ou ser acaso. Exemplos: gelados × afogamentos (temperatura); guarda-chuvas × chocolate quente (frio/chuva) [Slides 18/09, p. 50 a 53; ficha, ex. 12].

**Fórmulas úteis [complemento: não vêm nos slides]:** χ² = Σ(O − E)²/E; E = (total da linha × total da coluna)/n; gl = (linhas − 1)(colunas − 1); V = √(χ² / (n · min(l − 1, c − 1))). A solução oficial do teste-modelo refere que o qui-quadrado se aplica "desde que os pressupostos relativos às frequências esperadas sejam satisfeitos" (regra habitual: E ≥ 5).

**Frases-modelo**

- *"r = −0,64: associação linear negativa moderada a forte; maiores tempos de espera tendem a acompanhar menor satisfação; p < 0,001 dá evidência contra ausência de correlação linear; não demonstra causalidade nem exclui confundimento."* [Modelo de Exame 2, resolução, Q8]
- *"p = 0,002 → rejeita-se H₀, há evidência de associação; V = 0,21 → intensidade fraca a moderada; a relevância prática avalia-se no contexto."* [Modelo de Exame 2, resolução, Q7]

**Para treinar o Q7 do Modelo de Exame 2 (canal × satisfação):** frequências esperadas 24, 36 e 40 em ambas as linhas; χ² ≈ 8,89 (gl = 2); V = √(8,89/200) ≈ 0,21, o que coincide com o V dado no enunciado (cálculos meus).

# 5. PCA / ACP

**Essencial**

- Variáveis **quantitativas**; **padronizar** (Z = (X − x̄)/s) quando as escalas diferem, para que uma variável de escala grande não domine [PCA, p. 5; exercícios PCA, ex. 3 e 4]. Variáveis qualitativas não entram diretamente numa PCA convencional (exercícios PCA, ex. 2).
- **Objetivo:** reduzir a dimensionalidade preservando tanta variância quanto possível; as componentes são **combinações lineares** das variáveis originais, ordenadas pela variância explicada [PCA, p. 3].
- **Adequação:** matriz de correlações; **KMO** (adequação; 0,76–0,84 interpretados como razoável/boa); **Bartlett** H₀: R = I, p < 0,05 → rejeita H₀, há correlação suficiente (não diz quais variáveis nem que todas as correlações sejam fortes) [PCA, p. 6 a 8].
- **Quantas componentes reter:** valores próprios, **Kaiser (λ > 1)**, scree plot (cotovelo), variância acumulada e interpretabilidade; a decisão é conjunta [PCA, p. 9 a 14].
- **Variância explicada pela componente = λ/p** (com variáveis padronizadas, Σλ = p) [PCA, p. 10; complemento para Σλ = p]. Ex.: λ = 2,60; 0,82; 0,38; 0,20 → C1 = 2,60/4 = 65% (Modelo de Exame 2, Q9); λ = 3,18 → 79,5% (exercícios PCA, ex. 7).
- **Loading** = variável ↔ componente (intensidade e direção). **Score** = observação ↔ componente (posição) [PCA, p. 18, 20 e 21].
- **Interpretar:** loadings altos e positivos em todas as variáveis → dimensão *global* (ex.: "qualidade global do produto", "desempenho global"); sinais opostos → contraste (qualidade/durabilidade/satisfação positivas contra preço percebido negativo → "valor/qualidade global percebida") [PCA, p. 16 e 19; Modelo de Exame 2, Q9d].
- **O que a PCA não faz:** não estabelece causalidade, não dá o nome da componente (é interpretação), e **scores próximos não implicam observações semelhantes em todas as variáveis** [PCA, p. 21 e 22].

**Perguntas dos exercícios**

- 1 componente (79,5%) vs 2 componentes (91,5%): a 2.ª preserva mais informação; a 1.ª é mais simples e serve para um indicador único para ordenar; a 2.ª é mais informativa para ver dimensões (exercícios PCA, ex. 10).
- *"A qualidade causa maior satisfação"* → inadequado; dizer antes *"a PCA identifica uma dimensão comum associada a qualidade, durabilidade e satisfação"*. *"Um score positivo implica valores altos em todas as variáveis"* → falso; depende dos loadings (ex. 9 e 11).

# 6. ACS e ACM

**Essencial**

- **ACS:** duas variáveis categóricas (tabela de contingência) → mapa. **ACM:** várias variáveis categóricas simultaneamente. **Não são clustering** e não dão segmentos; para segmentar usa-se classificatória (a ACM pode ser etapa exploratória prévia) [ACS_ACM, p. 22 e 23; exercícios ACS/ACM, ex. 5.4].
- **Variáveis da ACM:** apenas categóricas (faixa etária, canal, plano, pagamento, região). Rendimento, idade, frequência e nº de produtos são quantitativas e, em geral, não entram diretamente [ACS_ACM, p. 18; exercícios, ex. 5.1].
- **Qui-quadrado antes da ACS:** diz se há associação global, não *onde* está (para isso, resíduos ajustados ou o mapa) [ACS_ACM, p. 6; exercícios, ex. 2.4].
- **Inércia:** afastamento da independência; % de uma dimensão = inércia da dimensão / inércia total. Ex.: 0,081/0,109 ≈ 74,3%; as duas dimensões somam 100%. Na ACM: inércia corrigida 38,6% + 24,7% = 63,3%; **por representar = 100 − 63,3 = 36,7%** (exercícios, ex. 3 e 5.2). O número de dimensões num mapa bidimensional é 2.
- **Coordenada:** posição e sentido na dimensão. **Contribuição (%):** importância da categoria na construção da dimensão. **cos²:** qualidade de representação. **Longe da origem ≠ contribui muito nem bem representada** [ACS_ACM, p. 13 e 14].
- **Ler uma dimensão:** comparar os lados positivo e negativo (contraste). Ex.: 1.ª dimensão opõe 18–34 + Tecnologia a 50+ + Lazer (exercícios, ex. 4.1); na ACM, 50+, Plano Premium e Compra em Loja contra 18–34, Plano Básico e Compra Online (ex. 5.3).
- **Proximidade no mapa ≠ associação direta nem causal:** ver contribuições, cos², % de inércia (62% representada → 38% omitida) e o contexto (exercícios, ex. 4.5; Modelo de Exame 2, Q10).

**Perguntas dos exercícios**

- Faixa etária (18–34, 35–49, 50+) é **qualitativa ordinal**; tipo de produto é **nominal**; a distinção nominal/ordinal é relevante (ex. 1.1 a 1.3).
- Diferenças nas preferências por faixa etária sugerem associação, mas não permitem dizer que a idade *determina* a preferência (ex. 1.4 e 1.5).
- Categoria que mais contribui: a de maior contribuição (ex.: Tecnologia 31,5% na dimensão 1; Casa 35,4% na dimensão 2); melhor representada: maior cos² (ex.: Plano Premium 0,91).

# 7. Análise Classificatória (clustering)

**Essencial**

- Grupos **desconhecidos**; não supervisionada; observações no mesmo grupo semelhantes e em grupos diferentes distintas [Análise Classificatória, p. 3; Clustering, p. 2 e 4].
- **Distâncias:** euclidiana, Manhattan, Chebyshev e Minkowski (quantitativas); *matching* (categóricas); Hamming (binárias) [Clustering, p. 5 a 11]. Ex.: p = (1, 0, 2) e q = (6, 0, 3) → Manhattan 6; euclidiana √26; Chebyshev 5 [Clustering, p. 9].
- **Padronização:** resolve diferenças de escala, **não elimina valores extremos** [Análise Classificatória, p. 5 e 21; exercícios classificatória, ex. 1].
- **Hierárquico aglomerativo:** começa com n grupos e vai agregando os mais próximos até 1; o dendrograma mostra a altura (distância) e o corte define k, que se escolhe *depois*. **Divisivo:** o contrário [Análise Classificatória, p. 7 a 9; Clustering, p. 15]. **Ligações:** simples (distância mínima), completa (máxima), Ward (menor aumento da variabilidade interna) [Clustering, p. 16; Análise Classificatória, p. 10; exercícios, ex. 3c].
- **K-means** (não hierárquico, só numéricas): define k → centros iniciais → atribui ao mais próximo → recalcula centros → repete até estabilizar. Resultados podem diferir com inicializações diferentes; não se aplica diretamente a variáveis nominais com distância euclidiana [Análise Classificatória, p. 11 e 12; Clustering, p. 18 a 20; exercícios, ex. 4].
- **Limitações do K-means:** k prévio, sensível à inicialização e a outliers, escala, assume clusters de tamanho e variância semelhantes [Clustering, p. 20; Modelo de Exame 2, resolução, Q11].
- **Silhouette:** s(i) = (b − a)/max(a, b); **≈ 1** bem integrada e afastada dos outros; **≈ 0** fronteira; **< 0** possivelmente mal atribuída [Análise Classificatória, p. 14; Clustering, p. 25; Modelo de Exame 2, Q6]. Escolhe-se o k com silhouette média mais alta, **mas** também se olha para o tamanho dos grupos, a estabilidade e a interpretabilidade. Ex.: k = 4 com 0,49 e um cluster de 4% → preferir k = 3 (0,57; menor cluster 18%); cluster com 3 observações não se aceita automaticamente (exercícios, ex. 5d). Método do cotovelo (WSS) é outro critério [Clustering, p. 24].
- **Caracterizar os grupos:** médias *e* dispersão, tamanho e distribuições; variáveis externas (como abandono) podem diferir entre clusters, mas isso **não prova que o clustering está certo nem causalidade** [Análise Classificatória, p. 17 e 18].
- **Cuidado com conclusões:** silhouette alto não prova "grupos verdadeiros"; uma taxa de abandono de 21% num cluster **não** é a probabilidade individual de cada cliente; métodos concordantes são evidência complementar, não prova de robustez (exercícios, ex. 7 a 9).

# 8. Análise Discriminante

**Essencial**

- Grupos **conhecidos**; supervisionada; estuda diferenças entre grupos, as variáveis que mais os distinguem e classifica novas observações [Análise Discriminante, p. 3]. Dois grupos: uma função **D = a₀ + a₁X₁ + … + aₚXₚ**; D > corte → Grupo 1 [p. 7 e 9]. Com K grupos, no máximo **min(p, K − 1)** funções [p. 10].
- **Pressupostos:** variáveis quantitativas, sem multicolinearidade grave, normalidade multivariada nos grupos, covariâncias aproximadamente iguais, sem observações muito influentes. **Teste de Box:** H₀: Σ₁ = … = Σ_K; p < 0,05 → evidência contra; p ≥ 0,05 não "prova" igualdade [p. 20 e 21].
- **Matriz de confusão** (linhas = real, colunas = previsto): **TP, FN, FP, TN** [p. 11 e 13].

| Medida | Fórmula | Lê-se |
|---|---|---|
| Accuracy | (TP + TN)/N | proporção total de classificações corretas |
| Recall | TP/(TP + FN) | dos que pertencem ao grupo, quantos foram identificados |
| Precision | TP/(TP + FP) | dos classificados no grupo, quantos pertencem a ele |
| F1 | 2·P·R/(P + R) | equilíbrio entre precision e recall |
| Balanced accuracy | média dos recalls | desempenho equilibrado entre grupos |

[p. 12 a 18]

- **FP** = erro tipo I (falso alarme); **FN** = erro tipo II (omissão) [p. 13].
- **Accuracy alta pode enganar** com grupos desequilibrados (84,3% com recall do Grupo 1 de 2%) [p. 12 e 23].
- **Validação:** avaliar só na amostra de estimação é otimista; usar validação cruzada ou amostra de teste [p. 19; Modelo de Exame 2, Q12c].
- Coeficiente elevado ≠ causa; classificar não é explicar [p. 24].

**Cálculos para saber de cor**

| Matriz | TP / FN / FP / TN | Accuracy | Recall | Precision | F1 |
|---|---|---|---|---|---|
| Teste-modelo (doença) | 30 / 20 / 10 / 40 | 70% | 60% | 75% | 0,667 |
| Modelo de Exame 2 (risco) | 36 / 14 / 9 / 41 | 77% | 72% | 80% | 0,758 (meu cálculo) |
| Exemplo dos slides (abandono) | 26 / 18 / 26 / 210 | 84,3% | 59,1% | 50% | 0,542 |

# 9. Erros mais comuns (reler antes do exame)

1. Dizer que correlação ou associação **causa** algo.
2. Dizer que r ≈ 0 significa "não há relação".
3. Escolher Pearson para rankings ou para ordinais (é Spearman) ou ponto-bisserial para duas categóricas.
4. Dizer que p < 0,05 implica associação *forte* (usar V de Cramér).
5. Dizer que padronizar resolve outliers.
6. Dizer que o K-means escolhe o k sozinho ou que o silhouette mais alto prova o número "verdadeiro" de grupos.
7. Confundir recall com precision (recall: dividir pelos **reais** positivos; precision: dividir pelos **previstos** positivos).
8. Confundir accuracy com bom desempenho em todos os grupos.
9. Dizer que ACS/ACM são clustering ou que proximidade no mapa prova associação.
10. Dizer que a PCA prova que uma variável causa outra, ou que scores próximos implicam observações iguais.
11. Eliminar outliers ou substituir omissos pela média sem ver a origem.
12. Chamar contínua a uma contagem, ou quantitativa a um código.

# 10. Modelo de Exame 2: resposta-resumo

| Q | Resposta de referência |
|---|---|
| 1 | Ordinal: categorias ordenadas (satisfação baixa/média/alta). Discreta: contagem (nº de compras). |
| 2 | A mediana é robusta a extremos; a média é influenciada por eles. |
| 3 | **Spearman** (duas ordinais; associação monótona com base em ordens). |
| 4 | PCA reduz dimensionalidade; loading = variável ↔ componente; score = observação ↔ componente. |
| 5 | Clustering: grupos desconhecidos (não supervisionado); discriminante: grupos conhecidos (supervisionado). |
| 6 | Silhouette ≈ 1: bem integrada; negativo: possivelmente mal atribuída. |
| 7 | H₀: independência; H₁: associação; qui-quadrado; p = 0,002 rejeita H₀; V = 0,21 fraca a moderada. |
| 8 | r = −0,64: negativa moderada a forte; p < 0,001; sem causalidade. |
| 9 | KMO = 0,76 razoável/boa; Bartlett rejeita R = I; Kaiser → 1 componente; C1 = 2,60/4 = 65%; contraste qualidade/durabilidade/satisfação vs preço. |
| 10 | Proximidade sugere associação; cos² elevado = boa representação; cautelas: ver contribuições, 38% da inércia omitida, contexto, sem causalidade. |
| 11 | K = 3 (silhouette 0,57; menor cluster 18%); K = 4 tem cluster de 4%. Limitações: k prévio, inicialização, escala/outliers, clusters compactos. |
| 12 | TP 36, FN 14, FP 9, TN 41; accuracy 77%, recall 72%, precision 80%; treino é otimista. |

# 11. Plano para os últimos dias

- **31 de outubro:** ler este resumo; fazer o **Modelo de Exame 2** a cronómetro (60–90 min) sem consultar; corrigir com a resolução; ler a secção 9.
- **1 de novembro:** refazer só o que falhou; resolver os exercícios de PCA e ACS/ACM e a ficha de associação; copiar **à mão** a folha de apoio (ver nota abaixo) e testar usá-la numa questão.
- **Dia do exame:** levar a folha manuscrita; gerir o tempo (cerca de 5 min por questão); ler bem V/F e escolha múltipla.

**Nota sobre a folha de apoio:** o email da professora só permite **uma folha A4 manuscrita**, preparada individualmente; **não são permitidas folhas impressas ou fotocopiadas**. A folha que preparei (`folha_apoio_frente_verso.pdf`) é um guia para **copiares à mão**; não a imprimas para levar.

# 12. Fontes e limites

- Matéria: slides da UC (Análise Preliminar, Slides 18/09, PCA, ACS_ACM, Análise Classificatória, Clustering, Análise Discriminante, Overview, Apresentação da UC), ficha de exercícios de associação, exercícios e soluções de PCA, ACS/ACM e Análise Classificatória, Modelo de Exame 2 e solução oficial do teste-modelo.
- O **Wooclap** só traz as perguntas (todas com 0 votos, sem a chave de respostas); as respostas indicadas foram deduzidas dos slides.
- Os **artigos** (medidas de associação, medidas de dispersão, Correspondence Analysis, PCA em inglês e a revisão de Cluster Analysis de Jaeger) foram usados como apoio; só a parte de medidas de dispersão (variância e coeficiente de variação) entrou aqui. Não os li em detalhe e não os considero matéria de exame se não aparecerem nos slides.
- Marquei **[complemento]** o que não está nos documentos da professora.
