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
