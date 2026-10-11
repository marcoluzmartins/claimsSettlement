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
