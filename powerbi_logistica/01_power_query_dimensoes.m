// =====================================================================
// POWER QUERY (M) – LogiDistrib – as 9 tabelas do trabalho
//
// Como usar no Power BI Desktop:
//   1. Página Inicial > Transformar dados.
//   2. Nova origem > Consulta em branco > (Base) Editor avançado.
//   3. Para CADA bloco abaixo: apagar o texto, colar o bloco e dar à
//      consulta o nome indicado em "Consulta:".
//   4. Consultas stg_encomendas e stg_entregas: botão direito >
//      desmarcar "Ativar carregamento" (servem só de origem).
//
// Formatos confirmados nos 9 CSV (não alterar os ficheiros):
//   UTF-8 com BOM (Encoding=65001 trata o BOM) | separador vírgula |
//   sem aspas | fim de linha LF | decimais com PONTO | datas ISO
//   aaaa-mm-dd | sem nulos nem espaços sobrantes.
//   -> Todas as conversões usam a cultura "en-US": com a localidade
//      do Windows em PT, "59.94" seria lido como 5994 ou como erro.
//   -> "mes" (ex.: 2026-01) é TEXTO: não deixar o Power BI convertê-lo
//      em data.
// =====================================================================


// ---------------------------------------------------------------------
// Consulta: PastaDados   (texto – pasta com os CSV, com "\" no fim)
// ---------------------------------------------------------------------
"C:\Users\O_SEU_UTILIZADOR\Trabalho_PowerBI\dados\"


// ---------------------------------------------------------------------
// Consulta: dim_calendario      Grão: 1 linha por dia (642 dias)
// 01/01/2025 a 04/10/2026. dia_util = Sim/Não (seg–sex, sem feriados).
// ATENÇÃO: as encomendas só vão até 31/08/2026 -> o período comparável
// é 1 jan–31 ago de cada ano (ver coluna DAX "Em Periodo Comparavel").
// du_antes = nº de dias úteis ANTERIORES à data (exclui a própria data).
//   Dias úteis decorridos entre duas datas = du_antes(fim) - du_antes(início)
//   = nº de dias úteis em [início ; fim[   (= NETWORKDAYS - 1 do Excel).
//   O DAX não tem NETWORKDAYS: é por isto que se usa este contador.
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "dim_calendario.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"data", type date}, {"ano", Int64.Type}, {"mes_num", Int64.Type},
                 {"mes", type text}, {"trimestre", type text},
                 {"dia_semana", type text}, {"dia_util", type text}}, "en-US"),
    Ord   = Table.Buffer(Table.Sort(Tipos, {{"data", Order.Ascending}})),
    // dia útil como 1/0
    Uteis = List.Transform(Table.Column(Ord, "dia_util"), each if _ = "Sim" then 1 else 0),
    // soma acumulada EXCLUINDO a linha atual: {0, x1, x1+x2, ...}
    Acum  = List.Buffer(List.RemoveLastN(
                List.Accumulate(Uteis, {0},
                    (estado, x) => estado & {List.Last(estado) + x}), 1)),
    Idx   = Table.AddIndexColumn(Ord, "idx", 0, 1, Int64.Type),
    Antes = Table.AddColumn(Idx, "du_antes", each Acum{[idx]}, Int64.Type),
    Sem   = Table.RemoveColumns(Antes, {"idx"}),
    // auxiliares para ordenar e rotular gráficos
    SemNum = Table.AddColumn(Sem, "dia_semana_num",
                each Date.DayOfWeek([data], Day.Monday) + 1, Int64.Type),
    Abrev  = Table.AddColumn(SemNum, "mes_abrev",
                each {"jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"}{[mes_num] - 1},
                type text)
in
    Abrev


// ---------------------------------------------------------------------
// Consulta: dim_centro   (8 centros; chave id_centro)
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "dim_centro.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"id_centro", type text}, {"centro", type text},
                 {"regiao_centro", type text}, {"ano_abertura", Int64.Type},
                 {"capacidade_diaria", Int64.Type}}, "en-US")
in
    Tipos


// ---------------------------------------------------------------------
// Consulta: dim_cliente   (229 clientes; chave id_cliente)
// "regiao" passa a regiao_cliente para não se confundir com regiao_centro.
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "dim_cliente.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"id_cliente", type text}, {"segmento_cliente", type text},
                 {"regiao", type text}, {"tipo_cliente", type text}}, "en-US"),
    Renom = Table.RenameColumns(Tipos, {{"regiao", "regiao_cliente"}})
in
    Renom


// ---------------------------------------------------------------------
// Consulta: dim_produto   (50 produtos; chave id_produto)
// preco_base é preço de TABELA; o valor das encomendas usa o preço
// efetivamente praticado (linha_encomenda[preco_unitario]).
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "dim_produto.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"id_produto", type text}, {"categoria", type text},
                 {"subcategoria", type text}, {"custo_unitario", type number},
                 {"preco_base", type number}, {"peso_unitario_kg", type number},
                 {"fragil", type text}}, "en-US")
in
    Tipos


// ---------------------------------------------------------------------
// Consulta: dim_transportadora   (6 transportadoras; chave id_transportadora)
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "dim_transportadora.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"id_transportadora", type text}, {"transportadora", type text},
                 {"tipo_transportadora", type text}, {"indice_custo", type number}}, "en-US")
in
    Tipos


// ---------------------------------------------------------------------
// Consulta: objetivos_2026      Grão: centro × mês (8 × 8 = 64 linhas)
// data_mes = 1.º dia do mês (liga a dim_calendario[data]). Só jan–ago.
// volume_objetivo = nº de encomendas; custo_medio_objetivo = € por
// encomenda; taxa_entrega_prazo_objetivo = fração (0–1) de entregas
// até à data prometida.
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "objetivos_2026.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"data_mes", type date}, {"mes", type text}, {"id_centro", type text},
                 {"volume_objetivo", Int64.Type}, {"custo_medio_objetivo", type number},
                 {"taxa_entrega_prazo_objetivo", type number}}, "en-US")
in
    Tipos


// ---------------------------------------------------------------------
// Consulta: linha_encomenda     Grão: 1 linha por produto numa encomenda
// 22 974 linhas. preco_unitario = preço efetivamente praticado (€/un.);
// peso_kg = quantidade × peso_unitario_kg (confirmado: 0 diferenças).
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "linha_encomenda.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"id_linha", type text}, {"id_encomenda", type text},
                 {"id_produto", type text}, {"quantidade", Int64.Type},
                 {"preco_unitario", type number}, {"peso_kg", type number}}, "en-US")
in
    Tipos


// ---------------------------------------------------------------------
// Consulta: stg_encomendas   (desativar carregamento)
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "encomendas.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"id_encomenda", type text}, {"data_encomenda", type date},
                 {"id_cliente", type text}, {"id_centro", type text},
                 {"id_transportadora", type text}, {"tipo_servico", type text},
                 {"canal", type text}, {"prioridade", type text}}, "en-US")
in
    Tipos


// ---------------------------------------------------------------------
// Consulta: stg_entregas   (desativar carregamento)
// custo_transporte = custo logístico da encomenda (parece incluir re-entregas).
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "entregas.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"id_encomenda", type text}, {"data_expedicao", type date},
                 {"data_prometida", type date}, {"data_entrega", type date},
                 {"custo_transporte", type number},
                 {"tentativas_entrega", Int64.Type}}, "en-US")
in
    Tipos


// ---------------------------------------------------------------------
// Consulta: encomendas      Grão: 1 linha por encomenda (10 693)
// Junta as colunas de entregas (relação 1:1 por id_encomenda) numa só
// tabela. Esta consulta NÃO acede a ficheiros: só combina as duas
// consultas de origem (evita o erro "Formula.Firewall").
// Confirmado: 10 693 encomendas = 10 693 entregas, sem órfãos.
// ---------------------------------------------------------------------
let
    Junta   = Table.NestedJoin(stg_encomendas, {"id_encomenda"},
                stg_entregas, {"id_encomenda"}, "ent", JoinKind.LeftOuter),
    Expande = Table.ExpandTableColumn(Junta, "ent",
                {"data_expedicao", "data_prometida", "data_entrega",
                 "custo_transporte", "tentativas_entrega"})
in
    Expande
