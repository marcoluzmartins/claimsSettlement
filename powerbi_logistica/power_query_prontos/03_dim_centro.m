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
