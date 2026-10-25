# Audio sources

## Music (lofi bed)

Both tracks come from Pixabay and are covered by the **Pixabay Content License** (https://pixabay.com/service/license-summary/):
free for commercial and non-commercial use, including YouTube; no attribution required; no permission or payment needed.
The licence forbids selling or redistributing the track on its own, unaltered, or presenting it as your own work. Using it as a background bed in a video is fine.
On the track page, neither track is marked "Content ID Registered". Pixabay tracks with that flag can trigger YouTube claims, so tracks with the flag were rejected.

| File | Title | Artist | URL | Source file | Notes |
|---|---|---|---|---|---|
| `lofi-1.mp3` → `lofi-1.wav` | Chillhop — Remain | Ornave | https://pixabay.com/music/beats-chillhop-remain-594997/ | https://cdn.pixabay.com/download/audio/2026/08/31/audio_77d8cbede6.mp3 (166.6 s, 48 kHz) | Pixabay labels it "AI generated". No Content ID. Trimmed to 148 s |
| `lofi-2.mp3` → `lofi-2.wav` | Lo-Fi Chillhop | AtlasAudio | https://pixabay.com/music/beats-lo-fi-chillhop-617588/ | https://cdn.pixabay.com/download/audio/2026/10/09/audio_b4c9ac3a5f.mp3 (143.6 s, 44.1 kHz) | No Content ID. Looped once with a 2 s crossfade at ~141.6 s, then trimmed to 148 s |

Attribution line: none required. Optional credit: `Music: "Chillhop — Remain" by Ornave / "Lo-Fi Chillhop" by AtlasAudio (Pixabay)`.

Both `.wav` files are 48 kHz stereo 24-bit and exactly 148.0 s long, with `afade=t=out:st=146.5:d=1.5`. Each was normalised with two-pass linear `loudnorm=I=-32:TP=-6:LRA=11` and measures −32.0 LUFS integrated.

## Voice (cleaned take)

`voice-clean.wav` is the original speech from `pitch/video-raw/preston-pitch-raw.mp4`. It contains no third-party audio. It is 48 kHz mono, 24-bit, 179.42 s long, and measures −16.0 LUFS integrated with a true peak of −2.7 dBTP.
The denoiser uses the RNNoise model `models/sh.rnnn` from https://github.com/richardpl/arnndn-models (`sh.rnnn`). This is a processing tool and none of its audio ends up in the video.
Filter chain (run from `fx/audio/`):

```
arnndn=m=models/sh.rnnn:mix=0.95,afftdn=nr=10:nf=-45:tn=1,highpass=f=80,lowpass=f=12000,deesser,volume=14dB,
acompressor=threshold=-20dB:ratio=2.5:attack=10:release=120,alimiter=limit=0.25:attack=3:release=60:level=false,
loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=-25.11:measured_TP=-12.04:measured_LRA=4.20:measured_thresh=-35.80:offset=0:linear=true,aresample=48000
```
