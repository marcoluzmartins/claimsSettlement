#!/usr/bin/env python3
"""Regista despesas, receitas e investimentos no ficheiro Gestao_Monetaria__AAAA.xlsx.

O ficheiro é editado diretamente no XML, só nas células tocadas, para preservar
gráficos, tabelas e formatação. As fórmulas do tipo =SUM(a,b,c) ganham mais uma parcela.
O Excel recalcula tudo ao abrir.

Exemplos:
  python gestao.py ficheiro.xlsx                      # modo interativo
  python gestao.py ficheiro.xlsx add super 23.40      # despesa no mês atual
  python gestao.py ficheiro.xlsx add rest 8.5 -m Sep  # noutro mês
  python gestao.py ficheiro.xlsx receita salario 1500 --set
  python gestao.py ficheiro.xlsx invest PPR 167 --set
  python gestao.py ficheiro.xlsx ver                  # categorias e totais do mês
"""
import argparse
import csv
import datetime as dt
import re
import shutil
import sys
import unicodedata
import zipfile
from pathlib import Path

from lxml import etree

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# secção -> (coluna do rótulo, coluna do valor, linhas)
SECTIONS = {
    "despesa": ("C", "D", range(3, 42)),
    "investimento": ("H", "I", range(3, 6)),
    "receita": ("K", "L", range(3, 10)),
}


def q(tag):
    return f"{{{NS}}}{tag}"


def norm(s):
    s = unicodedata.normalize("NFD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def col_idx(col):
    n = 0
    for ch in col:
        n = n * 26 + ord(ch) - 64
    return n


class Workbook:
    def __init__(self, path):
        self.path = Path(path)
        with zipfile.ZipFile(self.path) as z:
            self.files = {i.filename: z.read(i.filename) for i in z.infolist()}
            self.order = [i.filename for i in z.infolist()]
        wb = etree.fromstring(self.files["xl/workbook.xml"])
        rels = etree.fromstring(self.files["xl/_rels/workbook.xml.rels"])
        target = {r.get("Id"): r.get("Target") for r in rels}
        self.sheet_file = {}
        for s in wb.find(q("sheets")):
            t = target[s.get(f"{{{RNS}}}id")].lstrip("/")
            self.sheet_file[s.get("name")] = t if t.startswith("xl/") else "xl/" + t
        sst = etree.fromstring(self.files["xl/sharedStrings.xml"])
        self.strings = ["".join(si.itertext()) for si in sst]
        self.trees = {}

    def tree(self, sheet):
        if sheet not in self.trees:
            self.trees[sheet] = etree.fromstring(self.files[self.sheet_file[sheet]])
        return self.trees[sheet]

    def cell(self, sheet, ref, create=False):
        sd = self.tree(sheet).find(q("sheetData"))
        row_n = int(re.sub(r"\D", "", ref))
        row = next((r for r in sd if int(r.get("r")) == row_n), None)
        if row is None:
            return None
        for c in row:
            if c.get("r") == ref:
                return c
        if not create:
            return None
        col = re.sub(r"\d", "", ref)
        new = etree.Element(q("c"), r=ref)
        above = self.cell(sheet, f"{col}{row_n - 1}")
        if above is not None and above.get("s"):
            new.set("s", above.get("s"))
        pos = 0
        for i, c in enumerate(row):
            if col_idx(re.sub(r"\d", "", c.get("r"))) < col_idx(col):
                pos = i + 1
        row.insert(pos, new)
        return new

    def text(self, c):
        if c is None:
            return ""
        v = c.find(q("v"))
        if v is None:
            return ""
        return self.strings[int(v.text)] if c.get("t") == "s" else v.text

    def labels(self, sheet, kind):
        lc, _, rows = SECTIONS[kind]
        out = []
        for r in rows:
            t = self.text(self.cell(sheet, f"{lc}{r}")).strip()
            if t:
                out.append((r, t))
        return out

    def formula_or_value(self, c):
        if c is None:
            return None
        f = c.find(q("f"))
        if f is not None:
            return f.text or ""
        v = c.find(q("v"))
        return None if v is None else v.text

    def write(self, sheet, ref, amount, add=True):
        """Soma `amount` ao conteúdo da célula (ou substitui). Devolve o novo total."""
        c = self.cell(sheet, ref, create=True)
        cur = self.formula_or_value(c)
        amt = repr(round(amount, 2))
        if amt.endswith(".0"):
            amt = amt[:-2]
        if not add or cur is None or cur.strip() in ("", "0"):
            # célula vazia/zero (ou "definir"): mantém o estilo da célula (fórmula SUM ou valor simples)
            formula = f"SUM({amt})" if c.find(q("f")) is not None else None
            value = amount
        else:
            inner = re.fullmatch(r"SUM\((.*)\)", cur.strip())
            body = inner.group(1) if inner else cur.strip()
            body = "" if body.strip() == "0" else body
            formula = f"SUM({body},{amt})" if body else f"SUM({amt})"
            value = (float(c.findtext(q("v")) or 0)) + amount
        for ch in list(c):
            c.remove(ch)
        c.attrib.pop("t", None)
        if formula:
            etree.SubElement(c, q("f")).text = formula
        etree.SubElement(c, q("v")).text = repr(round(value, 2))
        return round(value, 2)

    def save(self, dest=None):
        for name, root in self.trees.items():
            self.files[self.sheet_file[name]] = etree.tostring(
                root, xml_declaration=True, encoding="UTF-8", standalone=True)
        # força o Excel a recalcular e a reconstruir a cadeia de cálculo
        wb = etree.fromstring(self.files["xl/workbook.xml"])
        wb.find(q("calcPr")).set("fullCalcOnLoad", "1")
        self.files["xl/workbook.xml"] = etree.tostring(
            wb, xml_declaration=True, encoding="UTF-8", standalone=True)
        if "xl/calcChain.xml" in self.files:
            del self.files["xl/calcChain.xml"]
            self.order.remove("xl/calcChain.xml")
            rels = etree.fromstring(self.files["xl/_rels/workbook.xml.rels"])
            for r in list(rels):
                if r.get("Target", "").endswith("calcChain.xml"):
                    rels.remove(r)
            self.files["xl/_rels/workbook.xml.rels"] = etree.tostring(
                rels, xml_declaration=True, encoding="UTF-8", standalone=True)
            ct = etree.fromstring(self.files["[Content_Types].xml"])
            for o in list(ct):
                if o.get("PartName") == "/xl/calcChain.xml":
                    ct.remove(o)
            self.files["[Content_Types].xml"] = etree.tostring(
                ct, xml_declaration=True, encoding="UTF-8", standalone=True)
        dest = Path(dest or self.path)
        tmp = dest.with_suffix(".tmp")
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for n in self.order:
                z.writestr(n, self.files[n])
        tmp.replace(dest)


def find_label(wb, sheet, kind, query):
    labels = wb.labels(sheet, kind)
    nq = norm(query)
    exact = [x for x in labels if norm(x[1]) == nq]
    if exact:
        return exact[0]
    part = [x for x in labels if nq in norm(x[1])]
    if len(part) == 1:
        return part[0]
    if not part:
        raise SystemExit(f"Nada corresponde a '{query}' em {kind}. Opções: "
                         + ", ".join(t for _, t in labels))
    raise SystemExit(f"'{query}' é ambíguo: " + ", ".join(t for _, t in part))


def register(path, kind, query, amount, month, add=True, note=""):
    path = Path(path)
    wb = Workbook(path)
    row, label = find_label(wb, month, kind, query)
    col = SECTIONS[kind][1]
    shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    total = wb.write(month, f"{col}{row}", amount, add)
    wb.save()
    with open(path.with_name("movimentos.csv"), "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([dt.datetime.now().isoformat(timespec="seconds"),
                                month, kind, label, amount, "soma" if add else "define", note])
    return label, total


def show(path, month):
    wb = Workbook(path)
    for kind in SECTIONS:
        print(f"\n[{kind}] {month}")
        for r, t in wb.labels(month, kind):
            v = wb.text(wb.cell(month, f"{SECTIONS[kind][1]}{r}"))
            try:
                v = f"{float(v):.2f}"
            except ValueError:
                pass
            print(f"  {t:42s} {v}")


def interactive(path, month):
    kinds = {"d": "despesa", "r": "receita", "i": "investimento"}
    print(f"Ficheiro: {path} | mês: {month}  (Enter vazio para sair)")
    while True:
        k = input("\nTipo [d]espesa / [r]eceita / [i]nvestimento: ").strip().lower() or None
        if not k:
            return
        if k not in kinds:
            continue
        q_ = input("Categoria (parte do nome): ").strip()
        try:
            amt = float(input("Valor: ").strip().replace(",", "."))
            label, total = register(path, kinds[k], q_, amt, month, add=True)
        except (ValueError, SystemExit) as e:
            print("Erro:", e)
            continue
        print(f"OK -> {label}: total do mês agora {total:.2f}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ficheiro")
    p.add_argument("-m", "--mes", choices=MONTHS, default=MONTHS[dt.date.today().month - 1])
    sub = p.add_subparsers(dest="cmd")
    for name in ("add", "receita", "invest"):
        s = sub.add_parser(name)
        s.add_argument("categoria")
        s.add_argument("valor", type=lambda x: float(x.replace(",", ".")))
        s.add_argument("--set", action="store_true", help="substituir em vez de somar")
        s.add_argument("-n", "--nota", default="")
    sub.add_parser("ver")
    a = p.parse_args()
    if a.cmd is None:
        interactive(a.ficheiro, a.mes)
    elif a.cmd == "ver":
        show(a.ficheiro, a.mes)
    else:
        kind = {"add": "despesa", "receita": "receita", "invest": "investimento"}[a.cmd]
        label, total = register(a.ficheiro, kind, a.categoria, a.valor, a.mes, not a.set, a.nota)
        print(f"OK -> {a.mes} / {label}: {total:.2f}")


if __name__ == "__main__":
    sys.exit(main())
