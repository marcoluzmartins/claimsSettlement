// =====================================================================
// Power Query (M) – tabelas já recebidas: calendário, centro, cliente,
// produto e objetivos 2026.
//
// Como usar no Power BI Desktop:
//   1. Página Inicial > Transformar dados.
//   2. Parâmetro: Nova origem > Consulta em branco > Editor avançado,
//      colar o bloco "PastaDados" e chamar à consulta PastaDados.
//   3. Para cada tabela: Nova origem > Consulta em branco > Editor
//      avançado, colar o bloco respetivo e dar o nome indicado.
//
// Notas:
//   - Os CSV NÃO são alterados; todas as transformações são feitas aqui.
//   - Culture "en-US" nas conversões de tipo: os decimais usam ponto
//     (8.04) e, com a região do Windows em PT, seriam lidos como 804.
// =====================================================================


// ---------------------------------------------------------------------
// Consulta: PastaDados   (texto – altere para a sua pasta, com "\" final)
// ---------------------------------------------------------------------
"C:\Users\O_SEU_UTILIZADOR\Trabalho_PowerBI\dados\"


// ---------------------------------------------------------------------
// Consulta: dim_calendario
// Grão: 1 linha por dia (2025-01-01 a 2026-10-04). dia_util = Sim/Não
// (seg–sex, sem feriados, conforme o enunciado).
// ATENÇÃO: o calendário vai até 04/10/2026 mas as encomendas só até
// 31/08/2026 -> o período comparável é 1 jan–31 ago de cada ano.
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "dim_calendario.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"data", type date}, {"ano", Int64.Type}, {"mes_num", Int64.Type},
                 {"mes", type text}, {"trimestre", type text},
                 {"dia_semana", type text}, {"dia_util", type text}}, "en-US"),
    // dia útil como número (1 = Sim, 0 = Não)
    DiaUtilNum = Table.AddColumn(Tipos, "dia_util_num",
                each if [dia_util] = "Sim" then 1 else 0, Int64.Type),
    Ordenado = Table.Buffer(Table.Sort(DiaUtilNum, {{"data", Order.Ascending}})),
    // contador acumulado de dias úteis: dias úteis entre duas datas
    // = du_acum(data fim) - du_acum(data início)  (conta o fim, não o início)
    Acum  = List.Skip(List.Accumulate(Table.Column(Ordenado, "dia_util_num"), {0},
                (s, x) => s & {List.Last(s) + x})),
    Final = Table.FromColumns(Table.ToColumns(Ordenado) & {Acum},
                Table.ColumnNames(Ordenado) & {"du_acum"}),
    Tipado = Table.TransformColumnTypes(Final, {{"du_acum", Int64.Type}})
in
    Tipado


// ---------------------------------------------------------------------
// Consulta: dim_centro   (8 centros logísticos; chave id_centro)
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
// A coluna "regiao" é a região do CLIENTE (≠ regiao_centro).
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "dim_cliente.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"id_cliente", type text}, {"segmento_cliente", type text},
                 {"regiao", type text}, {"tipo_cliente", type text}}, "en-US"),
    Renomear = Table.RenameColumns(Tipos, {{"regiao", "regiao_cliente"}})
in
    Renomear


// ---------------------------------------------------------------------
// Consulta: dim_produto   (50 produtos; chave id_produto)
// preco_base é preço de TABELA: para o valor das encomendas usar o preço
// efetivamente praticado nas linhas de encomenda (enunciado).
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
// Consulta: objetivos_2026
// Grão: centro × mês (8 centros × 8 meses = 64 linhas, jan–ago 2026).
// data_mes = 1.º dia do mês -> liga a dim_calendario[data].
// Só existem objetivos até agosto: a Q5 limita-se a jan–ago.
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


// =====================================================================
// TABELAS DE FACTOS
// =====================================================================

// ---------------------------------------------------------------------
// Consulta: linha_encomenda   Grão: 1 linha por produto numa encomenda
// (22 974 linhas; FK id_encomenda, id_produto).
// preco_unitario = preço efetivamente praticado.
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
// Consulta: encomendas   Grão: 1 linha por encomenda (10 693)
// Junta as colunas de "entregas" (relação 1:1 pela chave id_encomenda)
// -> uma única tabela ao grão da encomenda; evita relação 1:1 no modelo
// e dá ao Key Influencers (Q9) tudo na mesma tabela.
// Depois de criada, desligar "Ativar carregamento" na consulta
// "entregas" (só serve de origem).
// ---------------------------------------------------------------------
let
    Fonte = Csv.Document(File.Contents(PastaDados & "encomendas.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"id_encomenda", type text}, {"data_encomenda", type date},
                 {"id_cliente", type text}, {"id_centro", type text},
                 {"id_transportadora", type text}, {"tipo_servico", type text},
                 {"canal", type text}, {"prioridade", type text}}, "en-US"),
    Junta = Table.NestedJoin(Tipos, {"id_encomenda"}, entregas, {"id_encomenda"},
                "ent", JoinKind.LeftOuter),
    Expande = Table.ExpandTableColumn(Junta, "ent",
                {"data_expedicao", "data_prometida", "data_entrega",
                 "custo_transporte", "tentativas_entrega"})
in
    Expande


// ---------------------------------------------------------------------
// Consulta: entregas   Grão: 1 linha por encomenda (10 693; 1:1)
// custo_transporte = custo logístico da encomenda.
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
