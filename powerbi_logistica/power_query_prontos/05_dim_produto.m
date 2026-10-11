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
