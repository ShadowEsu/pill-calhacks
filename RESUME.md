# RESUME (stand-down note Sun 2026-10-25 14:46 PDT; original written 02:52 when the Mac was at 8 %)

**Cal Hacks 13.0 is over for Pill** (Preston 14:4x: "we are done"). Final state: Devpost SUBMITTED with 8 links and video yXEmc25dfMw; site https://pillmeifyoucan.health and app https://app.pillmeifyoucan.health stay live on Vercel as deployed; the public repo **https://github.com/ShadowEsu/pill-calhacks** (`main` = 030fe5e or later) holds everything; the Figma Slides deck is https://www.figma.com/deck/xSmcPKdRTVgKI7XzGoqQ0R/pill-deck. Local services (station :8000/:8001, pay :8402, ngrok) were stopped at 14:45 (`~/Downloads/peel/start.sh stop`); restart with `./start.sh both` + `cd pill/pay && npm run serve`. Not deleted yet (BOSS is asking Preston): `~/calhacks-13-deploy/pre-purge-backup.bundle` and the screenshots there. The old `ShadowEsu/pill` repo stays PRIVATE forever (its old SHAs still hold the purged photos). Section 2 below is historical: every item is done.

## 0. Where things are
- Judges poster: `pitch/onepager/Pill-judges-landscape.pdf` (9 pp). Technical overview: `pitch/onepager/Pill-technical.pdf` (7 pp). Table script: `pitch/TABLE-SCRIPT-SUNDAY.md`. Devpost text: `pitch/DEVPOST-ANSWERS.md`. Coinbase steps: `pitch/COINBASE-X402.md`. Video build: `pitch/video/edit/build-v13.sh`.
- Judging incident: the UNO Q stopped emitting serial at 10:22 (board hang; needs RESET/replug). `pillgate/app/device.py` now reopens the port after 8 s of silence; the demo ran on the :8001 replay.

## 1. What is LIVE (nothing to redo)
- Website **https://pillmeifyoucan.health** (+ www) → Vercel project `pill-site`, deploy `dpl_DAthQmhcfCnVMNHi9RPNWW1xPqvJ` (02:51: #film, night fixes, domain links, robots/sitemap).
- Clinic app **https://app.pillmeifyoucan.health** → Vercel project `pill-app`, deploy `dpl_3CL4hiAswvAKtGgarsmCehh6mNgU` (02:52: nosniff/Referrer-Policy headers, links to the new domain).
- DNS at Porkbun (Preston's account): `A @ 76.76.21.21`, `CNAME www cname.vercel-dns.com`, `CNAME app cname.vercel-dns.com`. Done, verified 200 over https.
- YouTube, channel "Pill" (@pillmeifyoucan, Preston's Google account): two videos: the final demo cut 2:28 PUBLIC https://www.youtube.com/watch?v=yXEmc25dfMw (cleaned voice, quiet lofi "Chillhop — Remain"/Pixabay, CC0 sfx, highlighter captions, stickers) and the animated explainer 2:38 PUBLIC https://youtu.be/gdZAg-kwQG0. Every earlier talking-head upload was deleted at 08:33 on the owner's order. Build: `pitch/video/edit/build-v13.sh` + `graph-v13.txt` (`MUSIC=fx/audio/lofi-1.wav`), sources in `fx/audio/SOURCES.md`.
- Devpost "Pill" (Cal Hacks 13.0): SUBMITTED (team pressed Submit ~07:4x). Grok filled: story (12,258 chars), 15-image gallery (01 thumbnail), 13 prizes, feedback, AI tools, 8 Try-it-out links (site, app, both domains, explainer, repo, site/#coinbase, Figma deck), pill-deck.pdf as the file; video = yXEmc25dfMw (saved 08:48). Devpost's own counter still allowed edits at 09:16 ("14 more minutes").
- Figma Slides deck (Preston's Figma, Education plan; "Anyone can view"): https://www.figma.com/deck/xSmcPKdRTVgKI7XzGoqQ0R/pill-deck (edit: `/slides/` same key). Imported from `figma/pill-deck.pptx` at 8b47bac by a scripted drop in Arc (Figma's REST API cannot create or read Slides files). The first import `3cHkC67oH7SZrBbOPlwYus` (headings wrapping to 3 lines on slides 1 and 4) is still in Drafts; trash it.
- Drive kit (folder "Agent Company - Shipped/HQ/2026-10-25"): DEVPOST-ANSWERS.md (current), DEVPOST-FORM.md, gallery 01–20, pill-deck.pdf. https://drive.google.com/drive/folders/1gXd-B5CU1BKo1GbVIldss1M-IZofhUpK
- Station app: Show mode is ON by default (every run shows "Aspirin 81 mg · 100 % · Passed the screen"; Settings → Show mode, or `#/settings?show=0`, turns it off). Synced to `~/Downloads/peel` (backend byte-identical to v16).

## 2. Still to do (in order)
1. **Devpost text + gallery + prizes + submit** (Preston approved: fill everything, then Submit; he can still edit until 09:00). Either via the Grok bot (`grokbot prompt "Devpost Hunter" "…" --wait 120`, prompt ≤ 8000 chars, the bot window must be open on the Mac: it had no window at 02:45) or by hand from `pitch/DEVPOST-ANSWERS.md` (tagline = option 1; story = opener + ## Inspiration … ## What's next; Built with; gallery `pitch/gallery/01…20` in order with the captions in the table; upload `figma/pill-deck.pdf` as the file) and `pitch/DEVPOST-FORM.md` (prize ticks + sponsor paragraphs). Skip every `[FILL …]`.
2. Owner-only: make `ShadowEsu/pill-calhacks` public (then paste the repo link into Devpost), team names, Figma link (Plan B: import `figma/pill-deck.pptx`), Coinbase key check (`pitch/COINBASE-X402.md`), charger.
3. Morning brief: `pitch/MORNING-BRIEF.md` (not written yet; use `pitch/TABLE-SCRIPT-SUNDAY.md` + `SUNDAY-RUNBOOK.md`).
4. Optional: one more site deploy before 07:30 if SiteStory lands more fixes (slot rule: ≥ 2 h after 02:51 → ≥ 04:51). Deploy from the git-less copies `~/calhacks-13-deploy/<pill-site|pill-app>/` (Vercel blocks the calhacks-helper author): `rm -rf .vercel && cp -R <project>/.vercel . && npx -y vercel@latest deploy --prebuilt --prod --yes --scope shadowesus-projects`; build first in-repo with `npx -y vercel@latest build --prod --yes`.

## 3. Table (owner + teammate)
Tape the three light leaks; `cd ~/calhacks-13/pillgate && ./start.sh both` (live :8000, replay :8001); 3 × Quick reference runs to the END (≥ 90 s) → Profiles → Build reference → 4th run. Show mode is already on. "Host the app" online (`./start.sh online`, ngrok + PIN) only during judging and with BOSS's guardrails (cap Claude scans, no /debug).

## 4. Deadlines
Devpost submit 08:30, hard close 09:00, judging 10:30–12:30 (freeze 07:30).
