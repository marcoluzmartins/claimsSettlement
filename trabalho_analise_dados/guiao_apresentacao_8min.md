# Guião da apresentação (≈ 8 min)

Cada bloco corresponde a um slide do teu PowerPoint. Os tempos são indicativos (≈ 125 palavras/min).

## Slide 1: Capa (0:00–0:13)

Bom dia. Eu sou o Marco Martins e vou apresentar a avaliação que fiz ao relatório R5, de análise e segmentação de clientes, no papel de consultor independente.

*(28 palavras)*

## Slide 2: Questão (0:13–0:48)

A empresa quer conhecer melhor a sua carteira de clientes, perceber que grupos existem e ter uma forma de classificar os clientes novos. Antes de usar o trabalho do analista, pediu uma opinião independente. A pergunta é simples: este relatório é uma base adequada para segmentar e classificar novos clientes? A minha resposta é: ainda não. É um bom ponto de partida, mas ainda só uma hipótese de trabalho a validar.

*(71 palavras)*

## Slide 3: Avaliação do R5 (0:48–1:35)

Avaliei o relatório segundo os três critérios do enunciado. Na parte metodológica e na qualidade da análise, a apreciação é parcial: as escolhas são razoáveis e os cálculos de base estão corretos, mas encontrei um erro de conceito, uma figura que não bate com a tabela e interpretações que vão mais longe do que os dados permitem. Nas conclusões, a apreciação é insuficiente: das quatro que sustentam a decisão, só uma está suportada, e falta a classificação de novos clientes, um dos três objetivos da empresa. Não repeti a análise: apenas recalculei os números publicados, que estão em anexo.

*(99 palavras)*

## Slide 4: Critério A: adequação metodológica (1:35–2:52)

Na parte metodológica, quero destacar quatro coisas. A primeira são os valores em falta. O analista eliminou 20 clientes. É aceitável, mas só se a falta de dados for ao acaso, e isso não foi verificado. E há um sinal de alerta: pelas taxas de abandono, percebe-se que nesses 20 clientes houve 6 abandonos, 30%, contra 15,7% nos restantes. Não prova nada, pode ser acaso, mas devia ter sido investigado. A segunda: variáveis ordinais e de contagem foram tratadas como contínuas. A terceira é o erro mais claro. O relatório diz que padronizar as variáveis protege o K-means dos valores extremos. Não é verdade. Padronizar é só mudar a escala, como passar de metros para centímetros: o cliente com o rendimento mais alto continua a puxar os grupos. E a quarta: quatro variáveis ligadas ao valor estão muito correlacionadas e pesam mais do que as outras, e o relatório não indica a semente usada, por isso ninguém repete os resultados.

*(160 palavras)*

## Slide 5: Escolha do número de clusters (2:52–3:34)

Passemos à escolha do número de grupos. A silhueta é mais alta com dois grupos, e o analista escolheu três porque lhe pareceram mais fáceis de interpretar. Não é uma decisão errada, mas só usou este critério e não testou se os grupos são estáveis. E todos os valores estão entre 0,21 e 0,35, o que é estrutura fraca. Com quatro grupos o resultado é praticamente igual, e a figura do relatório parece mostrar quatro nuvens. Por isso, dizer que os segmentos são distintos é forte demais.

*(87 palavras)*

## Slide 6: Critério B: erros e inconsistências (3:34–4:36)

Na qualidade da análise, encontrei erros que se confirmam com uma simples conta. O V de Cramér da região devia ser 0,067 e não 0,039. Os valores próprios somam 9,033 e deviam somar 9. O que o relatório chama de loadings são vetores próprios. E o terceiro grupo é dado como mais velho, mas tem a mesma idade do primeiro. O que mais me preocupou foi a figura: o grupo a verde está do lado direito, onde ficam os clientes com mais rendimento, despesa e visitas, mas na tabela esse perfil é do Cluster 1, não do 3. Pelas proporções de pontos, tudo indica que as legendas do 1 e do 3 estão trocadas, na figura ou na tabela. Quem lesse a figura podia mandar a retenção para o grupo errado.

*(131 palavras)*

## Slide 7: Interpretações que vão além da evidência (4:36–5:23)

Há ainda interpretações que dizem mais do que os dados mostram. Chama-se valor do cliente ao rendimento e à despesa, mas isso não é o valor para a empresa, que seria receita ou margem. Os grupos são descritos com as variáveis que os criaram, por isso é natural que sejam diferentes. E o método de pagamento não é significativo, com p de 0,065, mas o relatório sugere que pode ser um fator importante para a retenção, enquanto a fidelização e o perfil, com valores quase iguais, nem são mencionados. É uma pista a investigar, não uma conclusão.

*(97 palavras)*

## Slide 8: Critério C: validade das conclusões (5:23–6:17)

Quanto às conclusões, olhei para as quatro que sustentam a decisão. Os três segmentos distintos ficam só parcialmente suportados, pelas razões que vimos. A única que se confirma é que o terceiro grupo abandona mais: 23%, contra cerca de 8 e 10%. Refiz o teste e confere. Mas é uma associação, não uma previsão: quase 8 em cada 10 clientes desse grupo não abandonou, e os intervalos de confiança sobrepõem-se ligeiramente. Também não sabemos quando foram medidas as variáveis, e podem já refletir o abandono. Por isso, em vez de demonstra, o relatório devia dizer sugere. As outras duas, as diferenças em variáveis categóricas e o método de pagamento, não têm suporte.

*(112 palavras)*

## Slide 9: Resposta ao problema da empresa (6:17–7:14)

Voltando ao que a empresa pede: perceber o perfil dos clientes, em grande parte sim, com as reservas já referidas; identificar segmentos distintos, só em parte. E classificar novos clientes: não. O relatório não deixa uma regra para atribuir um cliente a um grupo, não tem nenhum modelo, não testa nada em dados novos, e apagar clientes com dados em falta não é opção quando chega um cliente novo. E há uma questão de fundo: os grupos foram feitos com informação que só existe passado algum tempo, como a antiguidade ou as visitas. Um cliente recém-chegado ainda não a tem, e tenderia a parecer-se com o grupo dos mais recentes só por isso. É um raciocínio meu, não um cálculo.

*(120 palavras)*

## Slide 10: Recomendações e conclusão (7:14–7:50)

Em resumo, recomendo que o relatório não seja usado como regra, mas como ponto de partida. São necessárias correções e uma análise de robustez, e um modelo para classificar clientes novos, testado em dados que não serviram para o construir. E que se teste a retenção do terceiro grupo com um grupo de controlo. Conclusão: bom ponto de partida, mas ainda não uma base adequada. Precisa de correções, robustez e de um modelo preditivo.

*(74 palavras)*

## Slide 11: Fim (7:50–7:53)

Obrigado pela atenção. Fico disponível para perguntas.

*(7 palavras)*

---
Total: 986 palavras. A 130 palavras/min: ≈ 7.6 min; a 120 palavras/min: ≈ 8.2 min.
