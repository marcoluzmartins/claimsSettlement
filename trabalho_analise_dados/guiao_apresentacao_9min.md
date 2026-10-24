# Guião da apresentação (≈ 9 min), com base no teu PowerPoint

Cada bloco corresponde a um slide do teu ficheiro `Apresentação.pptx`. Usa-o como apoio: diz com as tuas palavras e não leies os slides.

## Slide 1: Capa (0:00–0:15)

Bom dia. Eu sou o Marco Martins e vou apresentar a avaliação que fiz ao relatório R5, de análise e segmentação de clientes, no papel de consultor independente.

*(28 palavras)*

## Slide 2: Questão (0:15–1:00)

Vamos começar pelo problema. A empresa quer conhecer melhor os clientes, perceber que grupos existem e ter uma forma de classificar os clientes novos. Antes de usar o trabalho do analista, pediu uma opinião independente. E a pergunta é simples: este relatório dá uma base adequada para segmentar e para classificar novos clientes? Digo já a minha resposta: ainda não. É um bom ponto de partida, mas é só isso, uma hipótese de trabalho que precisa de ser validada.

*(79 palavras)*

## Slide 3: Avaliação do R5 (1:00–1:50)

Para chegar a esta resposta, olhei para o relatório segundo os três critérios do enunciado. Na parte metodológica e na qualidade da análise, a apreciação é parcial. As escolhas são razoáveis e as contas de base estão certas, mas encontrei um erro de conceito, uma figura que não bate com a tabela e algumas interpretações que vão mais longe do que os dados permitem. Nas conclusões, a apreciação é insuficiente: das quatro que sustentam a decisão, só uma está realmente suportada, e falta tratar a classificação de novos clientes. Não repeti a análise: recalculei os números publicados, e isso está no anexo.

*(102 palavras)*

## Slide 4: Critério A: adequação metodológica (1:50–3:15)

Na parte metodológica, quero destacar quatro coisas. A primeira são os valores em falta. O analista tirou 20 clientes da análise. Com tão poucos, é aceitável, mas só se a falta de dados for ao acaso, e isso ninguém verificou. E há um sinal de alerta: pelas taxas de abandono que o relatório dá, percebe-se que nesses 20 clientes houve 6 abandonos, ou seja, 30%, contra 15,7% nos outros. Não prova nada, pode ser acaso, mas devia ter sido investigado. A segunda é o erro mais claro. O relatório diz que padronizar as variáveis protege o K-means dos valores extremos. Isso não é verdade. Padronizar é só mudar a escala, é como passar de metros para centímetros: o cliente com o rendimento mais alto continua a ser o mais alto, e continua a puxar os grupos. E a terceira: quatro variáveis ligadas ao valor estão muito correlacionadas e acabam por pesar a dobrar, e o relatório não diz que sementes usou, por isso ninguém consegue repetir os resultados.

*(168 palavras)*

## Slide 5: Escolha do número de clusters (3:15–4:10)

Passemos à escolha do número de grupos. Olhando para o gráfico, a silhueta é mais alta com dois grupos, e o analista escolheu três, porque lhe pareceram mais fáceis de interpretar. Não é uma decisão errada, e o analista foi transparente. O problema é que só usou este critério, e não testou se os grupos se mantêm estáveis. E repare-se: todos os valores estão entre 0,21 e 0,35, o que, segundo a literatura, quer dizer estrutura fraca. Com quatro grupos o resultado é quase igual, e a própria figura do relatório parece mostrar quatro nuvens. Por isso, dizer que os segmentos são distintos é forte demais.

*(106 palavras)*

## Slide 6: Critério B: erros e inconsistências (4:10–5:20)

Na qualidade da análise, encontrei erros que se confirmam com uma simples conta. O V de Cramér da região devia ser 0,067, e não 0,039. Os valores próprios somam 9,033, quando tinham de somar 9. O que o relatório chama de loadings são, na verdade, vetores próprios. E o terceiro grupo é dado como mais velho, mas tem a mesma idade do primeiro. Mas o que mais me preocupou foi a figura. Vejam: o grupo a verde está do lado direito, onde ficam os clientes com mais rendimento, mais despesa e mais visitas. Só que, na tabela, esse perfil pertence ao Cluster 1, e não ao 3. Pela proporção de pontos de cada cor, cerca de 22%, 48% e 30%, tudo indica que as legendas do 1 e do 3 estão trocadas, na figura ou na tabela. E isto importa: quem lesse a figura podia mandar as ações de retenção para o grupo errado.

*(154 palavras)*

## Slide 7: Interpretações que vão além da evidência (5:20–6:15)

Há ainda algumas interpretações que dizem mais do que os dados mostram. Por exemplo, chama-se valor do cliente ao rendimento e à despesa. Mas o rendimento de um cliente não é o valor que ele tem para a empresa, isso seria receita ou margem. Depois, os grupos são descritos com as variáveis que os criaram, por isso é natural que sejam diferentes. E o método de pagamento: o resultado não é significativo, com p de 0,065, mas o relatório sugere que pode ser um fator importante para a retenção, enquanto a fidelização e o perfil, com valores quase iguais, nem são mencionados. Para mim, isso é uma pista para investigar, não uma conclusão.

*(113 palavras)*

## Slide 8: Critério C: validade das conclusões (6:15–7:25)

Vamos então às conclusões. Olhei para as quatro que sustentam a decisão. A existência de três segmentos distintos fica só parcialmente suportada, pelas razões que vimos. A única que se confirma é que o terceiro grupo abandona mais: 23%, contra cerca de 8 e 10%. Refiz o teste e confere. Mas atenção, isto é uma associação, não uma previsão. Quase 8 em cada 10 clientes desse grupo não abandonou. E os intervalos de confiança, que se veem no gráfico, sobrepõem-se um pouco. Além disso, não sabemos quando foram medidas as variáveis, e podem já refletir o abandono. Por isso, em vez de demonstra, o relatório devia dizer sugere. As outras duas conclusões, as diferenças entre grupos nas variáveis categóricas e o papel do método de pagamento, não têm suporte nos resultados.

*(131 palavras)*

## Slide 9: Resposta ao problema da empresa (7:25–8:15)

Então, voltando à empresa, o que é que o relatório resolve? Perceber o perfil dos clientes: em grande parte, sim, com as reservas que já referi. Identificar segmentos distintos: só em parte. E classificar novos clientes: não. O relatório não deixa uma regra para atribuir um cliente a um grupo, não tem nenhum modelo, não testa nada em dados novos, e apagar clientes com dados em falta não é opção quando chega um cliente novo. E há uma questão de fundo: os grupos foram feitos com informação que só existe passado algum tempo, como a antiguidade ou as visitas. Um cliente que acabou de chegar ainda não a tem, e tenderia a parecer-se com o grupo dos mais recentes só por isso. Isto é um raciocínio meu, não um cálculo.

*(130 palavras)*

## Slide 10: Recomendações e conclusão (8:15–8:50)

Em resumo, o que recomendo à administração? Que não use o relatório como regra, mas como ponto de partida. Que peça as correções e uma análise de robustez. Que encomende um modelo para classificar clientes novos, testado em dados que não serviram para o construir. E que teste a retenção do terceiro grupo num piloto, com grupo de controlo. A minha conclusão é esta: o R5 descreve bem os clientes e identifica uma associação interessante com o abandono, mas, tal como está, não é uma base suficiente para decidir.

*(89 palavras)*

## Slide 11: Fim (8:50–9:00)

Obrigado pela atenção. Fico disponível para as vossas perguntas.

*(9 palavras)*

---
Total: 1109 palavras. Ritmo natural de fala (≈ 130 palavras/min): ≈ 8.5 min. A falar mais devagar (≈ 115 palavras/min): ≈ 9.6 min. Cronometra uma leitura em voz alta.
