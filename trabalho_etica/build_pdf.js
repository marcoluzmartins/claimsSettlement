// Gera Relatorio_Toeslagenaffaire.pdf a partir de relatorio.html (Playwright + Chromium).
// Uso: node build_pdf.js   (requer: playwright e pypdf para juntar as duas versões)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');

const dir = __dirname;
const html = 'file://' + path.join(dir, 'relatorio.html');
const out = path.join(dir, 'Relatorio_Toeslagenaffaire.pdf');
const tmpA = path.join(dir, '.tmp_com_rodape.pdf');
const tmpB = path.join(dir, '.tmp_sem_rodape.pdf');

const margin = { top: '16mm', bottom: '18mm', left: '17mm', right: '17mm' };
const footer = `<div style="font-family:'Liberation Sans',Arial,sans-serif;font-size:7.5px;color:#5b6470;width:100%;text-align:center;">
  Toeslagenaffaire · Ética, Cibersegurança e Privacidade de Dados · pág. <span class="pageNumber"></span></div>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(html, { waitUntil: 'load' });
  await page.pdf({ path: tmpA, format: 'A4', margin, printBackground: true, displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: footer });
  await page.pdf({ path: tmpB, format: 'A4', margin, printBackground: true });
  await browser.close();

  // Página 1 (rosto) sem rodapé + restantes páginas com rodapé
  execFileSync('python3', ['-I', '-c', `
import sys
from pypdf import PdfReader, PdfWriter
a, b, out = sys.argv[1:4]
ra, rb = PdfReader(a), PdfReader(b)
w = PdfWriter()
w.add_page(rb.pages[0])
for p in ra.pages[1:]:
    w.add_page(p)
w.add_metadata({'/Title': 'Toeslagenaffaire: dano algorítmico, governação de dados e falha institucional', '/Subject': 'Ética, Cibersegurança e Privacidade de Dados — Tópico B'})
with open(out, 'wb') as f:
    w.write(f)
`, tmpA, tmpB, out], { stdio: 'inherit' });
  fs.unlinkSync(tmpA); fs.unlinkSync(tmpB);
  console.log('OK ->', out);
})();
