# Guião da apresentação (≈ 9 min)

Slides: `apresentacao_9min.pptx` (9 slides, com as notas do orador em cada um). Ritmo: ~125 palavras/minuto. Diz as frases com as tuas palavras; não leias os slides.

## Slide 1: Avaliação crítica do relatório R5

[0:00–0:45] Bom dia. Fui contratado como consultor independente para avaliar o relatório R5, em que um analista segmenta 300 clientes com PCA e K-means. A questão central é: estes resultados são uma base adequada para segmentar clientes e classificar novos clientes? A minha resposta é: não, por ora. Servem como hipótese de trabalho, mas há falhas metodológicas, inconsistências e uma lacuna importante: a classificação de novos clientes nunca é tratada.

*(70 palavras)*

## Slide 2: Como avaliei o R5

[0:45–1:30] Avaliei o R5 segundo os três critérios do enunciado. Na adequação metodológica e na qualidade da interpretação a apreciação é parcial: os cálculos de base são coerentes, mas há um erro conceptual, uma figura inconsistente e interpretações mais fortes do que a evidência. Na validade das conclusões é insuficiente: das quatro conclusões que sustentam a decisão, só uma é suportada. Não reproduzi a análise; recalculei os números publicados e anexei as verificações.

*(73 palavras)*

## Slide 3: Critério A: adequação metodológica

[1:30–3:00] Na parte metodológica, quatro pontos. Primeiro, os valores em falta: o analista apagou 20 clientes, o que é aceitável com 6,7% de perdas, mas só se a falta for aleatória, e isso não foi testado. Pelas taxas de abandono por cluster, que dão 5, 8 e 31 abandonos, deduz-se que esses 20 clientes têm 6 abandonos, 30%, contra 15,7% nos restantes. Não é conclusivo, com p de 0,12, mas é um alerta. Segundo, variáveis ordinais e de contagem tratadas como contínuas, com Pearson sobre variáveis assimétricas. Terceiro, a padronização: o relatório diz que protege dos valores extremos. É falso. O z-score é linear, os extremos continuam a 3,7 desvios-padrão e o K-means continua sensível a eles. Quarto, o K-means pesa mais as quatro variáveis de valor, que estão correlacionadas, e não indica inicializações nem semente.

*(136 palavras)*

## Slide 4: Escolha do número de clusters

[3:00–4:00] A silhueta é máxima com dois clusters, 0,353, e o analista escolhe três, 0,325, por ser mais interpretável. É um critério legítimo e o analista foi transparente. Mas há um só índice, nenhuma análise de estabilidade e todas as silhuetas, entre 0,21 e 0,35, indicam estrutura fraca. Com quatro clusters o valor é praticamente igual, 0,319, e a figura do próprio relatório mostra quatro nuvens. Por isso «distintos» é demasiado forte para os dados.

*(75 palavras)*

## Slide 5: Critério B: erros e inconsistências

[4:00–5:15] Na qualidade da análise, encontrei cinco problemas verificáveis. O V de Cramér da Região está errado: a raiz de 1,364 sobre 300 dá 0,067 e não 0,039. Os valores próprios somam 9,033 em vez de 9. As loadings da Tabela 7 são vetores próprios, não correlações. O cluster 3 é descrito como mais velho mas tem 47,9 anos, igual ao cluster 1. E o mais grave: na figura do relatório, o cluster 3, a verde, está do lado direito da primeira componente, ou seja, rendimento e despesa elevados, mas a tabela atribui esse perfil ao cluster 1. As proporções de pontos, 22, 48 e 30 por cento, confirmam que as legendas 1 e 3 estão trocadas. Quem lesse a figura dirigia a retenção ao segmento errado.

*(127 palavras)*

## Slide 6: Interpretações que vão além da evidência

[5:15–6:15] Há ainda interpretações que vão além da evidência. «Valor do cliente» é inferido do rendimento e da despesa, que não medem o valor para a empresa. Os clusters são descritos com as mesmas variáveis que os formaram: as diferenças são grandes por construção, e só se mostram médias, sem dispersão. O método de pagamento, com p de 0,065, não é significativo, mas o relatório diz que pode ser um fator relevante, enquanto a fidelização e o perfil, com p de 0,088 e 0,090, não recebem o mesmo tratamento. É uma hipótese a testar, não uma conclusão. E os rótulos dos componentes são leituras, e a interpretação é seletiva.

*(109 palavras)*

## Slide 7: Critério C: validade das conclusões

[6:15–7:30] Na validade das conclusões, analisei as quatro que sustentam a decisão. A existência de três segmentos distintos é só parcialmente suportada. A única suportada, como associação, é que o cluster 3 tem maior abandono, 23% contra 8 e 10 por cento, com p de 0,0055. Mas é associação, não previsão: 77% do cluster 3 não abandonou, não há AUC, os intervalos de confiança sobrepõem-se parcialmente e não se sabe quando foram medidas as variáveis. «Demonstra» devia ser «sugere». As outras duas, diferenças entre clusters em variáveis categóricas e o método de pagamento como fator de retenção, não têm suporte: não há tabelas nem testes, ou o teste não é significativo.

*(111 palavras)*

## Slide 8: Os resultados respondem ao problema da empresa?

[7:30–8:20] Face aos três objetivos da empresa: conhecer o perfil dos clientes, em grande parte sim, com reservas. Identificar segmentos distintos, só parcialmente. E classificar novos clientes, não: o relatório não apresenta centróides nem parâmetros de padronização, nenhum classificador, nenhuma validação, e a eliminação de casos não serve para novos clientes. Além disso, as variáveis usadas, como antiguidade, visitas e reclamações, acumulam-se com o tempo e não existem à entrada: um cliente recém-chegado tenderia a parecer-se com o cluster 2 só por ser recente, o que é uma inferência minha. E com 50 abandonos a amostra é pequena.

*(98 palavras)*

## Slide 9: Recomendações e conclusão

[8:20–9:00] Recomendo à administração: não adotar o R5 como regra operacional; exigir as correções e análises de robustez, como transformar as variáveis, testar outros valores de k e a estabilidade; encomendar um modelo supervisionado para novos clientes, validado em dados não usados; e testar a retenção do cluster 3 num piloto com grupo de controlo. Em conclusão, o R5 descreve bem os clientes e mostra uma associação com o abandono, mas não é, na forma atual, uma base adequada. Precisa de correções, robustez e de um modelo preditivo. Obrigado.

*(89 palavras)*

---
Total: 888 palavras ≈ 7.1 min a 125 palavras/minuto.
