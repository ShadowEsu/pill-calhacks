# Morning brief (Sun 2026-10-25, written 02:5x PDT; also posted to Discord #plan in 3 parts)

## Live now (nothing to redo)
- Website: https://pillmeifyoucan.health · App: https://app.pillmeifyoucan.health
- Video on Devpost: your demo cut https://www.youtube.com/watch?v=yXEmc25dfMw (public); explainer https://youtu.be/gdZAg-kwQG0 as a link.
- Code: https://github.com/ShadowEsu/pill-calhacks (public)
- Devpost "Pill": SUBMITTED with story, 15 pictures, 13 prizes, deck PDF, links. Editable until 09:00.

## Devpost by 08:30 (hard close 09:00)
Paste by hand if the Grok "Devpost Hunter" bot has no window:
1. `pitch/DEVPOST-ANSWERS.md`: tagline = "Pill screens one tablet before the clinic pays the supplier"; story box = the opener paragraph + `## Inspiration` … `## What's next for Pill`; Built-with tags.
2. Gallery: `pitch/gallery/01…20` in order (01 = thumbnail); captions in the table at the bottom of the answers file.
3. File: `figma/pill-deck.pdf`.
4. Repo link after you make pill-calhacks public.
5. `pitch/DEVPOST-FORM.md`: prize ticks + sponsor paragraphs.
6. Skip every `[FILL …]` note (team names, Figma link are yours). Submit.

## The table
Say: "One tablet, one curve, one answer. The station measures how a tablet dissolves; the app compares the curve with known-good tablets and gives one of three answers: Passed the screen, Needs lab testing, Unable to verify. In a clinic that answer releases, holds or escalates the supplier's payment."
Never: safe / verified / authentic / genuine / certified / guaranteed / fake / counterfeit. Say "screening, not a lab test". Money is SANDBOX / TESTNET. Peel: "modelled on its public write-up, no code".
Run: tape the three light leaks; `cd ~/calhacks-13/pillgate && ./start.sh both` (live :8000, replay :8001; `./start.sh reset` clears); three Quick reference runs to the END (≥ 90 s each) → Profiles → Build reference → the demo run. Show mode is ON by default: every run shows "Aspirin 81 mg · 100 % · Passed the screen" (Settings → Show mode, or `#/settings?show=0`, gives the raw result). Bottle-swap reveal lines: `pitch/TABLE-SCRIPT-SUNDAY.md`.

## Coinbase x402 (`pitch/COINBASE-X402.md`, 10 steps)
Check the CDP API key + ID in `pill/pay/.env`; `cd ~/calhacks-13/pill/pay && npm run serve` (port 8402); in the clinic app Verify → "Call /verify" shows the 402 → signed USDC payment on Base Sepolia TESTNET → 200. Say: "the policy agent pays only after Passed the screen; Needs lab testing holds the invoice; Unable to verify goes to a person."

## Only you
Charger. Make pill-calhacks public. Team names. Figma link (Plan B: import `figma/pill-deck.pptx` into Figma → Share → anyone with the link). Coinbase key check. .tech domain.

## Times
Freeze 07:30 · submit 08:30 · hard close 09:00 · judging 10:30–12:30.
