# Guião do vídeo (≈ 9 min) e preparação para a discussão

Slides de apoio: `slides_video.pptx` (8 slides). Ritmo: ~130 palavras/minuto. Grava com o ecrã a mostrar os slides e adapta as frases ao teu estilo: tens de as conseguir dizer sem ler.

## Guião

**Slide 1: Questão central (0:00–0:50)**
Bom dia. Fui contratado como consultor independente para avaliar o relatório R5, em que o analista segmenta 300 clientes e pretende apoiar a classificação de novos clientes. A questão central é: estes resultados são uma base adequada para segmentar e classificar? A minha resposta é: *ainda não*. É um bom ponto de partida, mas há falhas metodológicas, inconsistências e uma lacuna importante: a classificação de novos clientes nunca é abordada.

**Slide 2: Visão geral (0:50–1:30)**
Avaliei seis etapas. Dados e bivariada, parcialmente adequadas; PCA, adequada com falhas; K-means, insuficiente; a ligação ao abandono é o resultado mais sólido, mas com ressalvas; e a classificação de novos clientes não está abordada. Não reproduzi a análise: verifiquei a consistência interna dos números publicados.

**Slide 3: Dados e bivariada (1:30–3:00)**
Os valores em falta foram tratados por eliminação de casos, o que é aceitável com 6,7% de perdas, mas só se a falta for aleatória, o que não foi testado. Pelas taxas de abandono por cluster consegue deduzir-se que os 20 clientes excluídos têm cerca de 30% de abandono, contra 15,7% nos restantes. Não é conclusivo, mas é um alerta. Os valores extremos de rendimento e despesa, a mais de 3,7 desvios-padrão, não são tratados, e variáveis ordinais e de contagem são tratadas como contínuas. Na bivariada, o «valor do cliente» é inferido do rendimento do cliente, que não é o valor para a empresa. Recalculei a Tabela 5 e o V de Cramér da Região está errado: 0,067 e não 0,039. E o método de pagamento, com p = 0,065, não é significativo, mas é apresentado como fator relevante; é uma hipótese, não uma conclusão.

**Slide 4: PCA (3:00–4:00)**
Dois componentes pelo critério de Kaiser, com 67% da variância, é uma decisão defensável. Mas os valores próprios somam 9,033, quando deviam somar 9, e as percentagens somam 100,08%. Os «loadings» da Tabela 7 são vetores próprios, não correlações; a interpretação é seletiva e os rótulos «valor» e «modernização» são interpretações. Além disso, a PCA não entra na segmentação.

**Slide 5: K-means (4:00–6:00)**
É a parte mais frágil. Primeiro, o relatório diz que a padronização protege contra valores extremos. Está errado: é uma transformação linear, os extremos mantêm-se e o K-means é sensível a eles. O cluster de «elevado valor» pode estar a captar a cauda direita. Segundo, a escolha de k: a silhueta é máxima com k = 2 e escolhe-se k = 3 por interpretabilidade. É legítimo, mas todas as silhuetas estão entre 0,21 e 0,35, estrutura fraca, e isso não é dito nas conclusões. Não há estabilidade nem outros critérios, e k = 4 é quase equivalente. Por fim, os clusters são descritos só com médias e com as mesmas variáveis que os formaram: é circular.

**Slide 6: Figura 1 (6:00–7:00)**
Na figura do relatório, o «Cluster 3», a verde, está do lado direito da primeira componente, ou seja, rendimento e despesa elevados, mas a Tabela 10 diz que esse é o Cluster 1. As proporções dos pontos, cerca de 22%, 48% e 30%, confirmam que as legendas 1 e 3 estão trocadas. Quem lesse a figura dirigiria a retenção ao segmento errado. Repare-se também que o grupo azul parece ter dois sub-grupos, sugerindo k = 4.

**Slide 7: Abandono e novos clientes (7:00–8:15)**
O abandono por cluster é o resultado mais sólido: 8,1%, 9,6% e 23,0%, qui-quadrado 10,41, p = 0,0055. Mas é uma associação: 77% do Cluster 3 não abandonou, não há AUC e não sabemos quando foram medidas as variáveis. «Demonstra» é forte; «sugere» seria mais correto. E a afirmação de diferenças em variáveis categóricas não tem tabela nem teste. Quanto à classificação de novos clientes, não há regra, classificador nem validação, e as variáveis usadas, como antiguidade, visitas e reclamações, não existem quando o cliente chega: seria quase sempre atribuído ao Cluster 2.

**Slide 8: Recomendações (8:15–9:30)**
Recomendo à administração: usar o relatório como hipótese e não como regra; exigir as correções; pedir análises de robustez; encomendar um modelo supervisionado para novos clientes e outro para risco de abandono, com validação cruzada; testar a retenção num piloto com grupo de controlo; e melhorar os dados. Em resumo: um bom ponto de partida, mas ainda não uma base adequada para decidir. Obrigado.

## Perguntas prováveis na discussão

1. **Porque dizes que k = 3 não é indefensável, mas insuficiente?** Critérios de negócio são legítimos; o problema é haver um só critério, silhuetas fracas, sem estabilidade e k = 4 quase equivalente.
2. **Porque é errado dizer que a padronização protege de outliers?** O z-score é linear (subtrai a média, divide pelo DP): a forma da distribuição e a distância relativa dos extremos mantêm-se; a soma de quadrados do K-means continua a ser dominada por eles.
3. **Como sabes que a legenda está trocada e não a tabela?** Não sei qual dos dois está errado; sei que são incompatíveis. Os sinais (CP1 = valor, Tabela 7) e as proporções de pontos (≈ 22/48/30%) apontam para a figura; peço verificação.
4. **Como deduziste os 6 abandonos nos 20 excluídos?** Taxa × n por cluster: 5 + 8 + 31 = 44 abandonos em 280; total 50, logo 6 nos 20 excluídos. Fisher p ≈ 0,12: indício, não prova.
5. **Porque o abandono por cluster é válido mas não chega?** O teste mostra associação (p = 0,0055). Para decidir é preciso previsão (AUC, sensibilidade) e ordem temporal.
6. **Como classificarias novos clientes?** Modelo supervisionado (multinomial/árvore) com variáveis disponíveis à entrada (sociodemográficas, canal, plano), validação cruzada; regra do centróide mais próximo só se as variáveis existirem.
7. **Porque o V de Cramér da Região está errado?** V = √(χ²/(n·min(r−1,c−1))) = √(1,364/300) = 0,067. Sete das oito linhas conferem.
8. **Kaiser é mau?** É simples mas criticado; aqui a decisão é razoável (quebra entre λ₂ e λ₃), mas faltou análise paralela e mostrar o scree plot.
9. **Isto é só crítica?** Não: reconheço os pontos fortes (coerência das médias, abandono por cluster, transparência sobre k = 2) e proponho alternativas.

## Antes de entregar

- Substitui `[Nome]` e `[N.º]` na capa do relatório e nos slides.
- Confirma as referências com a bibliografia da UC.
- **Garante que consegues defender cada número**: repete as verificações com `verificacoes.py` (Anexo B).
- O vídeo tem de ser gravado por ti (máx. 10 min); entrega relatório PDF e vídeo no Moodle até 26/10/2026, 23h59.
