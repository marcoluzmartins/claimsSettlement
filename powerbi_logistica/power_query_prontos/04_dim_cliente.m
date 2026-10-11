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
