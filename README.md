# Pill

Pill screens one tablet from a medicine delivery before the clinic pays the supplier. A small dark station (Arduino UNO Q, blue, white and red LEDs, two photoresistors) watches one tablet dissolve in a cup of water and compares the curve with a known-good reference. The answer is one of three: **Passed the screen**, **Needs lab testing**, or **Unable to verify**. In the clinic app, that answer decides whether the supplier's payment is proposed for release, held, or handed to a person. All money is TESTNET / SANDBOX.

First built at Cal Hacks 13.0 (October 24-25, 2026). Devpost: https://devpost.com/software/pill-01mtdn · Demo video: https://youtu.be/yXEmc25dfMw · Site: https://pillmeifyoucan.health

## What's in this repo

| Folder | What it is |
|---|---|
| `pillgate/` | **Pill Gate**, the station app: Python + FastAPI + SQLite, vanilla JS front end. Curve maths, quality gates, guided run, lid detection, evidence lookups, report and guardrail. 14 pytest tests. |
| `firmware/` and `pillgate/firmware/` | Arduino sketches. The firmware streams one reading a second and decides nothing. |
| `pill/web/` | The clinic app: React 19 + TypeScript + Vite (deployed on Vercel). Seven deterministic rules set every verdict. |
| `pill/pay/` | The pay service: Node 22 + Express on Base Sepolia (x402 seller, verdict-gated escrow, policy agent). |
| `pill-site/` | The project website. |
| `pillgate/cad/` | 3D-printable chamber, lid and plates (STL). |

## Run it

**Station app (no hardware needed for a replay):**

```bash
cd pillgate/app
pip install -r requirements.txt
REPLAY_FILE=../runs/SIM_good.csv python server.py     # open http://localhost:8000 (shows "REPLAY (not live)")
python -m pytest -q tests                             # 14 tests, no hardware or internet
```

With the UNO Q plugged in, run `python server.py` (or `./pillgate/start.sh`). Details: `pillgate/app/README.md`.

**Clinic app + pay service:**

```bash
cd pill/pay && npm install && cp -n .env.example .env && npm run serve      # port 8402; missing keys report "unavailable"
cd pill/web && npm install && printf 'VITE_PAY_URL=http://127.0.0.1:8402\n' > .env.local && npx vite --port 5183
```

Details: `pill/web/README.md` and `pill/pay/README.md`.

## AI tools and services used

- **Anthropic Claude (Claude Sonnet), station evidence and the escrow clerk:** reads the bottle label and tablet imprint, writes the plain-language report with numbered sources and the "why" behind a verdict, answers Ask Pill questions from Pill's own record, and acts as the escrow clerk, which may only agree with the ceiling computed in code or escalate. It never sets a verdict or moves money. Set `ANTHROPIC_API_KEY`; without it the station app runs in a labelled mock mode.
- **Google Gemini, the clinic checks:** reads the delivery label into editable fields (unreadable fields stay empty), runs the checker agent over the label, up to three frames of the cup and an openFDA recall lookup, and powers the small helper on each clinic screen. It never sets a verdict or moves money.
- **Public data services:** openFDA (NDC directory and recalls by lot) and RxNav (drug names).
- **Payments (TESTNET):** Coinbase Developer Platform server wallets and x402 (`@x402/express`, `@x402/evm`) on Base Sepolia; a Capital One Nessie sandbox mirror.
- **Built with AI coding agents** running Anthropic's Claude models.

## What's real, what's not yet

Real: the station hardware, one measured aspirin run, live Claude / Gemini / openFDA / RxNav calls, and a real x402 `402 Payment Required` on TESTNET. Not yet: a reference profile (so real scans end Unable to verify), the paid x402 response and escrow transfers (simulated until a CDP key is added). Demo curves in the clinic app are labelled replays.

## Credit

Method modelled on the public write-up of Peel (HackMIT 2026 grand prize): a water blank, a light sensor watching a tablet dissolve, a side sensor for cloudiness, and three plain answers. No code was taken from Peel.
