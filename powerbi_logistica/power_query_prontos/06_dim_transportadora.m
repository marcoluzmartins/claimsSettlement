let
    Fonte = Csv.Document(File.Contents(PastaDados & "dim_transportadora.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cab   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cab,
                {{"id_transportadora", type text}, {"transportadora", type text},
                 {"tipo_transportadora", type text}, {"indice_custo", type number}}, "en-US")
in
    Tipos
