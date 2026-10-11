let
    Junta   = Table.NestedJoin(stg_encomendas, {"id_encomenda"},
                stg_entregas, {"id_encomenda"}, "ent", JoinKind.LeftOuter),
    Expande = Table.ExpandTableColumn(Junta, "ent",
                {"data_expedicao", "data_prometida", "data_entrega",
                 "custo_transporte", "tentativas_entrega"})
in
    Expande
