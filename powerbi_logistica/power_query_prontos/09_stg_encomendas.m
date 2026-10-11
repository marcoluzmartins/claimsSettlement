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
