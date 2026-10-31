// Gera as imagens dos ecrãs da app (docs/ecras/*.png) num telemóvel virtual de 390x844.
// Requer Node e Playwright: node scripts/capturar_ecras.js
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const raiz = path.resolve(__dirname, "..");
const saida = path.join(raiz, "docs", "ecras");
const PORTA = 8765;
const URL = `http://127.0.0.1:${PORTA}/`;
fs.mkdirSync(saida, { recursive: true });

async function esperarServidor() {
  for (let i = 0; i < 60; i++) {
    try { if ((await fetch(URL + "api/concelhos")).ok) return; } catch (_) { /* ainda a arrancar */ }
    await new Promise(r => setTimeout(r, 200));
  }
  throw new Error("O servidor não arrancou.");
}

async function analisarSimples(page, { concelho, preco, area }) {
  await page.goto(URL);
  await page.selectOption("#concelho", concelho);
  await page.fill("#preco", String(preco));
  await page.fill("#area", String(area));
  await page.click('#exposicao [data-v="S"]');
  await page.click("#analisar");
  await page.waitForSelector("#p-veredicto .badge");
}

(async () => {
  const servidor = spawn("python3", ["-m", "imovel_radar.server", "--porta", String(PORTA)], { cwd: raiz, stdio: "inherit" });
  const navegador = await chromium.launch();
  const ficheiros = {};
  // Ajusta a janela à altura do conteúdo: assim o cabeçalho e a barra inferior ficam nos
  // extremos do ecrã (uma captura "fullPage" deixá-los-ia a meio da imagem).
  const guardar = async (page, nome, legenda, depois) => {
    const ficheiro = path.join(saida, nome + ".png");
    const altura = await page.evaluate(() => Math.max(844, document.documentElement.scrollHeight));
    await page.setViewportSize({ width: 390, height: altura });
    if (depois) await depois();
    await page.screenshot({ path: ficheiro });
    await page.setViewportSize({ width: 390, height: 844 });
    ficheiros[nome] = { ficheiro, legenda };
  };
  try {
    await esperarServidor();
    const contexto = await navegador.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, locale: "pt-PT", colorScheme: "light" });
    const page = await contexto.newPage();

    await page.goto(URL);
    await page.waitForFunction(() => document.querySelectorAll("#concelho option").length > 1);
    await guardar(page, "01-formulario", "1. Dados do imóvel");

    await page.click("#exemplo");
    await guardar(page, "02-formulario-preenchido", "2. Com os extras: piscina, anexos, terreno");

    await page.click("#analisar");
    await page.waitForSelector("#p-veredicto .badge");
    await guardar(page, "03-veredicto", "3. Veredicto e o que pesa no valor");

    await page.click('nav [data-tab="zona"]');
    await guardar(page, "04-zona", "4. Padrão da zona e zonas semelhantes");

    await page.click('nav [data-tab="hist"]');
    await guardar(page, "05-historico", "5. Histórico comparativo");

    await page.click('nav [data-tab="prev"]');
    await guardar(page, "06-previsao", "6. Previsão a 5, 10 e 20 anos");
    await guardar(page, "07-previsao-detalhe", "7. Toque no gráfico: valores por cenário", async () => {
      const grafico = await page.locator("#gp svg").boundingBox();
      await page.mouse.move(grafico.x + grafico.width * 0.6, grafico.y + grafico.height * 0.5);
    });

    await analisarSimples(page, { concelho: "Exemplo-Cidade", preco: 270000, area: 85 });
    await guardar(page, "08-veredicto-aceitavel", "8. Exemplo: preço aceitável");
    await analisarSimples(page, { concelho: "Exemplo-Litoral", preco: 360000, area: 110 });
    await guardar(page, "09-veredicto-bom-negocio", "9. Exemplo: bom negócio");

    const escuro = await navegador.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, locale: "pt-PT", colorScheme: "dark" });
    const pe = await escuro.newPage();
    await pe.goto(URL);
    await pe.waitForFunction(() => document.querySelectorAll("#concelho option").length > 1);
    await pe.click("#exemplo");
    await pe.click("#analisar");
    await pe.waitForSelector("#p-veredicto .badge");
    await pe.click('nav [data-tab="hist"]');
    await guardar(pe, "10-historico-modo-escuro", "10. Modo escuro");

    // Folha com os ecrãs principais lado a lado.
    const principais = ["02-formulario-preenchido", "03-veredicto", "04-zona", "05-historico", "06-previsao", "09-veredicto-bom-negocio"];
    const celulas = principais.map(n => {
      const b64 = fs.readFileSync(ficheiros[n].ficheiro).toString("base64");
      return `<figure><img src="data:image/png;base64,${b64}"><figcaption>${ficheiros[n].legenda}</figcaption></figure>`;
    }).join("");
    const folha = await navegador.newPage({ viewport: { width: 1360, height: 900 } });
    await folha.setContent(`<style>body{margin:0;padding:28px;background:#e9e8e3;font:600 15px system-ui,sans-serif;color:#0b0b0b}
      h1{margin:0 0 4px;font-size:26px} p{margin:0 0 22px;font-weight:400;color:#52514e}
      .g{display:flex;flex-wrap:wrap;gap:26px;align-items:flex-start}
      figure{margin:0;width:390px}img{width:390px;display:block;border-radius:18px;box-shadow:0 6px 24px rgba(0,0,0,.18)}
      figcaption{margin-top:10px;text-align:center}</style>
      <h1>Imóvel Radar: como a app funciona</h1><p>Protótipo com dados de exemplo (sintéticos). Os valores não são reais.</p><div class="g">${celulas}</div>`);
    await folha.screenshot({ path: path.join(saida, "00-visao-geral.png"), fullPage: true });
    console.log("Imagens guardadas em", saida);
  } finally {
    await navegador.close();
    servidor.kill();
  }
})().catch(e => { console.error(e); process.exit(1); });
