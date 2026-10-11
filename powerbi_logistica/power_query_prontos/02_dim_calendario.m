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
