# Clinic / personal app — gallery captions

Live at https://app.pillmeifyoucan.health. Desktop shots 1280×800 (saved at 1.25×), phone shots 390×844 (saved at 2×). All money shown is SANDBOX / TESTNET.

| # | File | Title (≤ 60 chars) | Description (≤ 160 chars) |
|---|------|--------------------|---------------------------|
| 1 | clinic-01-dashboard.png | Clinic dashboard | A week at a glance: deliveries, PASS rate, held and released money (SANDBOX / TESTNET), the station card and its live pulse. |
| 2 | clinic-02-deliveries.png | Deliveries by lot | Every incoming lot moves through logged → tested → decision. Each row shows its escrow state and the station's answer. |
| 3 | clinic-03-delivery-held.png | One delivery: held (NEEDS LAB) | Lot TM-01 got NEEDS LAB, so the payment stays in escrow (SANDBOX / TESTNET) and a lab referral is drafted. |
| 4 | clinic-04-delivery-released.png | One delivery: released (PASS) | Lot B2-01 Passed the screen, and a pharmacist's tap released the test USDC from escrow to the supplier. |
| 5 | clinic-05-verify-402-lane.png | Pay per verdict: the 402 lane | After "Send curve" the x402 lane lights up to 402 Payment Required → buyer signs. The paid 200 stays dashed (simulated, TESTNET). |
| 6 | clinic-06-verify-x402-exchange.png | x402 request, step by step | The raw exchange: POST /verify → 402 with the 0.05 USDC price on Base Sepolia (TESTNET) → signed retry → verdict JSON. |
| 7 | clinic-07-pay-release.png | Where the money goes: release | The policy agent's path for a PASS lot: release only after a pharmacist's tap, escrow → supplier wallet (TESTNET). |
| 8 | clinic-08-pay-escalate.png | Where the money goes: escalate | For an UNABLE TO VERIFY lot the agent escalates to a person, and no money moves. |
| 9 | clinic-09-kiosk-ready.png | Station kiosk: ready | The screen on the box itself: clean water in, lid closed, press Start. Live absorbance chart and light path on the right. |
| 10 | clinic-10-kiosk-replay-running.png | Station kiosk: tablet dissolving | A recorded run replaying: the inline and 90° glow channels climb toward the reference band as the tablet dissolves. |
| 11 | clinic-11-kiosk-pass-verdict.png | Station kiosk: PASS | The run ends at 100 % of reference, rule P1, PASS, with the note "Screening result, not a pharmacopeial test." |
| 12 | clinic-12-runs.png | Runs | 13 runs through the data path: station → seven rules → Claude's why → policy agent. A heatmap of runs per hour, and filters by verdict. |
| 13 | clinic-13-evaluation.png | One run's evaluation | PASS at 101 % of reference, plateau inside the band, both channels shown, and the plain-English reason. |
| 14 | clinic-14-activity.png | Activity feed | Who did what and when: station runs, lots logged into escrow, policy agent holds, and the assistant's summaries. |
| 15 | clinic-15-log.png | Decision log | Every lot's money decisions in order, filterable by lot and exportable as CSV. SANDBOX / TESTNET amounts. |
| 16 | clinic-16-medicines.png | My medicines | Bottles on file with recall status and the station's answer for each. This list never re-tests by itself. |
| 17 | clinic-17-station.png | Station status | Station state, last five runs as tablet icons, and the six run phases from lights off to verdict. |
| 18 | clinic-18-calibration.png | Calibration | Ten reference tablets, dissolved one by one; their plateaus set the band that every later run is judged against. |
| 19 | clinic-19-check.png | Checker | Reads the label, looks for a recall and checks the cup. It explains the sensor result; it never changes it. |
| 20 | clinic-20-agent-record.png | Policy agent: escrow clerk | What the agent may do (propose release, hold, escalate, draft a lab referral) and what it can't (move money or edit caps). |
| 21 | clinic-21-ask.png | Ask Pill | Ask about runs, lots, deliveries and holds. Answers come only from Pill's record and the seven rules. |
| 22 | clinic-22-schedule.png | Schedule | Today's doses with "I took it" and reminder buttons. |
| 23 | clinic-23-add-bottle.png | Add a bottle | Photograph the label; Gemini reads the fields, and anything it can't read stays empty. |
| 24 | clinic-24-place-tablet.png | Prepare a run | Station self-checks (LED baseline, dark reading, stick, lid), then: fill the cup with clean water. |
| 25 | clinic-25-medical-home.png | Medical home | The clinic's quick view: scan a bottle and see the latest deliveries with their escrow state. |
| 26 | clinic-26-personal-today.png | Personal mode: Today | Big-text home for one person: next dose, today's doses, recall status and the Easy mode switch. |
| 27 | clinic-27-welcome.png | Welcome: who is this for? | Pick clinic (lots, escrow in SANDBOX, decision log) or personal (bottles, reminders, big text), or watch the story. |
| 28 | clinic-28-story.png | How Pill works: chapter 1 | The problem, with its source: 1 in 10 medical products in low- and middle-income countries is substandard or falsified (WHO). |
| 29 | clinic-29-settings.png | Settings | Who I am, Easy mode, big text, sound, follower assistant, and links to every data source the app uses. |
| 30 | clinic-30-demo.png | Two-minute demo | One delivery from label to hold on the real screens, with a replayed run of lot TM-02 and SANDBOX / TESTNET money. |
| 31 | clinic-31-demo-run-lights-off.png | Demo: lights off | The run's first phase: all LEDs off so the station learns what dark looks like. The caption bar narrates each step. |
| 32 | clinic-32-demo-lot-held.png | Demo: lot TM-02 held | NEEDS LAB at 93 %: $480 stays held in escrow (SANDBOX / TESTNET). Release is off, so hold or ask a person. |
| 33 | clinic-33-phone-dashboard.png | Phone: dashboard | The same dashboard on a phone, with a bottom tab bar. |
| 34 | clinic-34-phone-deliveries.png | Phone: deliveries | The lot pipeline on a phone: logged, tested, policy decided, released by a pharmacist's tap. |
| 35 | clinic-35-phone-verify-402.png | Phone: pay per verdict | The x402 diagram on a phone after a request. Swipe sideways to follow the arrows. TESTNET. |
| 36 | clinic-36-phone-kiosk.png | Phone: station kiosk | The station screen fits a phone: tablet gauge, timer and live chart. |
| 37 | clinic-37-phone-medicines.png | Phone: my medicines | Bottles with their NEEDS LAB / PASS chip and recall check on a phone. |
| 38 | clinic-38-phone-settings-easy-mode.png | Phone: settings, Easy mode on | Easy mode on: 25 % larger words, stronger contrast, bigger buttons, and answers read aloud. |
