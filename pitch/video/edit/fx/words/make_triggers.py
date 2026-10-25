#!/usr/bin/env python3
"""Per-word overlay triggers: raw-take whisper words → cut-relative and output times (C1 frame 0 = 0)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
EDIT = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(EDIT, "make_edit.py")).read()
ns = {}
exec(src[src.index("FPS ="):src.index("# ── whisper")] if "FPS =" in src else "FPS=30", ns)
FPS = ns.get("FPS", 30)
CUT_D, DISS = 1 / FPS, round(8 / FPS, 3)
blk = src[src.index("CUTS = ["):src.index("END_JOIN")]
exec(blk, {"CUT_D": CUT_D, "DISS": DISS}, ns)
CUTS = ns["CUTS"]
starts, t = [], 0.0
for i, c in enumerate(CUTS):
    c["dur"] = round(c["src"][1] - c["src"][0], 3)
    if i: t -= c["join"][1]
    starts.append(round(t, 3)); t += c["dur"]
WORDS = [w for s in json.load(open(os.path.join(EDIT, "asr", "audio16k.json")))["segments"] for w in s["words"]]
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
CLS = {"pill": "pill", "pills": "pill", "tablet": "pill", "tablets": "pill", "medicine": "pill",
       "water": "water", "crush": "crush", "pound": "crush", "crushing": "crush", "pounding": "crush",
       "drop": "drop", "inside": "drop", "arduino": "hardware", "board": "hardware", "sensor": "hardware",
       "led": "hardware", "hardware": "hardware", "photoresistor": "hardware", "cpu": "hardware", "leds": "hardware", "light": "hardware", "lights": "hardware",
       "seconds": "countdown", "countdown": "countdown", "result": "result", "verify": "result", "unable": "result"}
out = []
for k, w in enumerate(WORDS):
    n = norm(w["word"]); cls = CLS.get(n); word = w["word"].strip(" ,.!?")
    if n == "put" and [norm(x["word"]) for x in WORDS[k + 1:k + 3]] == ["it", "in"]:
        cls, word = "drop", "put it in"
    if not cls: continue
    for c, s in zip(CUTS, starts):
        a, b = c["src"]
        if a <= w["start"] < b:
            tc = round(w["start"] - a, 3)
            out.append(dict(word=word, cls=cls, raw_t=round(w["start"], 3), cut_id=c["id"], t_in_cut=tc,
                            t_in_video=round(s + tc, 3)))
out.sort(key=lambda e: e["t_in_video"])
# suggested overlay top-left (output px, 1080x1920). pill-pop 300x300 on his hand side, y varied per occurrence;
# water-magic 500x500 centred on the cup (frame reads: C5 the on-screen cup icon, C6/C11 the printed chamber)
CUP = {67.24: (370, 893), 73.24: (362, 1033), 149.14: (186, 1290), 153.9: (152, 1450)}
k = 0
for e in out:
    if e["cls"] == "pill":
        e["xy"] = [(640, 700, 760)[k % 3], 600 + (k * 130) % 301]; k += 1
    elif e["cls"] == "water":
        cx, cy = CUP[e["raw_t"]]; e["xy"] = [cx - 250, cy - 250]
meta = {"note": "t_in_video is relative to the first frame of C1 (add any pre-roll); t_in_cut from CUTS src in make_edit.py; "
        "raw_t = whisper word onset in preston-pitch-raw.mp4",
        "cut_starts": {c["id"]: s for c, s in zip(CUTS, starts)},
        "counts": {k: sum(e["cls"] == k for e in out) for k in dict.fromkeys(CLS.values())}}
json.dump(dict(meta=meta, triggers=out), open(os.path.join(HERE, "triggers.json"), "w"), indent=1)
print(len(out), meta["counts"])
for e in out: print(e)
