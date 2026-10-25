// Renders fx/stickers/*.svg to PNGs with a real alpha channel at 2× their own SVG size (width/height attributes).
//   node pitch/video/edit/fx/render_fx_stickers.mjs
// Same puppeteer-core + local Chrome setup as ../render_stickers.mjs (CHROME= to override).
import { createRequire } from 'node:module';
import { readdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const EDIT = path.join(HERE, '..');
const require = createRequire(path.join(EDIT, '../../film/package.json'));
const puppeteer = require('puppeteer-core');
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const DIR = path.join(HERE, 'stickers');
const SCALE = 2;
const font = (f) => pathToFileURL(path.join(EDIT, 'fonts', f)).href;
const CSS = `@font-face{font-family:"Inter";src:url("${font('Inter-Variable.ttf')}");font-weight:100 900}
@font-face{font-family:"Instrument Serif";src:url("${font('InstrumentSerif-Regular.ttf')}")}
html,body{margin:0;background:transparent}svg{display:block}`;

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--allow-file-access-from-files'] });
try {
  const page = await browser.newPage();
  for (const f of readdirSync(DIR).filter((x) => x.endsWith('.svg')).sort()) {
    const svg = readFileSync(path.join(DIR, f), 'utf8');
    const width = Number(svg.match(/\bwidth="(\d+)"/)[1]);
    const height = Number(svg.match(/\bheight="(\d+)"/)[1]);
    await page.setViewport({ width, height, deviceScaleFactor: SCALE });
    await page.goto(pathToFileURL(DIR + '/').href, { waitUntil: 'load' });  // file:// origin so the @font-face URLs load
    await page.setContent(`<!doctype html><style>${CSS}</style>${svg}`, { waitUntil: 'load' });
    await page.evaluate(async () => { await document.fonts.ready; });
    const out = path.join(DIR, f.replace(/\.svg$/, '.png'));
    await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width, height } });
    console.log('wrote', path.relative(process.cwd(), out), `${width * SCALE}x${height * SCALE}`);
  }
} finally {
  await browser.close();
}
