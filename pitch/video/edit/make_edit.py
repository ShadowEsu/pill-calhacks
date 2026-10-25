#!/usr/bin/env python3
"""Pill pitch cut, v9-playful: generates captions.ass, captions.srt, graph.txt and build.sh from one cut list.

    python3 pitch/video/edit/make_edit.py        (no rendering; build.sh renders)

Timing comes from whisper word onsets (asr/audio16k.json: `whisper small.en --word_timestamps True` on the raw audio).
Every caption phrase starts on the onset of its first word, and every card starts on the onset of its cue word;
the wording comes from the Gemini transcript where whisper mishears (TRANSCRIPT.md).
Look: Inter Bold 84 karaoke captions (each word sweeps white → yellow as he says it, black 4-px outline, ≤ 2 lines per
cue) over a soft bottom scrim; lower-third text cards; v9: sprung pop-up stickers, doodles and alpha animations (fx/)
with soft pops, VideoFX's grade (fx/grade.txt). End card: v2's, v7 links, confetti.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
W, H = 1080, 1920
END_DUR = 4.0
CUT_D = 1 / FPS           # a "cut" is a one-frame xfade so the whole chain is one xfade/acrossfade ladder
DISS = round(8 / FPS, 3)  # 8-frame dissolve

# ── whisper word onsets ───────────────────────────────────────────────────────────────────────────
WORDS = [w for s in json.load(open(os.path.join(HERE, "asr", "audio16k.json")))["segments"] for w in s["words"]]
def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())
def onset(word, near, win=1.2):
    """Real onset (source seconds) of `word` nearest to `near`."""
    k = norm(word)
    c = [w for w in WORDS if norm(w["word"]) == k and abs(w["start"] - near) <= win]
    if not c:
        raise SystemExit(f"no whisper onset for {word!r} near {near}")
    return min(c, key=lambda w: abs(w["start"] - near))["start"]
def word_end(word, after, before):
    """End (source s) of the last `word` spoken in [after, before)."""
    k = norm(word)
    c = [w for w in WORDS if norm(w["word"]) == k and after <= w["start"] < before]
    return c[-1]["end"] if c else None

# ── cut list ──────────────────────────────────────────────────────────────────────────────────────
# src in/out = seconds of preston-pitch-raw.mp4. caps = (approx src time, phrase); the phrase starts on its first
# word's whisper onset (anchor= overrides the anchor word). join = transition INTO this cut.
CUTS = [
    # J-cut: audio 0:44.30–0:49.10 throughout; video shows him for `head` s ("So what we built is"), then cuts to the
    # station (2:05.10, purple chamber + UNO Q board) slowed to 0.75× with a subtle glow and slow push.
    dict(id="C1", name="Hook: what we built is Pill (J-cut to the hardware)", src=(44.30, 48.58), fx="hook", join=None,
         jcut=dict(head=0.90, src=125.10, speed=0.75),
         caps=[(44.50, "So what we built is Pill."), (46.66, "Pill is a hardware and software device.")]),
    dict(id="C2", name="Problem: why pills", src=(8.20, 13.60), fx="push", join=("fade", DISS), seated=True,
         caps=[(8.60, "Why are we talking about pills?"), (10.60, "Pills go through a very intense process"),
               (12.48, "with the FDA,")]),
    dict(id="C3", name="Problem: checked again, the pharmacy shelf", src=(13.80, 23.25), fx="push", join=("cut", CUT_D), seated=True,
         caps=[(14.22, "they have to go through this process several times"),
               (16.20, "before being checked out through a normal pharmacy,"), (18.48, "like Walgreens."),
               (19.84, "I got this from Walgreens: it's an aspirin 81.")]),
    dict(id="C4", name="Problem: the last step can fail", src=(27.65, 35.60), fx="push", join=("cut", CUT_D), seated=True,
         caps=[(27.66, "In the final process,"), (29.44, "some of them could be malfunctioned,"),
               (31.80, "people could have bad intentions and put different drugs in here.")]),
    # v7-long: the whole demo, 0:49.85–2:13.85 as five contiguous cuts split where the camera moves (app → cup →
    # crushing/stirring → countdown → hardware → the station's lights), each split in a pause between sentences.
    dict(id="C5", name="App: open it, the prescription, what the tablet looks like, water prompt", src=(49.85, 68.35),
         fx="push", join=("fade", DISS),
         caps=[(49.96, "Let me go through the app first."), (52.90, "If we check my medical,"),
               (56.08, "First we put in the prescription of the drug,"), (58.88, "and then we use it,"),
               (60.92, "as well as what it looks like."), (64.04, "As we click this,"),
               (65.78, "it's going to tell us to get the water inside.")]),
    dict(id="C6", name="Box: 3D-printed station, water to the mark, start, tablet in", src=(68.35, 84.40), fx="push",
         join=("cut", CUT_D),
         caps=[(68.70, "What we have in this beautifully 3D-printed device:"),
               (72.08, "we're going to put some water in there."), (74.08, "There's going to be a marking, just like so."),
               (78.16, "Perfect."), (80.34, "As I click start,"), (82.64, "I push this medicine in.", "I'm")]),
    dict(id="C7", name="Box: crush the tablet, add it, stir by hand", src=(84.40, 103.90), fx="push", join=("cut", CUT_D),
         caps=[(84.98, "First, I'm going to pound it."), (88.68, "Pounding it."),
               (93.02, "As that countdown is going,"), (94.58, "I put the medicine inside,", "I'm"),
               (97.46, "and I mix it with my hand.", "and"), (99.32, "Excuse the disturbance."), (102.38, "Perfect.")]),
    dict(id="C8", name="App: the countdown", src=(103.90, 112.45), fx="push", join=("cut", CUT_D),
         caps=[(104.28, "Alrighty, now that it's ready,"), (106.28, "we will go through the countdown."),
               (108.26, "This is going to take 60 seconds,"), (109.64, "and as I walk you through the process,"),
               (111.48, "this is going to keep going.")]),
    dict(id="C9", name="Box: the hardware", src=(112.45, 124.70), fx="push", join=("cut", CUT_D),
         caps=[(112.82, "As you see in this hardware,"), (114.46, "we use an Arduino UNO Q for the main head and CPU.", "we're"),
               (118.42, "It uses red, blue and white lights,"),
               (122.40, "as well as a photoresistor at the back.")]),
    dict(id="C10", name="Box: dark chamber, three colours, one measurement", src=(124.70, 133.85), fx="push",
         join=("cut", CUT_D),
         caps=[(125.28, "Since this is black and there are no lights inside,"),
               (129.08, "we use these three colours to find a good measurement.", "we're")]),
    dict(id="C11", name="App + box: the reading", src=(147.40, 163.40), fx="push", join=("fade", DISS),
         caps=[(147.84, "As we use the water"), (149.54, "and it does the 10-second countdown,", "and"),
               (151.54, "it goes through what is inside the water", "it"), (154.14, "and sees it as stable, variable.", "and"),
               (157.26, "And using these lights,"), (158.30, "we can find a true concentration"),
               (160.06, "of what is in the prescription"), (161.70, "and what is in the clouds.")]),
    # the ending as ONE continuous take (owner, 01:5x: "get the entire ending part … it explains why it's unable to
    # verify"): timer → check → unable to verify → the reveal → watch out → thank you, natural pauses kept, no cuts.
    # The camera is on the laptop first and on him from "because" on, so captions sit high from there (high_from).
    dict(id="C12", name="Ending, one take: Unable to verify → the reveal → thank you", src=(163.90, 179.20), fx="push",
         join=("fade", DISS), high_from=170.30,
         caps=[(164.10, "As the timer runs out,"), (166.78, "it's going to check."),
               (168.10, "And oh no: it's unable to verify."),
               (170.34, "Because guess what,"), (171.32, "I put morphine in here instead of aspirin."),
               (174.04, "So watch out."), (176.76, "Please swallow the right pills."), (178.14, "Thank you.")]),
]
END_JOIN = ("fadeblack", 0.45)
PUSH = 0.04        # slow push-in over each cut (≤ 6 %)
HOOK_PUSH = 0.06   # the hardware shot
MUSIC_LUFS = -38  # v8: a barely-there bed, 22 LU under the voice stem (voice alone -16 LUFS)
WHOOSH_GAIN = 0.12 # one soft whoosh per card entry
CAP_SIZE = 84     # Inter Bold, black 4-px outline; v8: karaoke, each word sweeps white → yellow as he says it
CAP_ML = 60
CAP_MV = 410      # v9 (EDIT-BRIEF safe zone): caption block bottom at y=1510, above the Shorts UI band
CAP_MV_HIGH = 800 # seated cuts (laptop screen in the lower third): bottom at y=1120, over his shirt, above the cards

# ── timeline ──────────────────────────────────────────────────────────────────────────────────────
for c in CUTS:
    c["dur"] = round(c["src"][1] - c["src"][0], 3)
# v9 opening (owner, 08:03): PRE s of black with "Pill" typing in and the intro card, then a fast fade into C1
PRE, PRE_JOIN = 3.5, 0.3
starts, t = [], PRE - PRE_JOIN
for i, c in enumerate(CUTS):
    if i:
        t -= c["join"][1]
    starts.append(round(t, 3)); t += c["dur"]
END_START = round(t - END_JOIN[1], 3)
TOTAL = round(END_START + END_DUR, 3)
for c, s in zip(CUTS, starts):
    c["out"] = s
BYID = {c["id"]: c for c in CUTS}
def to_out(cid, src):
    if cid == "END":
        return END_START + src
    c = BYID[cid]
    return round(c["out"] + (src - c["src"][0]), 3)
def cut_end(i):  # out time where cut i stops being the main picture
    c = CUTS[i]; nxt = CUTS[i + 1]["join"][1] if i + 1 < len(CUTS) else END_JOIN[1]
    return round(c["out"] + c["dur"] - nxt, 3)

# words cut off at a cut boundary (printed so the cut list can be fixed)
for c in CUTS:
    for w in WORDS:
        for edge in c["src"]:
            if w["start"] < edge < w["end"] - 0.05:
                print(f"WARN {c['id']}: '{w['word'].strip()}' ({w['start']:.2f}–{w['end']:.2f}) straddles {edge}")

# ── caption phrases on real onsets ────────────────────────────────────────────────────────────────
PHRASES, PHRASE_HIGH, PHRASE_CUT = [], [], []  # (out start, out end, text); caption sits high (seated cut); cut index
for i, c in enumerate(CUTS):
    caps = [(e[0], e[1], e[2] if len(e) > 2 else e[1].split()[0]) for e in c["caps"]]  # (approx, text, anchor word)
    srcs = [onset(anchor, approx) for approx, _, anchor in caps]
    hold = c["out"] + c["dur"] if i == len(CUTS) - 1 else cut_end(i)  # the last line may run into the dip to black
    for k, ((approx, text, _), s0) in enumerate(zip(caps, srcs)):
        nxt = srcs[k + 1] if k + 1 < len(srcs) else c["src"][1]
        e = word_end(text.split()[-1], s0, nxt + 0.01)
        s1 = min(nxt, (e if e else nxt) + 0.45)
        a, b = max(c["out"], to_out(c["id"], s0)), min(hold, to_out(c["id"], s1))
        b = max(b, min(a + 0.9, to_out(c["id"], nxt), hold))
        PHRASES.append((a, b, text))
        PHRASE_HIGH.append(bool(c.get("seated")) or ("high_from" in c and s0 >= c["high_from"]))
        PHRASE_CUT.append(i)

# ── cards (lower-third: 2-px purple rule + tracked caps label), all on cue-word onsets ─────────────
# card(cut, approx src, cue word, label, until=(cut, src) | None → until the next card in the slot)
def at(cid, approx, word): return to_out(cid, onset(word, approx))
CARDS = [
    (at("C6", 70.22, "3D"), "THE STATION · 3D-PRINTED CHAMBER"),
    (at("C6", 73.24, "water"), "03 · WATER TO THE MARK"),
    (at("C6", 83.30, "push"), "04 · ADD THE TABLET"),
    (at("C7", 85.72, "pound"), "CRUSH IT · STIR IT IN"),
    (at("C8", 107.40, "countdown"), "05 · DISSOLVE AND MEASURE"),
    (at("C9", 115.04, "Arduino"), "ARDUINO UNO Q · MAIN BOARD"),
    (at("C9", 119.04, "red"), "RED · BLUE · WHITE LIGHT + PHOTORESISTOR"),
    (at("C10", 129.84, "three"), "THREE COLOURS · ONE MEASUREMENT"),
    (at("C11", 149.14, "water"), "THE READING · LIGHT THROUGH THE WATER"),
]
CARDS_C5 = [(at("C5", 57.04, "prescription"), "01 · ENTER THE PRESCRIPTION"),
            (at("C5", 61.94, "looks"), "02 · WHAT THE TABLET LOOKS LIKE")]
CARDS = sorted(CARDS_C5 + CARDS)
CARD_STOPS = {  # a card holds until the next card, or until its cut ends if that comes first
    "default": [cut_end(i) for i in range(len(CUTS))]}
# the problem, as one stacked list built in time with his words (held to the end of C4)
LIST_HEAD = (at("C2", 12.88, "FDA"), "HOW A PILL REACHES YOU")
LIST = [(at("C2", 12.88, "FDA"), "01 · FDA REVIEW"),
        (at("C3", 15.58, "several"), "02 · CHECKED AGAIN, SEVERAL TIMES"),
        (at("C3", 18.06, "pharmacy"), "03 · THE PHARMACY SHELF"),
        (at("C4", 28.66, "final"), "04 · THE LAST STEP CAN FAIL")]
LIST_END = cut_end(3)
# the three answers, a restrained list with one swatch each: shown on "check", "Unable to verify" lifts on "unable"
ANS_HEAD = (at("C12", 167.10, "check"), "06 · THE ANSWER")
REVEAL = at("C12", 170.34, "because")
REVEAL_END = at("C12", 174.04, "So") + 0.45  # held into "So watch out"
REVEAL_TXT = ("THE REVEAL", "A different tablet in the Aspirin 81 bottle", "no match, no pass: Unable to verify")
HOOK_TITLE = at("C1", 45.58, "pill")

# ── captions.ass ──────────────────────────────────────────────────────────────────────────────────
PURPLE, WHITE, BLACK = "&H00FF5C7C&", "&H00FFFFFF&", "&H00000000&"
def ass_t(x):
    x = max(0.0, x); cs = int(x * 100 + 1e-6)  # floor to the centisecond: a cue never starts after its onset
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"
def wrap2(text, n=34):
    if len(text) <= n:
        return text
    best = min((abs(len(text[:m]) - len(text[m + 1:])), m) for m in range(len(text)) if text[m] == " ")[1]
    return text[:best] + r"\N" + text[best + 1:]
ev = []
def dlg(layer, a, b, style, tags, text, ml=0, mr=0, mv=0):
    ev.append(f"Dialogue: {layer},{ass_t(a)},{ass_t(b)},{style},,{ml},{mr},{mv},,{{{tags}}}{text}")
def soft(layer, a, b, style, tags, text, ml=0, mr=0, mv=0, dx=0, dy=3):
    """Crisp text over a blurred shadow copy (libass blurs the fill when there is no outline, so the shadow is a layer)."""
    sh = tags
    for m in re.finditer(r"\\(pos|move)\(([^)]*)\)", tags):
        v = [float(x) for x in m.group(2).split(",")]
        v[0] += dx; v[1] += dy
        if m.group(1) == "move":
            v[2] += dx; v[3] += dy
        sh = sh.replace(m.group(0), f"\\{m.group(1)}(" + ",".join(f"{x:g}" for x in v) + ")")
    if ml or mr or mv:  # margin-positioned (captions): shift the shadow copy by margins
        dlg(layer, a, b, style, sh + rf"\1c{BLACK}\1a&H60&\blur4", text, ml + dx, mr - dx, mv - dy)
    else:
        dlg(layer, a, b, style, sh + rf"\1c{BLACK}\1a&H60&\blur4", text)
    dlg(layer + 1, a, b, style, tags, text, ml, mr, mv)

EM = {" ": 0.26, "·": 0.32, ",": 0.32, "+": 0.67, "-": 0.40, ".": 0.30, ":": 0.30}
def textw(s, size, spacing=0):
    """Estimated advance width (Inter averages: caps 0.69 em, lowercase 0.55 em, digits 0.61 em)."""
    return sum((EM.get(ch) or (0.69 if ch.isupper() else 0.61 if ch.isdigit() else 0.55)) * size + spacing for ch in s)
# captions: yellow bold, at most 2 lines per cue: a long phrase is split into 2-line chunks, each chunk starting on its
# first word's whisper onset (proportional time if whisper has no such word). No fade-in, 80-ms fade-out. On the seated
# cuts the laptop screen fills the lower third, so their captions sit higher, over his dark shirt, above the card stack.
CAP_LINE_W = W - 2 * CAP_ML - 40
def cap_w(s): return textw(s, CAP_SIZE) * 0.74  # measured: libass draws Inter Bold at 84 ≈ 0.70 × the textw estimate
def fit_lines(ws):  # greedy line fill; number of lines `ws` needs
    n, cur = 1, []
    for w in ws:
        if cur and cap_w(" ".join(cur + [w])) > CAP_LINE_W:
            n += 1; cur = []
        cur.append(w)
    return n
def cap_chunks(text):
    """Split a phrase into the fewest cues of ≤ 2 lines, balanced by width (no one-word orphan cue)."""
    ws = text.split()
    n = 1
    while True:
        total = cap_w(text); groups, cur = [], []
        for w in ws:
            if cur and len(groups) < n - 1 and cap_w(" ".join(sum(groups, []) + cur + [w])) > total * (len(groups) + 1) / n:
                groups.append(cur); cur = []
            cur.append(w)
        groups.append(cur)
        if all(fit_lines(g) <= 2 for g in groups):
            break
        n += 1
    out = []
    for g in groups:  # balance the two lines of each cue
        t = " ".join(g)
        if cap_w(t) <= CAP_LINE_W or len(g) < 2:
            out.append((g, t)); continue
        m = min(range(1, len(g)), key=lambda m: max(cap_w(" ".join(g[:m])), cap_w(" ".join(g[m:]))))
        out.append((g, " ".join(g[:m]) + r"\N" + " ".join(g[m:])))
    return out
def karaoke(t, a, b, c):
    """Highlighter karaoke (\\ko): each word turns black on a yellow marker box (the BorderStyle-3 box) as he says it;
    unspoken words are white with no box. Words whisper doesn't
    have verbatim (caption trims like "3D-printed", "UNO Q") get times interpolated between their matched neighbours."""
    toks = [(w, li < len(t.split(r"\N")) - 1 and j == len(ln.split()) - 1)
            for li, ln in enumerate(t.split(r"\N")) for j, w in enumerate(ln.split())]
    sa, sb = c["src"][0] + a - c["out"], c["src"][0] + b - c["out"]
    times, last = [], sa - 0.35
    for w, _ in toks:
        m = next((x for x in WORDS if norm(x["word"]) == norm(w) and last <= x["start"] <= sb + 0.1), None)
        if m:
            times.append([to_out(c["id"], m["start"]), to_out(c["id"], m["end"])]); last = m["start"] + 0.01
        else:
            times.append(None)
    k = 0
    while k < len(times):  # interpolate runs of unmatched words
        if times[k] is None:
            j = k
            while j < len(times) and times[j] is None:
                j += 1
            t0 = times[k - 1][1] if k else a
            t1 = times[j][0] if j < len(times) else max(t0 + 0.3 * (j - k), min(b, t0 + 0.3 * (j - k)))
            step = max(t1 - t0, 0.1 * (j - k)) / (j - k)
            for n in range(k, j):
                times[n] = [t0 + step * (n - k), t0 + step * (n - k + 1)]
            k = j
        k += 1
    out, cur = [], 0
    base = int(a * 100 + 1e-6)  # the event start as ass_t writes it
    for n, ((w, brk), (w0, w1)) in enumerate(zip(toks, times)):
        st = max(cur, round(w0 * 100) - base)
        if st > cur:
            out.append(rf"{{\k{st - cur}}}")
        nxt = round(times[n + 1][0] * 100) - base if n + 1 < len(times) else st + 999
        d = max(5, min(round((w1 - w0) * 100), nxt - st if nxt > st else 5))
        out.append(rf"{{\ko{d}}}{w}" + (r"\N" if brk else " " if n + 1 < len(toks) else ""))
        cur = st + d
    return "".join(out)
for (a, b, text), high, ci in zip(PHRASES, PHRASE_HIGH, PHRASE_CUT):
    c, chunks = CUTS[ci], cap_chunks(text)
    starts_, pos = [a], len(" ".join(chunks[0][0])) + 1
    for ws, _ in chunks[1:]:
        guess = a + (b - a) * pos / len(text)
        src = c["src"][0] + guess - c["out"]
        cand = [w for w in WORDS if norm(w["word"]) == norm(ws[0]) and abs(w["start"] - src) <= 0.8]
        t0 = to_out(c["id"], min(cand, key=lambda w: abs(w["start"] - src))["start"]) if cand else guess
        starts_.append(min(max(t0, starts_[-1] + 0.5), b - 0.4))
        pos += len(" ".join(ws)) + 1
    for k, (_, t) in enumerate(chunks):
        e0 = starts_[k + 1] if k + 1 < len(chunks) else b
        dlg(5, starts_[k], e0, "Cap", r"\fad(0,80)", karaoke(t, starts_[k], e0, c),
            CAP_ML, CAP_ML, CAP_MV_HIGH if high else CAP_MV)
# hook title: clean serif, no halo; fades up and rises 24 px over 300 ms on the word "Pill"
soft(4, HOOK_TITLE, CUTS[0]["out"] + CUTS[0]["dur"] - 0.05, "Hook", r"\an5\move(540,524,540,500,0,300)\fad(300,200)", "Pill", dy=4)
# pre-roll: "Pill" types in on black, one letter per 4 frames, with a blinking cursor, then gives way to C1
TYPE0, TYPE_END = 0.35, PRE - PRE_JOIN
for n in range(1, 5):
    a_ = TYPE0 + (n - 1) * 4 / FPS
    b_ = TYPE0 + n * 4 / FPS if n < 4 else TYPE_END
    dlg(6, a_, b_, "Hook", r"\an4\pos(330,520)\fs260" + (r"\fad(0,250)" if n == 4 else ""), "Pill"[:n])
cx_ = 330 + round(textw("Pill", 260) * 0.62)  # cursor right after the last letter
for m in range(6):  # blinking cursor: on 0.27 s, off 0.2 s
    a_ = TYPE0 + m * 0.47
    dlg(6, a_, a_ + 0.27, "Hook", rf"\an4\pos({cx_ if m else 330 + 40},{520})\fs230\1c&H0000E5FF&", "|")
RULE = r"{\p1}m 0 0 l 96 0 96 2 0 2{\p0}"
X0 = 80
PAD = 24
PANEL_A = "&H6B&"  # black at 58 % opacity
def rrect(w, h, r=12):
    k = r * 0.552
    return (rf"{{\p1}}m {r} 0 l {w - r} 0 b {w - r + k:.1f} 0 {w} {r - k:.1f} {w} {r} l {w} {h - r} "
            rf"b {w} {h - r + k:.1f} {w - r + k:.1f} {h} {w - r} {h} l {r} {h} b {r - k:.1f} {h} 0 {h - r + k:.1f} 0 {h - r} "
            rf"l 0 {r} b 0 {r - k:.1f} {r - k:.1f} 0 {r} 0{{\p0}}")
def panel(a, b, top, w, h, fin=200, fout=160):
    """Soft dark rounded panel (12-px corners, 24-px padding, slightly blurred edge) behind a card or list."""
    dlg(2, a, b, "Rule", rf"\an7\pos({X0 - PAD},{top})\fad({fin},{fout})\1c{BLACK}\1a{PANEL_A}\blur2",
        rrect(round(w + 2 * PAD), round(h)))
def card(a, b, y, label, style="Label", rule=True, with_panel=True):
    if with_panel:
        panel(a, b, y - PAD, max(96, textw(label, 30, 4)), 14 + 34 + 2 * PAD)
    if rule:
        dlg(3, a, b, "Rule", rf"\an7\move({X0 - 40},{y},{X0},{y},0,200)\fad(200,160)\1c{PURPLE}", RULE)
    soft(4, a, b, style, rf"\an7\move({X0 - 24},{y + 14},{X0},{y + 14},0,200)\fad(200,160)", label, dy=2)
# single-slot cards at the lower third (above the caption block); a card holds at most CARD_MAX s on the long cuts
CARD_MAX = 5.0
for k, (a, label) in enumerate(CARDS):
    stop = min(x for x in CARD_STOPS["default"] if x > a + 0.3)
    b = min(stop, CARDS[k + 1][0], a + CARD_MAX) if k + 1 < len(CARDS) else min(stop, a + CARD_MAX)
    card(a, b, 1180, label)
# the problem list
# the problem list: one panel that grows a row at a time (fixed width so it doesn't jitter)
card(LIST_HEAD[0], LIST_END, 1150, LIST_HEAD[1], style="ListHead", with_panel=False)
lw = max(textw(l, 30, 4) for _, l in LIST)
for k, (a, label) in enumerate(LIST):
    nxt = LIST[k + 1][0] if k + 1 < len(LIST) else LIST_END
    panel(a, nxt, 1150 - PAD, lw, (1196 + 52 * k + 34) - 1150 + 2 * PAD, fin=200 if k == 0 else 0, fout=160 if k == len(LIST) - 1 else 0)
    soft(4, a, LIST_END, "Label", rf"\an7\move({X0 - 24},{1196 + 52 * k},{X0},{1196 + 52 * k},0,200)\fad(200,160)", label, dy=2)
# the three answers are the answers-bounce animation in v9 (see the overlay layer); a0 keeps their whoosh
a0 = ANS_HEAD[0]
# the reveal: header + line + sub on one panel, same place as the answers list
card(REVEAL, REVEAL_END, 1150, REVEAL_TXT[0], with_panel=False)
panel(REVEAL, REVEAL_END, 1150 - PAD, max(textw(REVEAL_TXT[1], 36), textw(REVEAL_TXT[2], 28)), (1258 + 34) - 1150 + 2 * PAD)
soft(4, REVEAL, REVEAL_END, "Reveal", rf"\an7\move({X0 - 24},{1208},{X0},{1208},0,200)\fad(200,160)", REVEAL_TXT[1], dy=2)
soft(4, REVEAL, REVEAL_END, "RevealSub", rf"\an7\move({X0 - 24},{1258},{X0},{1258},0,200)\fad(200,160)", REVEAL_TXT[2], dy=2)
# end card text (v2 layout; v7 links: the domain + the hackathon repo)
for (dy_, txt, st, d0) in ((880, "The box measures. Pill explains.", "CardSerif", 0.4),
                           (1500, "pillmeifyoucan.health", "Card", 1.2), (1590, "github.com/ShadowEsu/pill-calhacks", "Card", 1.4)):
    dlg(1, END_START + d0, TOTAL, st, rf"\an5\pos(540,{dy_})\fad(150,0)\fscx90\fscy90\t(0,160,\fscx100\fscy100)", txt)

ASS = f"""[Script Info]
; generated by make_edit.py — do not hand-edit, edit make_edit.py and re-run
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Bold,{CAP_SIZE},&H00000000,&H00FFFFFF,&H0000E5FF,&H00000000,0,0,0,0,100,100,0,0,3,10,0,2,{CAP_ML},{CAP_ML},{CAP_MV},1
Style: Hook,Instrument Serif,200,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,40,40,0,1
Style: Label,Inter SemiBold,30,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,4,0,1,0,0,7,0,0,0,1
Style: ListHead,Inter SemiBold,24,&H33FFFFFF,&H33FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,6,0,1,0,0,7,0,0,0,1
Style: Answer,Inter Medium,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Reveal,Inter Medium,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: RevealSub,Inter Medium,28,&H26FFFFFF,&H26FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Rule,Inter Medium,20,&H00FF5C7C,&H00FF5C7C,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: CardSerif,Instrument Serif,96,&H00111111,&H00111111,&H00E6EFF4,&H00000000,0,1,0,0,100,100,0,0,1,0,0,5,60,60,0,1
Style: Card,Inter,58,&H00111111,&H00111111,&H00E6EFF4,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n"
open(os.path.join(HERE, "captions.ass"), "w").write(ASS)

# ── build.sh ──────────────────────────────────────────────────────────────────────────────────────
inputs, fc = [], []
for c in CUTS:
    inputs.append(f'-ss {c["src"][0]:.3f} -t {c["dur"]:.3f} -i "$SRC"')
NC = len(CUTS)
iEND, iSIL, iMUS, iHW = NC, NC + 1, NC + 2, NC + 3
JC = CUTS[0]["jcut"]
iPV, iPA = iHW + 1, iHW + 2  # the black pre-roll (video, silence)
inputs += [f'-f lavfi -t {END_DUR} -i "color=c=0xF4EFE6:s={W}x{H}:r={FPS}"',
           f'-f lavfi -t {END_DUR} -i "anullsrc=r=48000:cl=stereo"', '-i "$MUSIC"',
           f'-ss {JC["src"]:.3f} -t {(CUTS[0]["dur"] - JC["head"]) * JC["speed"]:.3f} -i "$SRC"',
           f'-f lavfi -t {PRE} -i "color=c=black:s={W}x{H}:r={FPS}"', f'-f lavfi -t {PRE} -i "anullsrc=r=48000:cl=stereo"']
GRADE = open(os.path.join(HERE, "fx", "grade.txt")).read().strip()  # VideoFX's tested grade, after the scale to 1080x1920
BASE = f"fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1"
# Every segment is forced to its exact nominal length (clone-pad the last frame, then trim): the 31.58-fps VFR source
# otherwise loses a frame here and there, a later xfade offset lands past its input's end and the video stops early.
def fit(d): return f"tpad=stop_mode=clone:stop_duration=2,trim=duration={d:.3f},setpts=PTS-STARTPTS"
def afit(d): return f"apad=whole_dur={d:.3f},atrim=duration={d:.3f},asetpts=PTS-STARTPTS"
def push(p, d): return (f"scale=w='trunc({W}*(1+{p}*t/{d:.3f})/2)*2':h=-2:eval=frame:flags=bicubic,crop={W}:{H},setsar=1")
for i, c in enumerate(CUTS):
    if c["fx"] == "hook":  # him for `head` s, then the slowed hardware shot: slow push, subtle glow, soft vignette
        hw = round(c["dur"] - JC["head"], 3)
        fc.append(f"[{i}:v]trim=0:{JC['head']:.3f},setpts=PTS-STARTPTS,{BASE},{GRADE},format=yuv420p,{fit(JC['head'])},settb=1/{FPS}[hd]")
        fc.append(f"[{iHW}:v]setpts=(PTS-STARTPTS)/{JC['speed']},{BASE},{push(HOOK_PUSH, hw)},format=gbrp,split=2[h0][h1]")
        fc.append("[h1]gblur=sigma=28[hg]")
        fc.append("[h0][hg]blend=all_mode=screen:all_opacity=0.25,eq=contrast=1.06:saturation=1.12,"
                  f"vignette=angle=PI/4.5,format=yuv420p,{fit(hw)},settb=1/{FPS}[hw]")
        fc.append(f"[hd][hw]concat=n=2:v=1:a=0,{fit(c['dur'])},settb=1/{FPS}[v{i}]")
    else:
        fc.append(f"[{i}:v]{BASE},{push(PUSH, c['dur'])},{GRADE},format=yuv420p,{fit(c['dur'])},settb=1/{FPS}[v{i}]")
    fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=90,afftdn=nr=10,asetpts=PTS-STARTPTS,{afit(c['dur'])}[a{i}]")
fc.append(f"[{iEND}:v]format=yuv420p,setsar=1,{fit(END_DUR)},settb=1/{FPS}[v{NC}]")
fc.append(f"[{iSIL}:a]aformat=channel_layouts=stereo,{afit(END_DUR)}[a{NC}]")
joins = [c["join"] for c in CUTS[1:]] + [END_JOIN]
segstarts = starts[1:] + [END_START]
fc.append(f"[{iPV}:v]format=yuv420p,setsar=1,{fit(PRE)},settb=1/{FPS}[vpre]")
fc.append(f"[{iPA}:a]aformat=channel_layouts=stereo,{afit(PRE)}[apre]")
fc.append(f"[vpre][v0]xfade=transition=fade:duration={PRE_JOIN}:offset={PRE - PRE_JOIN:.3f}[xp]")
fc.append(f"[apre][a0]acrossfade=d={PRE_JOIN}:c1=tri:c2=tri[yp]")
pv, pa = "[xp]", "[yp]"
for k, ((tr, d), off) in enumerate(zip(joins, segstarts), start=1):
    trn = "fade" if tr == "cut" else tr
    nv, na = f"[x{k}]", f"[y{k}]"
    fc.append(f"{pv}[v{k}]xfade=transition={trn}:duration={d:.3f}:offset={off:.3f}{nv}")
    fc.append(f"{pa}[a{k}]acrossfade=d={d:.3f}:c1=tri:c2=tri{na}")
    pv, pa = nv, na
# soft bottom scrim under captions and cards (one generated frame, looped), off for the end card
SCRIM_Y, SCRIM_H = 980, H - 980
fc.append(f"color=c=black:s={W}x{SCRIM_H}:r={FPS}:d=0.04,format=rgba,"
          f"geq=r='0':g='0':b='0':a='185*pow(min(Y/({SCRIM_H}*0.36),1),2)*(3-2*min(Y/({SCRIM_H}*0.36),1))',"
          f"loop=loop=-1:size=1:start=0,trim=duration={END_START:.3f},setpts=N/{FPS}/TB[scrim]")
# screen shake on "pound"/"pounding" (owner: "crush/pound → screen shake"): a 3 % crop that jitters for 0.3 s
SHAKES = [to_out(c["id"], w["start"]) for c in CUTS for w in WORDS
          if norm(w["word"]) in ("pound", "pounding") and c["src"][0] <= w["start"] < c["src"][1]]
S = "+".join(f"between(t,{T:.3f},{T + 0.3:.3f})*exp(-(t-{T:.3f})*10)" for T in SHAKES) or "0"
fc.append(f"{pv}crop=w=1048:h=1862:x='16+16*({S})*sin(t*95)':y='29+22*({S})*cos(t*83)',scale={W}:{H}:flags=bicubic,setsar=1[vsh]")
fc.append(f"[vsh][scrim]overlay=x=0:y={SCRIM_Y}:eof_action=pass:format=auto[vs]")
vcur = "[vs]"
# v9 playful layer (owner, 07:57: "bring back … the stickers, and upgrade it"): v2's pop-up stickers on the v7 cut list,
# VideoFX's doodles (fx/placements.json: centre x/y, t_in seconds into the cut) and PillRain's alpha animations.
# Every sticker springs in (55 % → 100 % with a damped overshoot and a small drop) and gets a soft pop at -18 dB.
def png_size(p):
    with open(p, "rb") as f:
        head = f.read(24)
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")
STK = {"answer-passed": (900, 204, 62, 410), "answer-lab": (900, 204, 62, 410), "answer-unable": (900, 204, 62, 410),
       "chip-unoq": (700, 204, 162, 410), "chip-402": (1000, 204, 10, 410), "chip-box": (760, 204, 130, 410),
       "chip-explains": (620, 204, 200, 410), "pill": (600, 600, 212, 212), "ring": (800, 600, 112, 212),
       "arrow": (500, 500, 262, 262)}
for f in sorted(os.listdir(os.path.join(HERE, "stickers"))):
    if f.startswith("pop-") and f.endswith(".png"):
        STK[f[:-4]] = png_size(os.path.join(HERE, "stickers", f)) + (0, 0)
SAFE = (48, 120, 930, 1540)  # EDIT-BRIEF: keep overlays out of the Shorts UI (right 150 px, bottom ~380 px)
OVL = []  # dict(T0, dur, path, crop, wd, x, y, alpha, mov)
def P(cid, st, name, y, h, x=None, dur=None, to=None, alpha=1.0):
    cw, ch, ox, oy = STK[name]
    wd = round(h * cw / ch / 2) * 2
    x = (W - wd) // 2 if x is None else x
    x, y = max(SAFE[0], min(x, SAFE[2] - wd)), max(SAFE[1], min(y, SAFE[3] - h))
    T0 = to_out(cid, st) if cid != "END" else round(END_START + st, 3)
    OVL.append(dict(T0=T0, dur=round((to_out(*to) - T0) if to else dur, 2), path=f"stickers/{name}.png", crop=(cw, ch, ox, oy),
                    wd=wd, hd=h, x=x, y=y, alpha=alpha, mov=False))
def FX(cid, t_in, path, cx, cy, scale, dur):  # fx/placements.json: centre x/y, t_in s into the cut, 2× PNGs (size = scale/2)
    pw, ph = png_size(os.path.join(HERE, path))
    wd, h = round(pw * scale / 4) * 2, round(ph * scale / 2)
    x, y = cx - wd // 2, cy - h // 2
    x, y = max(SAFE[0], min(x, SAFE[2] - wd)), max(SAFE[1], min(y, SAFE[3] - h))
    OVL.append(dict(T0=round(BYID[cid]["out"] + t_in, 3), dur=dur, path=path, crop=(pw, ph, 0, 0), wd=wd, hd=h, x=x, y=y,
                    alpha=1.0, mov=False))
def MOV(T0, path, x, y, dur, scale=None, tint=False):  # pre-rendered alpha animation (ProRes 4444), played once from T0
    OVL.append(dict(T0=round(T0, 3), dur=dur, path=path, x=x, y=y, scale=scale, tint=tint, mov=True))
MOV(1.00, "fx/anim/intro-card.mov", 0, 0, 2.5)  # pre-roll: "One tablet. One curve. One answer." under the typed "Pill"
P("C2", 8.40, "pop-think", y=200, h=220, x=700, dur=1.8)
P("C3", 19.90, "pill", y=560, h=300, x=600, dur=3.2)
P("C5", 56.00, "pop-step1", y=150, h=110, to=("C5", 59.00))
P("C5", 59.04, "pop-step2", y=150, h=110, to=("C5", 63.40))
P("C5", 64.04, "chip-402", y=420, h=110, dur=3.2)
P("C6", 68.60, "pop-3d", y=320, h=130, x=60, dur=3.8)
P("C6", 72.50, "pop-step3", y=150, h=110, to=("C6", 77.55))
P("C6", 73.40, "pop-drop", y=420, h=200, x=720, dur=2.0)
P("C6", 74.80, "arrow", y=760, h=360, x=560, dur=2.6)
P("C6", 80.16, "pop-step4", y=150, h=110, to=("C6", 84.35))
P("C6", 81.20, "pop-eyes", y=330, h=200, x=700, dur=2.0)
MOV(to_out("C6", 83.30), "fx/anim/sparkle-burst.mov", 540 - 300, 860 - 300, 1.5)  # "I push this medicine in"
P("C8", 104.26, "pop-step5", y=150, h=110, to=("C8", 108.70))
MOV(to_out("C8", 108.84), "fx/anim/countdown-ring.mov", 430, 140, 3.6)  # "this is going to take 60 seconds"
P("C8", 104.30, "ring", y=735, h=270, x=410, dur=3.2)  # round the dial on the laptop
P("C9", 112.60, "chip-unoq", y=300, h=136, x=240, dur=5.2)
P("C9", 117.90, "pop-lights", y=330, h=120, x=60, to=("C9", 124.65))
P("C10", 125.30, "chip-box", y=420, h=110, dur=3.4)
P("C10", 128.90, "pop-measure", y=330, h=130, to=("C10", 133.80))
P("C11", 157.26, "chip-explains", y=420, h=110, dur=3.5)
P("C12", 164.40, "pop-eyes", y=380, h=200, x=700, dur=2.6)
MOV(to_out("C12", 168.10), "fx/anim/answers-bounce.mov", 120, 690, 3.0)  # the three answers as he reads the result
P("C12", 168.60, "pop-grimace", y=120, h=170, x=455, dur=2.6)
P("C12", 175.80, "pill", y=380, h=280, x=600, dur=2.4)
for e in json.load(open(os.path.join(HERE, "fx", "placements.json"))):  # the 60-s ring and the 402 chip are placed above
    if e["cut"] in BYID and not e["sticker"].endswith(("badge-x402.png", "badge-60s.png")):
        FX(e["cut"], e["t_in"], e["sticker"], e["x"], e["y"], e["scale"], e["dur"])
# "interactive every second" (owner, 08:03; WordTriggers' fx/words/triggers.json, word onsets + overlay top-left xy):
# a pill pop on every pill/tablet/medicine word, "magic water" on the cup on every "water", a white hit on "pound"
TRIG = [e for e in json.load(open(os.path.join(HERE, "fx", "words", "triggers.json")))["triggers"] if e["cut_id"] in BYID]
PILL_POPS, WATER = [], []
for e in TRIG:
    T = to_out(e["cut_id"], e["raw_t"])
    if e["cls"] == "pill" and e["cut_id"] != "C1":  # C1 has the "Pill" title
        MOV(T, "fx/words/pill-pop.mov", *e["xy"], 0.8); PILL_POPS.append(T)
    elif e["cls"] == "water":
        MOV(T, "fx/words/water-magic.mov", *e["xy"], 1.2); WATER.append(T)
    elif e["cls"] == "crush":
        MOV(T, "fx/words/shake-flash.mov", 0, 0, 0.27)
MOV(to_out("C9", 115.04), "fx/anim/arrow-point.mov", 520 - 62, 1150 - 338, 1.5)  # "Arduino": tip on the board
MOV(END_START + 0.4, "fx/anim/pill-rain.mov", 0, 0, 3.5)
P("END", 0.30, "pill", y=360, h=420, x=330, dur=3.7)
P("END", 0.90, "pop-end", y=1240, h=120, dur=3.1)
MOV(END_START, "fx/anim/confetti.mov", 0, 0, 3.0)
OVL.sort(key=lambda o: o["T0"])
pop_inputs = []
for j, o in enumerate(OVL):
    idx, T0, dur = iPA + 1 + j, o["T0"], o["dur"]
    if o["mov"]:
        pop_inputs.append(f'-i {o["path"]}')
        sc = f"scale={o['scale']}:{o['scale']}," if o.get("scale") else ""
        tn = "colorchannelmixer=rr=0:rb=1:br=1:bb=0," if o.get("tint") else ""  # yellow sparkle → cyan-blue "magic water"
        fc.append(f"[{idx}:v]format=rgba,{sc}{tn}setpts=PTS-STARTPTS+{T0}/TB[p{j}]")
        fc.append(f"{vcur}[p{j}]overlay=x={o['x']}:y={o['y']}:eof_action=pass:enable='between(t,{T0},{T0 + dur:.3f})'[o{j}]")
    else:
        cw, ch, ox, oy = o["crop"]
        wd, x, y, hd = o["wd"], o["x"], o["y"], o["hd"]
        al = f",colorchannelmixer=aa={o['alpha']}" if o["alpha"] < 1 else ""
        pop_inputs.append(f'-loop 1 -framerate {FPS} -t {dur:.2f} -i {o["path"]}')
        fc.append(f"[{idx}:v]format=rgba,crop={cw}:{ch}:{ox}:{oy},"
                  f"scale=w='trunc({wd}*(1-0.45*exp(-t*8)*cos(t*22))/2)*2':h=-2:eval=frame:flags=bicubic{al},"
                  f"fade=t=in:st=0:d=0.10:alpha=1,fade=t=out:st={dur - 0.18:.2f}:d=0.18:alpha=1,setpts=PTS-STARTPTS+{T0}/TB[p{j}]")
        fc.append(f"{vcur}[p{j}]overlay=x='{x}+({wd}-overlay_w)/2':y='{y}+({hd}-overlay_h)/2+40*exp(-(t-{T0})*10)*cos((t-{T0})*18)':"
                  f"eval=frame:enable='between(t,{T0},{T0 + dur:.3f})':eof_action=pass[o{j}]")
    vcur = f"[o{j}]"
fc.append(f"{vcur}ass=captions.ass:fontsdir=fonts,format=yuv420p[vout]")
# audio (v8, owner: "I can't hear myself, the music is too loud"): the voice is the master, normalised alone to
# -16 LUFS; the score sits under it at -38 LUFS (22 LU down) and ducks about 6 dB more while he speaks; soft whoosh per
# card entry. The full mix is normalised to -16 LUFS, TP -1.5 dBTP (YouTube level).
# sfx at about -18 dB under the -16 LUFS voice: a pop on every sticker, a whoosh on each card entry, uh-oh on "oh no",
# a ding on the end card (make_music.py writes sfx/*.wav)
SFX_GAIN = {"pop": 0.13, "whoosh": WHOOSH_GAIN, "uhoh": 0.16, "ding": 0.14}
sfx_ev = [("whoosh", max(0.0, t - 0.12)) for t in
          sorted({round(a, 3) for a, _ in CARDS} | {round(LIST_HEAD[0], 3), round(a0, 3), round(REVEAL, 3)})]
sfx_ev += [("pop", o["T0"]) for o in OVL if not o["mov"]] + [("uhoh", to_out("C12", 168.50)), ("ding", END_START + 0.30)]
sfx_ev += [("thud", T) for T in SHAKES] + [("plop", to_out("C6", 83.46))] + [("water", T - 0.05) for T in WATER]
sfx_ev += [("pop", T) for T in PILL_POPS]
SFX_GAIN.update({"thud": 0.15, "plop": 0.18, "water": 0.14})
SFX = [s for s in SFX_GAIN if any(n == s for n, _ in sfx_ev)]
iSFX = iPA + 1 + len(OVL)
fc.append(f"{pa}loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,asplit=2[vo][vsc]")
fc.append(f"[{iMUS}:a]atrim=0:{TOTAL},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
          f"loudnorm=I={MUSIC_LUFS}:TP=-9:LRA=11,aresample=48000,"
          f"afade=t=in:st=0:d=0.3,afade=t=out:st={TOTAL - 1.6:.2f}:d=1.6[mu]")
fc.append("[mu][vsc]sidechaincompress=threshold=0.04:ratio=3:attack=20:release=300:makeup=1[duck]")
sfx_labels = []
for k, s in enumerate(SFX):
    evs = [t for n, t in sfx_ev if n == s]
    fc.append(f"[{iSFX + k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={SFX_GAIN[s]},asplit={len(evs)}"
              + "".join(f"[{s}{m}]" for m in range(len(evs))))
    for m, t0 in enumerate(evs):
        ms = int(round(t0 * 1000))
        fc.append(f"[{s}{m}]adelay={ms}|{ms}[{s}d{m}]"); sfx_labels.append(f"[{s}d{m}]")
fc.append("".join(sfx_labels) + f"amix=inputs={len(sfx_labels)}:normalize=0:duration=longest[sfx]")
# the brick-wall limiter after loudnorm keeps the sfx transients under -1.5 dBTP after AAC (v10 first render: +0.4 dBTP)
fc.append("[vo][duck][sfx]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=192000,"
          "alimiter=limit=0.75:attack=1:release=50:level=disabled,aresample=48000[aout]")

graph = ";\n".join(fc)
open(os.path.join(HERE, "graph.txt"), "w").write(graph + "\n")
ins = " \\\n  ".join(inputs + pop_inputs + [f"-i sfx/{s}.wav" for s in SFX])
BUILD = f"""#!/usr/bin/env bash
# Pill pitch cut v10-interactive: {NC} cuts + {END_DUR:.0f}-s end card = {TOTAL:.2f} s, 1080x1920 (source is portrait: 1024x576 with -90° rotation).
# Generated by make_edit.py (edit the cut list there, re-run it, never hand-edit the graph).
#   bash pitch/video/edit/build.sh            full render  -> pitch/video/pill-pitch-v10-interactive.mp4
#   bash pitch/video/edit/build.sh --preview  seconds 0-10 -> pitch/video/pill-pitch-preview10.mp4
#   bash pitch/video/edit/build.sh --check    filtergraph dry run: 0.1 s to the null muxer, no encode
set -euo pipefail
cd "$(dirname "$0")"
SRC=../../video-raw/preston-pitch-raw.mp4
MUSIC=${{MUSIC:-work/music-long.wav}}   # original score synthesised by make_music.py (116 BPM), no licence needed
FF=${{FFMPEG:-bin/ffmpeg}}          # needs libass (the 'ass' filter); Homebrew's ffmpeg 8.1.2 has none
if ! "$FF" -hide_banner -filters 2>/dev/null | grep ' ass ' >/dev/null; then
  echo "fetching a static ffmpeg with libass into bin/ (martin-riedl.de, macOS arm64)"
  mkdir -p bin && curl -sSfL -o bin/ffmpeg.zip https://ffmpeg.martin-riedl.de/redirect/latest/macos/arm64/release/ffmpeg.zip
  (cd bin && unzip -o -q ffmpeg.zip && rm ffmpeg.zip && chmod +x ffmpeg && xattr -c ffmpeg 2>/dev/null || true)
  FF=bin/ffmpeg
fi
[ -f "$MUSIC" ] && [ -f sfx/whoosh.wav ] || {{ echo "missing $MUSIC or sfx/whoosh.wav: run .venv/bin/python make_music.py {int(TOTAL) + 5} && mv work/music-fun.wav $MUSIC"; exit 1; }}
[ -f fonts/Inter-Medium.ttf ] && [ -f fonts/Inter-SemiBold.ttf ] && [ -f fonts/Inter-Bold.ttf ] || {{ echo "missing static Inter: run .venv/bin/python make_fonts.py"; exit 1; }}
MODE=${{1:-full}}
case "$MODE" in
  --preview) OUTARGS=(-t 10 -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart ../pill-pitch-preview10.mp4) ;;
  --check)   OUTARGS=(-t 0.1 -f null -) ;;
  full)      OUTARGS=(-c:v libx264 -preset medium -crf 20 -profile:v high -pix_fmt yuv420p -r {FPS} -c:a aac -b:a 192k -ar 48000 -movflags +faststart ../pill-pitch-v10-interactive.mp4) ;;
  *) echo "usage: build.sh [--preview|--check]"; exit 2 ;;
esac
"$FF" -hide_banner -y -nostdin \\
  {ins} \\
  -/filter_complex graph.txt \\
  -map "[vout]" -map "[aout]" "${{OUTARGS[@]}}"
[ "$MODE" = --check ] || ls -la ../pill-pitch-*.mp4
"""
open(os.path.join(HERE, "build.sh"), "w").write(BUILD)
os.chmod(os.path.join(HERE, "build.sh"), 0o755)

# ── captions.srt (same phrases, for YouTube/Devpost upload) ─────────────────────────────────────────
def srt_t(x):
    ms = int(round(x * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
with open(os.path.join(HERE, "captions.srt"), "w") as f:
    for k, (a, b, text) in enumerate(PHRASES + [(END_START + 0.9, TOTAL, "pillmeifyoucan.health")], 1):
        f.write(f"{k}\n{srt_t(a)} --> {srt_t(b)}\n{wrap2(text).replace(chr(92) + 'N', chr(10))}\n\n")

# ── table for EDIT-PLAN.md ─────────────────────────────────────────────────────────────────────────
def mmss(x): return f"{int(x // 60)}:{x % 60:05.2f}"
print("| # | Out in–out | Source in–out | Dur | Transition in | Captions (phrase starts on the first word's onset) |")
print("|---|---|---|---|---|---|")
for c in CUTS:
    j = "—" if not c["join"] else ("cut" if c["join"][0] == "cut" else f'dissolve {round(c["join"][1] * FPS)} fr')
    print(f'| {c["id"]} {c["name"]} | {mmss(c["out"])}–{mmss(c["out"] + c["dur"])} | {mmss(c["src"][0])}–{mmss(c["src"][1])} | '
          f'{c["dur"]:.2f} | {j} | ' + " / ".join(e[1] for e in c["caps"]) + " |")
print(f"| END card | {mmss(END_START)}–{mmss(TOTAL)} | generated | {END_DUR:.2f} | dip to black {END_JOIN[1]:.2f}s | The box measures. Pill explains. / pillmeifyoucan.health / github.com/ShadowEsu/pill-calhacks |")
print(f"TOTAL {TOTAL:.2f}s; {len(PHRASES)} caption phrases; {len(ev)} ASS events")
print("CARDS:", [(round(a, 2), l) for a, l in CARDS])
print("LIST:", [(round(a, 2), l) for a, l in LIST], "ANSWERS at", round(a0, 2), "TITLE", round(HOOK_TITLE, 2))
print("OVERLAYS:", [(round(o["T0"], 2), o["path"].split("/")[-1]) for o in OVL])
print("PHRASES:", [(round(a, 2), round(b, 2), t[:24]) for a, b, t in PHRASES])
