# Gestão Monetária

Regista despesas, receitas e investimentos diretamente no `Gestao_Monetaria__AAAA.xlsx`
(uma folha por mês). Edita só as células tocadas, por isso gráficos e formatação ficam intactos.

    pip install -r requirements.txt
    python gestao.py Gestao_Monetaria__2026.xlsx                  # modo interativo
    python gestao.py Gestao_Monetaria__2026.xlsx add super 23,40  # soma à fórmula =SUM(...)
    python gestao.py Gestao_Monetaria__2026.xlsx -m Sep add rest 8.5
    python gestao.py Gestao_Monetaria__2026.xlsx receita salario 1500 --set
    python gestao.py Gestao_Monetaria__2026.xlsx invest PPR 167 --set
    python gestao.py Gestao_Monetaria__2026.xlsx ver

- A categoria aceita parte do nome, sem acentos nem maiúsculas ("seguro" é ambíguo e pede mais detalhe).
- Feche o Excel antes de correr. Cada escrita cria `ficheiro.xlsx.bak` e acrescenta uma linha a `movimentos.csv`.
- Os totais recalculam-se ao abrir no Excel.
