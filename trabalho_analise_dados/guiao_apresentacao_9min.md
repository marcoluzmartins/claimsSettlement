# Guião da apresentação (≈ 9 min), com base no teu PowerPoint

Cada bloco corresponde a um slide do teu ficheiro `Apresentação.pptx`. Usa-o como apoio: diz com as tuas palavras e não leies os slides.

## Slide 1: Capa (0:00–0:15)

Bom dia. Chamo-me Marco Martins e vou apresentar a avaliação crítica do relatório R5, de análise e segmentação de clientes, que fiz como consultor independente.

*(25 palavras)*

## Slide 2: Questão (0:15–1:00)

A empresa quer três coisas: conhecer o perfil dos clientes, identificar segmentos distintos e dispor de um sistema para classificar novos clientes. Antes de usar os resultados do analista, pediu uma avaliação independente. A questão central é esta: os resultados e as conclusões do R5 constituem uma base adequada para apoiar a segmentação dos clientes e a classificação de novos clientes? Adianto já a resposta: não, por ora. O R5 é um bom ponto de partida, mas só serve como hipótese de trabalho a validar.

*(85 palavras)*

## Slide 3: Avaliação do R5 (1:00–1:50)

Avaliei o R5 segundo os três critérios do enunciado. Na adequação das opções metodológicas, a apreciação é parcial: as escolhas são razoáveis, mas sem verificar pressupostos nem testar a robustez, e há uma justificação errada. Na qualidade da análise e da interpretação, também parcial: os cálculos de base são coerentes, mas encontrei erros pontuais, uma figura inconsistente com a tabela e interpretações mais fortes do que a evidência. Na validade das conclusões e recomendações, a apreciação é insuficiente: das quatro conclusões que sustentam a decisão, só uma é suportada, e falta tratar a classificação de novos clientes. Não reproduzi a análise: recalculei os números publicados para verificar a coerência interna, e as verificações estão no anexo do relatório.

*(118 palavras)*

## Slide 4: Critério A: adequação metodológica (1:50–3:15)

Começando pela adequação metodológica, quatro pontos. Primeiro, os valores em falta: o analista eliminou 20 clientes, 6,7% da amostra. É aceitável pela dimensão, mas só é inofensivo se a falta de dados for aleatória, e isso não foi testado. Pelas taxas de abandono que o relatório dá por cluster, deduz-se que nesses 20 clientes há 6 abandonos, 30%, contra 15,7% nos restantes. Com o teste de Fisher, p de 0,12, não é conclusivo, mas é um sinal de alerta. Segundo, as variáveis ordinais e de contagem foram tratadas como contínuas, e o Pearson foi aplicado a variáveis assimétricas. Terceiro, e é o erro conceptual mais claro: o relatório diz que padronizar as variáveis protege o K-means dos valores extremos. Não protege. O z-score é uma transformação linear, como passar de metros para centímetros: os extremos continuam a 3,7 desvios-padrão e o K-means, que usa distâncias ao quadrado, continua sensível a eles. Quarto, quatro variáveis de valor estão correlacionadas, com r até 0,84, e por isso pesam mais na distância; e o relatório não indica inicializações nem semente, o que impede reproduzir a análise.

*(183 palavras)*

## Slide 5: Escolha do número de clusters (3:15–4:10)

Na escolha do número de clusters, o coeficiente de silhueta é máximo com k igual a 2, 0,353, e o analista escolheu k igual a 3, 0,325, por ser mais interpretável. Escolher pelo negócio é legítimo, e o analista foi transparente. Mas usou um só índice, sem análise de estabilidade, e, como se vê no gráfico, todas as silhuetas ficam entre 0,21 e 0,35, o que indica estrutura fraca. Com k igual a 4 o valor é quase igual, 0,319, e a própria figura do relatório sugere quatro nuvens. Por isso, dizer que os segmentos são distintos é demasiado forte para os dados.

*(103 palavras)*

## Slide 6: Critério B: erros e inconsistências (4:10–5:20)

Quanto à qualidade da análise, encontrei erros verificáveis. O V de Cramér da Região está errado: a raiz de 1,364 a dividir por 300 dá 0,067 e não 0,039; as outras sete linhas da tabela batem certo. Os valores próprios somam 9,033, quando numa PCA com nove variáveis deviam somar 9. As loadings da Tabela 7 são, na verdade, vetores próprios. E o cluster 3 é descrito como mais velho, mas tem 47,9 anos, praticamente igual ao cluster 1, com 47,2. O problema mais grave está na figura do relatório, aqui anotada. O cluster 3, a verde, está no lado direito da primeira componente, ou seja, com rendimento, despesa e visitas elevados, mas a Tabela 10 atribui esse perfil ao cluster 1. As proporções de pontos, cerca de 22, 48 e 30 por cento, indicam que as legendas dos clusters 1 e 3 estão trocadas, na figura ou na tabela. Quem lesse a figura podia dirigir a retenção ao segmento errado.

*(161 palavras)*

## Slide 7: Interpretações que vão além da evidência (5:20–6:15)

Há ainda interpretações que vão além da evidência. O valor do cliente é inferido do rendimento e da despesa, que não medem o valor para a empresa; seria preciso receita ou margem. Os clusters são descritos com as mesmas variáveis que os formaram, por isso as diferenças são grandes por construção, e só se apresentam médias, sem dispersão. O método de pagamento, com p de 0,065, não é significativo, mas o relatório diz que pode ser um fator relevante para a retenção, enquanto a fidelização e o perfil, com p de 0,088 e 0,090, não recebem o mesmo tratamento. É uma hipótese a testar, não uma conclusão. Por fim, os rótulos valor e modernização dos componentes são leituras, e a interpretação é seletiva.

*(123 palavras)*

## Slide 8: Critério C: validade das conclusões (6:15–7:25)

Passando à validade das conclusões, analisei as quatro que sustentam a decisão. A existência de três segmentos distintos é só parcialmente suportada, pelas razões que vimos. A única suportada é que o cluster 3 tem maior abandono, 23% contra 8,1% e 9,6%, com p de 0,0055; refiz o teste e confirma-se. Mas é uma associação, não uma previsão: 77% dos clientes do cluster 3 não abandonaram, não há sensibilidade nem AUC, os intervalos de confiança do cluster 3 e do cluster 1 sobrepõem-se um pouco, como se vê no gráfico, e não se sabe quando foram medidas as variáveis, que podem refletir o próprio abandono. Por isso, demonstra devia ser sugere. As duas últimas conclusões não têm suporte: as diferenças entre clusters em variáveis categóricas não têm tabela nem teste, e o método de pagamento não é significativo.

*(138 palavras)*

## Slide 9: Critério C (slide repetido) (7:25–8:15)

[ATENÇÃO: este slide está repetido do anterior. Substitui-o pelo quadro «Os resultados respondem ao problema da empresa?» e usa este texto.] Voltando ao problema da empresa. Conhecer o perfil dos clientes: em grande parte sim, com reservas por causa dos dados em falta e dos extremos não tratados. Identificar segmentos distintos: só parcialmente, porque a estrutura é fraca e faltam validações. E classificar novos clientes: não. O relatório não apresenta centróides nem parâmetros de padronização, nenhum classificador, nenhuma validação, e a eliminação de casos não se pode aplicar a novos clientes. Além disso, as variáveis usadas, como antiguidade, visitas ou reclamações, acumulam-se com o tempo e não existem à entrada: um cliente recém-chegado tenderia a parecer-se com o cluster 2 só por ser recente, o que é uma inferência minha, não um cálculo. E, com 50 abandonos, a amostra limita modelos mais complexos.

*(143 palavras)*

## Slide 10: Recomendações e conclusão (8:15–8:50)

Recomendo à administração quatro coisas. Não adotar o R5 como regra operacional, usando-o como hipótese de trabalho. Exigir as correções, da figura, da afirmação sobre os extremos, do V de Cramér e dos valores próprios, e análises de robustez. Encomendar um modelo para classificar novos clientes, testado em dados não usados na sua construção. E testar a retenção do cluster 3 num piloto com grupo de controlo. Em conclusão, o R5 descreve bem os clientes e mostra uma associação com o abandono, mas, na forma atual, não é uma base adequada para decidir: precisa de correções, de análises de robustez e de um modelo preditivo.

*(105 palavras)*

## Slide 11: Fim (8:50–9:00)

Muito obrigado. Fico disponível para perguntas.

*(6 palavras)*

---
Total: 1190 palavras. A cerca de 115 palavras por minuto, dá ≈ 10.3 min.
