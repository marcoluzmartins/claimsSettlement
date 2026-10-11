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
