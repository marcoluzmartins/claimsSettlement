# Preparação para a discussão com a professora

Documento de estudo (não se entrega). Cada pergunta tem uma **resposta curta** para dizeres com as tuas palavras e, quando útil, **o que não deves afirmar**. As perguntas estão por ordem de probabilidade dentro de cada bloco.

---

## 0. Números a ter na ponta da língua

| Facto | Valor |
|---|---|
| Amostra / variáveis | 300 clientes, 19 variáveis (9 quantitativas) |
| Casos completos / excluídos | 280 / 20 (6,7%) |
| Abandono total | 50 (16,7%) |
| Abandonos por cluster (deduzidos) | 5 / 8 / 31 → 44 nos 280 (15,7%) |
| Abandonos nos 20 excluídos | 6 (30%); Fisher *p* ≈ 0,12 |
| Tamanhos dos clusters | 62 / 83 / 135 (22% / 30% / 48%) |
| Abandono por cluster | 8,1% / 9,6% / 23,0% |
| Qui-quadrado cluster × abandono | 10,41 (gl 2), *p* = 0,0055 (0,006 no R5), V = 0,193 |
| Silhuetas | *k*=2: 0,353 · 3: 0,325 · 4: 0,319 · 5: 0,278 · 6: 0,212 |
| V de Cramér da Região | R5: 0,039; correto: √(1,364/300) = 0,067 |
| Valores próprios | somam 9,033 (devia ser 9) |
| Método de pagamento | *p* = 0,065; V = 0,155 |
| Extremos | rendimento máx. 5 544 e despesa máx. 241: ambos a ≈ 3,7 DP |
| Resposta à questão central | Não, por ora: hipótese de trabalho a validar |

---

## 1. Perguntas gerais (quase certas)

**1.1. Em uma frase, qual é a tua conclusão?**
O R5 é um bom ponto de partida, mas não é, na forma atual, uma base adequada para segmentar e classificar novos clientes: precisa de correções, de análises de robustez e de um modelo para novos clientes.

**1.2. Porque é que a apreciação do critério C é "Insuficiente", se uma conclusão é sólida?**
Porque das quatro conclusões que sustentam a decisão só uma está suportada (o abandono é maior no Cluster 3, e mesmo essa é uma associação). Uma é parcial e duas não têm suporte. Além disso, falta o objetivo de classificar novos clientes. A apreciação é do conjunto, não de uma conclusão isolada.

**1.3. O que é que o R5 tem de bom?**
Descrição clara dos clientes; cálculos de base coerentes (as médias ponderadas dos clusters batem com as globais); a ligação cluster–abandono confirma-se por recálculo; e o analista foi transparente ao admitir que a silhueta é máxima em *k* = 2.

**1.4. Porque é que não reproduziste a análise?**
O enunciado diz que o objetivo não é reproduzi-la, mas avaliá-la. Verifiquei a coerência interna dos números publicados (recalculei testes e somas), e as verificações estão no anexo.

**1.5. O que farias de diferente do analista?**
Verificar o mecanismo dos dados em falta; tratar os extremos (logaritmo ou *k*-medoids) e comparar soluções; validar *k* com mais critérios e estabilidade; e construir um modelo supervisionado para classificar novos clientes com variáveis disponíveis à entrada.

---

## 2. Dados e valores em falta

**2.1. Porque é que eliminar 20 clientes pode ser um problema?**
Só é inofensivo se a falta de dados for aleatória (MCAR). Se, por exemplo, quem não indica o rendimento for diferente dos restantes, apagá-los distorce o retrato. O R5 não testou isso.

**2.2. Como chegaste aos 6 abandonos nos 20 excluídos?**
O R5 dá a taxa de abandono e o tamanho de cada cluster: 8,1% de 62, 9,6% de 83 e 23,0% de 135 dá 5, 8 e 31 abandonos (cada taxa arredondada só admite um inteiro). Somam 44 nos 280. Como no total há 50 abandonos, os outros 6 estão nos 20 excluídos.

**2.3. Isso prova que a eliminação distorceu os resultados?**
Não. 6 em 20 (30%) contra 15,7% é um sinal, mas com *p* ≈ 0,12 a diferença pode ser acaso: com só 20 casos há pouca potência. É um alerta para investigar, não uma conclusão.
*Não afirmar:* "os dados em falta estão ligados ao abandono".

**2.4. Que alternativa propões?**
Comparar excluídos e incluídos; imputação múltipla (MICE) ou por vizinhos mais próximos; e análise de sensibilidade (repetir a análise com e sem imputação).

**2.5. Como se classificaria um cliente novo com dados em falta?**
Não se pode "apagá-lo". É preciso imputar o valor em falta ou usar um modelo que lide com faltas.

---

## 3. Padronização e valores extremos (o erro conceptual)

**3.1. Porque é que dizes que a afirmação sobre a padronização é errada?**
O R5 diz que padronizar "garante que o K-means não seja afetado de forma relevante pelos valores extremos". Mas padronizar (*z-score*) é uma transformação linear: muda a escala, não a forma da distribuição. É como passar de metros para centímetros: o cliente mais alto continua o mais alto. Os extremos continuam a ≈ 3,7 desvios-padrão e o K-means, que minimiza somas de quadrados, continua sensível a eles.

**3.2. Então para que serve padronizar?**
Para que variáveis em escalas diferentes (euros, anos, percentagem) contribuam de forma comparável para a distância. É necessário, mas não resolve os extremos.

**3.3. Como se tratariam os extremos?**
Transformação logarítmica ou *winsorização*; ou um método mais robusto, como *k*-medoids (PAM).

**3.4. Tens a certeza de que o cluster "de elevado valor" é a cauda?**
Não: é uma hipótese. Rendimento médio de 3 648 contra um Q3 global de 2 252 é compatível com isso, mas sem os dados só posso pedir a análise de sensibilidade.

**3.5. Os extremos são mesmo *outliers*?**
3,7 DP é raro, mas o R5 não os trata nem os examina com gráficos. Convinha ver histogramas ou caixas-de-bigodes antes de decidir.

---

## 4. Escolha de *k* e qualidade dos clusters

**4.1. Porque criticas a escolha de *k* = 3?**
Não digo que esteja errada: escolher pelo negócio é legítimo, e o analista foi transparente. Critico a justificação: um só índice, sem estabilidade, e todas as silhuetas (0,21–0,35) indicam estrutura fraca. Além disso, *k* = 4 (0,319) quase empata e a figura do R5 sugere quatro nuvens.

**4.2. O que significa silhueta de 0,325?**
Mede se cada cliente está mais perto do seu grupo do que do grupo vizinho (−1 a 1). Segundo Kaufman e Rousseeuw: acima de 0,50 há estrutura razoável; entre 0,26 e 0,50 é fraca; até 0,25 não há estrutura substancial.

**4.3. Então os clusters não existem?**
Existem perfis interpretáveis, mas as fronteiras são difusas. Por isso digo que "distintos" é forte demais, e que a segmentação é uma hipótese a validar.

**4.4. Que critérios adicionais usarias?**
*Elbow*, Calinski–Harabasz, *gap*, e estabilidade por *bootstrap* (Rand ajustado); silhueta por cluster; e comparar *k* = 2, 3 e 4.

**4.5. K-means é o método certo?**
É convencional, mas assume grupos aproximadamente esféricos e é sensível a extremos. Dado que há variáveis ordinais e categóricas, poderia comparar com *k*-medoids com distância de Gower, ou com modelos de mistura gaussiana.

**4.6. Porque é que quatro variáveis correlacionadas são um problema?**
Rendimento, despesa, visitas e produtos medem em parte a mesma coisa (*r* até 0,84). Na distância euclidiana "pesam" várias vezes, e o agrupamento fica dominado pela dimensão de valor. Usar os *scores* da PCA ou selecionar variáveis ajuda.

---

## 5. Análise bivariada e testes

**5.1. Porque criticas o Pearson?**
Rendimento e despesa são assimétricos, e há variáveis ordinais e de contagem. O Spearman (que usa a ordem) é mais robusto. E o R5 não mostra gráficos de dispersão nem *p*-values, e só apresenta as correlações "principais".

**5.2. O que é o V de Cramér e porque está errado na Região?**
Mede a força da associação entre duas categóricas (0 a 1). Como o abandono é binário, V = √(χ²/*n*) = √(1,364/300) = 0,067, não 0,039. As outras sete linhas conferem, por isso é uma gralha, sem efeito nas conclusões.

**5.3. O que significa *p* = 0,065 no método de pagamento?**
Que, se não houvesse relação, uma diferença destas apareceria por acaso cerca de 6,5 vezes em 100. Não passa o limite de 5%, por isso não há prova suficiente. Dizer que "pode ser um fator relevante" é uma hipótese, não uma conclusão.

**5.4. Não é injusto ignorar um *p* de 0,065?**
Não ignoro: aceito como pista. O problema é o tratamento desigual: fidelização (0,088) e perfil (0,090) estão em situação quase igual e não são mencionados. E testaram-se oito variáveis, pelo que algo ficar perto do limite pode ser acaso.

**5.5. Havia problema nos oito testes?**
Sem correção, aumenta a probabilidade de um falso positivo, mas como nenhum é significativo o efeito prático é pequeno. Também não se verificaram as frequências esperadas (≥ 5).

---

## 6. PCA

**6.1. O que está errado na Tabela 6?**
Numa PCA com 9 variáveis padronizadas os valores próprios somam 9. No R5 somam 9,033. E a variância do CP1 (42,58%) não corresponde a 3,846/9 = 42,73%. As percentagens somam 100,08%. São diferenças pequenas, mas indicam erro de arredondamento ou de execução, e devem ser corrigidas.

**6.2. Os dois componentes estão bem escolhidos?**
É defensável: há uma quebra clara entre λ₂ = 2,21 e λ₃ = 0,83, e o critério de Kaiser dá dois (67% da variância). Mas Kaiser é um critério simples e criticado; faltou análise paralela e mostrar o *scree plot*.

**6.3. Porque dizes que as "loadings" são vetores próprios?**
As colunas da Tabela 7 têm norma ≈ 1 e são ortogonais, o que caracteriza vetores próprios. As correlações componente–variável (*loadings*) seriam o coeficiente × √λ: por exemplo, despesa–CP1 ≈ 0,90, e não 0,458.

**6.4. Para que serviu a PCA no R5?**
Só para visualização: o K-means foi feito sobre as 9 variáveis padronizadas, não sobre os *scores*. Por isso o objetivo de "representação mais simples" ficou parcialmente cumprido.

**6.5. A figura em duas dimensões chega para avaliar a separação?**
Não totalmente: os dois componentes explicam 67%, perde-se um terço da informação. Clusters que parecem separados em 2D podem sobrepor-se nas outras dimensões, e a silhueta (calculada nas 9 variáveis) é baixa.

---

## 7. Figura 1 e legenda trocada

**7.1. Como sabes que as legendas estão trocadas?**
Por duas pistas independentes: (1) pela Tabela 7, o lado direito do CP1 corresponde a rendimento, despesa, produtos e visitas elevados, e na figura é o "Cluster 3" (verde) que está aí, mas a Tabela 10 atribui esse perfil ao Cluster 1; (2) a proporção de pontos de cada cor (≈ 21%, 49%, 31%) corresponde aos tamanhos 62, 135 e 83.

**7.2. Qual dos dois está errado, a figura ou a tabela?**
Não sei: só sei que não podem estar os dois certos. Peço ao analista que verifique.

**7.3. Contaste os pontos?**
Não os contei um a um: estimei a proporção por cor (pixels) na imagem, por isso é uma estimativa aproximada, só de confirmação. A pista principal é a lógica entre a Tabela 7 e a Tabela 10.

**7.4. Que consequência prática tem?**
Quem lesse a figura podia dirigir as ações de retenção ao segmento errado.

---

## 8. Conclusões do R5 e abandono

**8.1. Porque dizes que o Cluster 3 só tem associação com o abandono?**
O teste confirma que o abandono difere entre clusters (*p* = 0,0055; V = 0,193). Mas 77% dos clientes do Cluster 3 não abandonaram, por isso pertencer-lhe não prevê o abandono individual. Não há sensibilidade nem AUC, e os intervalos de confiança do Cluster 3 [16,7; 30,7] e do Cluster 1 [3,5; 17,5] sobrepõem-se um pouco.

**8.2. O que significa "ordem temporal"?**
Não se sabe quando foram medidas visitas, produtos, satisfação e reclamações. Se foram medidos durante ou depois da decisão de sair, o perfil do Cluster 3 pode ser consequência do abandono, não causa.

**8.3. Porque trocarias "demonstra" por "sugere"?**
Porque o resultado é uma associação transversal, sem validação preditiva nem controlo de outros fatores.

**8.4. Porque dizes que "valor do cliente" é uma inferência?**
Rendimento do cliente e despesa não são necessariamente o valor para a empresa (receita, margem, CLV). Além disso o R5 não define se a despesa é na empresa.

**8.5. O que significa circularidade na descrição dos clusters?**
Os clusters foram formados com as variáveis que depois os descrevem; por isso é natural que sejam muito diferentes. A Tabela 10 só mostra médias, sem dispersão, e não serve como validação.

**8.6. E as "diferenças em grupo etário, plano e pagamento"?**
O R5 afirma-as sem tabela nem teste. O grupo etário deriva da idade (já usada) e o plano não tinha relação com o abandono (*p* = 0,994). Por isso digo que não têm suporte, não que sejam falsas.

---

## 9. Classificação de novos clientes (pergunta central para a professora)

**9.1. Porque dizes que o R5 não responde ao objetivo de classificar novos clientes?**
Não apresenta uma regra de atribuição (centróides e parâmetros de padronização), nenhum classificador supervisionado e nenhuma validação em dados não usados. E a eliminação de casos não se aplica a um cliente novo.

**9.2. Qual é o problema das variáveis usadas?**
Antiguidade, visitas, despesa, produtos, satisfação e reclamações acumulam-se com o tempo: um cliente recém-chegado ainda não as tem. Por isso um cliente novo tenderia a parecer-se com o Cluster 2 (menor antiguidade e menos visitas) só por ser recente. É uma inferência minha, não um cálculo.

**9.3. Como construirias esse sistema?**
Um modelo supervisionado (multinomial, árvore de decisão) com variáveis disponíveis à entrada (sociodemográficas, canal, plano), treinado com os segmentos como alvo e avaliado por validação cruzada. A regra do centróide mais próximo só serve se as variáveis existirem no momento da classificação.

**9.4. Como avaliarias esse modelo?**
Em dados que não serviram para o construir (treino/teste ou validação cruzada), com matriz de confusão, sensibilidade e especificidade (ou AUC, se for risco de abandono). Com 16,7% de abandono a exatidão sozinha engana: um modelo que previsse sempre "não abandona" teria 83% de acertos.

**9.5. A amostra chega para isso?**
Com 300 clientes e 50 abandonos é pouco para modelos com muitos preditores. Convém aumentar a amostra ou limitar o número de variáveis.

---

## 10. Recomendações

**10.1. Porque recomendas um piloto com grupo de controlo?**
Para testar se agir sobre o Cluster 3 reduz mesmo o abandono. Sem controlo não se distingue o efeito da ação do que aconteceria de qualquer forma.

**10.2. Concordas com a prioridade de retenção no Cluster 3?**
Como hipótese sim, desde que validada em piloto: é onde o abandono observado é maior. Não como certeza.

**10.3. E com acompanhar o método de pagamento?**
Aceito como monitorização, não como fator comprovado, dada a ausência de significância.

**10.4. O que dirias à administração hoje?**
Não usar o R5 como regra operacional; exigir correções e análises de robustez; encomendar um modelo para novos clientes; e testar a retenção num piloto.

---

## 11. Perguntas difíceis (sobre o teu próprio trabalho)

**11.1. Em que é que a tua avaliação pode estar errada?**
Trabalhei só com o relatório, sem os dados. Os 6 abandonos nos 20 excluídos resultam de dedução com taxas arredondadas; a troca de legendas assenta numa lógica forte mas uma contagem aproximada; e a ideia do cliente novo é uma inferência. São indícios fortes, não prova; recomendo que o analista os confirme.

**11.2. Tens bibliografia que sustente isto?**
Sim: Kaufman e Rousseeuw (1990) para a interpretação da silhueta; Kaiser (1960) e Horn (1965) para o número de componentes; Little e Rubin (2019) para dados em falta; Wilson (1927) para os intervalos de confiança. (Confirma que citas no texto as referências que listas.)

**11.3. Não estás a ser demasiado duro com o analista?**
Não: reconheço os pontos fortes e distingo o que é erro (padronização, V da Região, legendas) do que é falta de justificação (*k*, dados em falta) e do que é extrapolação (método de pagamento, "demonstra"). Cada crítica tem evidência e proposta de melhoria.

**11.4. Qual é o erro mais grave do R5, na tua opinião?**
Duas coisas, conforme a perspetiva. Conceptualmente, a afirmação errada de que padronizar protege dos extremos. Para a decisão da empresa, a ausência de qualquer resposta ao objetivo de classificar novos clientes.

**11.5. Se só pudesses corrigir uma coisa no R5, qual seria?**
Construir e validar um modelo para classificar novos clientes, porque é o objetivo da empresa que ficou por tratar.

---

## 12. Como responder se não souberes

- **"Não tenho essa informação, porque trabalhei só com o relatório. O que faria é…"** e diz o procedimento.
- **Não inventes números.** Se te perguntarem algo que não está nos teus anexos, diz que teria de recalcular.
- **Distingue sempre**: o que **recalculei** (certo), o que **deduzi** (forte, mas aproximado) e o que é **opinião técnica** (justificada, mas discutível).
- Se a professora discordar de um ponto, reconhece-o e explica em que pressuposto assenta a tua posição: "Se considerarmos X, então…".
