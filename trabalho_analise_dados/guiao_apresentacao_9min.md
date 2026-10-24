# Guião da apresentação (≈ 9 min), com base no teu PowerPoint

Cada bloco corresponde a um slide do teu ficheiro `Apresentação.pptx`. Usa-o como apoio: diz com as tuas palavras e não leies os slides.

## Slide 1: Capa (0:00–0:15)

Bom dia. Chamo-me Marco Martins e vou apresentar a avaliação crítica do relatório R5, de análise e segmentação de clientes, que fiz como consultor independente.

*(25 palavras)*

## Slide 2: Questão (0:15–1:00)

A empresa quer três coisas: conhecer o perfil dos clientes, identificar segmentos distintos e dispor de um sistema para classificar novos clientes. Antes de usar os resultados do analista, pediu uma avaliação independente. A questão central é esta: os resultados e as conclusões do R5 constituem uma base adequada para apoiar a segmentação dos clientes e a classificação de novos clientes? Adianto já a resposta: não, por ora. O R5 é um bom ponto de partida, mas só serve como hipótese de trabalho a validar.

*(85 palavras)*

## Slide 3: Avaliação do R5 (1:00–1:50)

Avaliei o R5 segundo os três critérios do enunciado. A adequação metodológica e a qualidade da análise têm apreciação parcial: as escolhas são razoáveis e os cálculos de base coerentes, mas há um erro conceptual, uma figura inconsistente e interpretações mais fortes do que a evidência. A validade das conclusões é insuficiente: das quatro que sustentam a decisão, só uma é suportada, e falta a classificação de novos clientes. Não reproduzi a análise: recalculei os números publicados, e as verificações estão no anexo.

*(83 palavras)*

## Slide 4: Critério A: adequação metodológica (1:50–3:15)

Na adequação metodológica, quatro pontos. Primeiro, o analista eliminou 20 clientes com valores em falta. É aceitável, mas só é inofensivo se a falta for aleatória, e isso não foi testado. Pelas taxas de abandono por cluster deduz-se que nesses 20 há 6 abandonos, 30%, contra 15,7% nos restantes; com p de 0,12 não é conclusivo, mas é um alerta. Segundo, ordinais e contagens foram tratadas como contínuas. Terceiro, o erro mais claro: o relatório diz que padronizar protege o K-means dos valores extremos. Não protege. O z-score é linear, como passar de metros para centímetros: os extremos continuam a 3,7 desvios-padrão e o K-means continua sensível a eles. Quarto, quatro variáveis de valor correlacionadas, com r até 0,84, pesam mais na distância, e não há inicializações nem semente, pelo que a análise não é reprodutível.

*(136 palavras)*

## Slide 5: Escolha do número de clusters (3:15–4:10)

A silhueta é máxima com k igual a 2, 0,353, e o analista escolheu k igual a 3, 0,325, por ser mais interpretável. É legítimo e foi transparente, mas usou um só índice, sem estabilidade, e todas as silhuetas ficam entre 0,21 e 0,35, estrutura fraca. Com k igual a 4 o valor é quase igual, e a figura do relatório sugere quatro nuvens. Por isso, dizer que os segmentos são distintos é demasiado forte.

*(75 palavras)*

## Slide 6: Critério B: erros e inconsistências (4:10–5:20)

Na qualidade da análise, encontrei erros verificáveis. O V de Cramér da Região está errado: a raiz de 1,364 sobre 300 dá 0,067 e não 0,039. Os valores próprios somam 9,033 em vez de 9. As loadings são, na verdade, vetores próprios. E o cluster 3 é descrito como mais velho, mas tem 47,9 anos, como o cluster 1. O mais grave está na figura: o cluster 3, a verde, está no lado direito da primeira componente, com rendimento e despesa elevados, mas a Tabela 10 atribui esse perfil ao cluster 1. As proporções de pontos, 22, 48 e 30 por cento, indicam que as legendas dos clusters 1 e 3 estão trocadas, na figura ou na tabela. Quem lesse a figura podia dirigir a retenção ao segmento errado.

*(129 palavras)*

## Slide 7: Interpretações que vão além da evidência (5:20–6:15)

Há interpretações que vão além da evidência. O valor do cliente é inferido do rendimento e da despesa, que não medem o valor para a empresa. Os clusters são descritos com as variáveis que os formaram, por isso as diferenças são grandes por construção. E o método de pagamento, com p de 0,065, não é significativo, mas é apresentado como fator relevante, enquanto a fidelização e o perfil, com p de 0,088 e 0,090, são ignorados. É uma hipótese a testar, não uma conclusão.

*(84 palavras)*

## Slide 8: Critério C: validade das conclusões (6:15–7:25)

Na validade das conclusões, analisei as quatro que sustentam a decisão. Três segmentos distintos: parcialmente suportada. A única suportada é que o cluster 3 tem maior abandono, 23% contra 8,1% e 9,6%, com p de 0,0055, que confirmei. Mas é associação, não previsão: 77% do cluster 3 não abandonou, não há AUC, os intervalos de confiança sobrepõem-se um pouco, como se vê no gráfico, e não se sabe quando foram medidas as variáveis. Por isso, demonstra devia ser sugere. As outras duas, diferenças entre clusters em variáveis categóricas e método de pagamento como fator de retenção, não têm suporte.

*(99 palavras)*

## Slide 9: Resposta ao problema da empresa (7:25–8:15)

Quanto ao problema da empresa: o perfil dos clientes, em grande parte, com reservas; os segmentos distintos, só parcialmente; e classificar novos clientes, não. Não há centróides nem parâmetros de padronização, classificador ou validação, e a eliminação de casos não se aplica a clientes novos. Além disso, as variáveis usadas, como antiguidade ou visitas, acumulam-se com o tempo e não existem à entrada: um cliente recém-chegado tenderia a parecer-se com o cluster 2 só por ser recente, o que é uma inferência minha, não um cálculo.

*(86 palavras)*

## Slide 10: Recomendações e conclusão (8:15–8:50)

Recomendo quatro coisas à administração. Não adotar o R5 como regra operacional, usando-o como hipótese de trabalho. Exigir as correções e análises de robustez. Encomendar um modelo para classificar novos clientes, testado em dados não usados na sua construção. E testar a retenção do cluster 3 num piloto com grupo de controlo. Em conclusão, o R5 descreve bem os clientes e mostra uma associação com o abandono, mas, na forma atual, não é uma base adequada para decidir: precisa de correções, robustez e de um modelo preditivo.

*(87 palavras)*

## Slide 11: Fim (8:50–9:00)

Muito obrigado. Fico disponível para perguntas.

*(6 palavras)*

---
Total: 895 palavras. A cerca de 115 palavras por minuto, dá ≈ 7.8 min.
