// Renders the animated overlays in anim.html to PNG sequences + ProRes 4444 (alpha) .mov files.
//   nice -n 15 node pitch/video/edit/fx/anim/render_anim.mjs [name ...]
// Canvas frames are read via toDataURL (exact alpha); one browser, one page, t stepped at 30 fps.
import { createRequire } from 'node:module';
import { mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(HERE, '../../../../film/package.json'));
const puppeteer = require('puppeteer-core');
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const FFMPEG = path.join(HERE, '../../bin/ffmpeg');
const FPS = 30;
const names = process.argv.slice(2).length ? process.argv.slice(2) : ['pill-rain', 'sparkle-burst', 'confetti'];

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--allow-file-access-from-files'] });
try {
  const page = await browser.newPage();
  await page.goto(pathToFileURL(path.join(HERE, 'anim.html')).href);
  for (const name of names) {
    const { w, h, dur } = await page.evaluate((n) => window.setup(n), name);
    const dir = path.join(HERE, name);
    rmSync(dir, { recursive: true, force: true }); mkdirSync(dir);
    const n = Math.round(dur * FPS);
    for (let i = 0; i < n; i++) {
      const url = await page.evaluate((nm, t) => window.frame(nm, t), name, i / FPS);
      writeFileSync(path.join(dir, String(i).padStart(4, '0') + '.png'), Buffer.from(url.split(',')[1], 'base64'));
    }
    const mov = path.join(HERE, name + '.mov');
    execFileSync(FFMPEG, ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, '%04d.png'),
      '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-alpha_bits', '16', mov]);
    console.log('wrote', name, `${w}x${h}`, `${n} frames`, mov);
  }
} finally {
  await browser.close();
}
