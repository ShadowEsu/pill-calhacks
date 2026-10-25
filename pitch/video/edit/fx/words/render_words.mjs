// Frame-steps the per-word overlays (<name>.html exposes window.ANIM = {w, h, dur} and window.render(t))
// with puppeteer, screenshots each frame with a transparent background, then encodes ProRes 4444 with alpha.
//   nice -n 15 node pitch/video/edit/fx/words/render_words.mjs [name ...]
// Uses puppeteer-core from pitch/film/node_modules and the local Chrome (CHROME= to override).
import { createRequire } from 'node:module';
import { mkdirSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(HERE, '../../../../film/package.json'));
const puppeteer = require('puppeteer-core');
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const FFMPEG = path.join(HERE, '../../bin/ffmpeg');
const FPS = 30;
const names = process.argv.slice(2).length ? process.argv.slice(2) : ['pill-pop', 'water-magic', 'shake-flash'];

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--allow-file-access-from-files'] });
try {
  const page = await browser.newPage();
  for (const name of names) {
    await page.goto(pathToFileURL(path.join(HERE, `${name}.html`)).href, { waitUntil: 'load' });
    await page.evaluate(async () => { await document.fonts.ready; });
    const { w, h, dur } = await page.evaluate(() => window.ANIM);
    await page.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
    const tmp = path.join(os.tmpdir(), `anim-${name}`);
    rmSync(tmp, { recursive: true, force: true });
    mkdirSync(tmp, { recursive: true });
    const n = Math.round(dur * FPS);
    for (let i = 0; i < n; i++) {
      await page.evaluate((t) => window.render(t), i / FPS);
      await page.screenshot({ path: path.join(tmp, `${String(i).padStart(4, '0')}.png`), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
    }
    const out = path.join(HERE, `${name}.mov`);
    execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(tmp, '%04d.png'),
      '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-alpha_bits', '16', out]);
    console.log('wrote', path.relative(process.cwd(), out), `${n} frames ${w}x${h}`, `frames in ${tmp}`);
  }
} finally {
  await browser.close();
}
