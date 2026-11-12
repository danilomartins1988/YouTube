"""Professional pt-BR "news explainer" Short (owner's personal-brand channel) from projects/<slug>/news_short.yaml.

Narration: ONE ElevenLabs /with-timestamps request for the whole script (owner's natural-voice settings; no per-sentence
splitting, no EQ/echo/tempo), cached under output/<slug>/news_v2/ and reused for every render. Captions and cuts come
from the character alignment. Music bed and SFX are synthesised locally with FFmpeg (no third-party audio).

Run:  python tools/make_pt_news_short.py projects/short-pt-cbs-prazo [--test 10.4]
"""
from __future__ import annotations

import base64
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
CH = "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell"


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw).stdout


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", str(s).lower())
    return re.sub(r"[^0-9a-z]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def voice(cfg: dict, work: Path, text: str) -> list[dict]:
    mp3, al = work / "voice_v2.mp3", work / "voice_v2_alignment.json"
    if not (mp3.exists() and al.exists()):
        v = cfg["voice"]
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{v['voice_id']}/with-timestamps",
                          headers={"xi-api-key": "proxy-injected", "Content-Type": "application/json"},
                          json={"text": text, "model_id": v["model_id"], "voice_settings": v["voice_settings"]}, timeout=300)
        r.raise_for_status()
        j = r.json()
        mp3.write_bytes(base64.b64decode(j["audio_base64"]))
        al.write_text(json.dumps(j["alignment"], ensure_ascii=False))
        print(f"synthesised {len(text)} chars")
    a = json.loads(al.read_text())
    words, cur, s0, pe = [], "", None, 0.0
    for c, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if c.isspace():
            if cur:
                words.append({"w": cur, "s": round(s0, 3), "e": round(pe, 3)})
            cur, s0 = "", None
            continue
        if s0 is None:
            s0 = s
        cur += c
        pe = e
    if cur:
        words.append({"w": cur, "s": round(s0, 3), "e": round(pe, 3)})
    return words


def main(proj: Path, test: float | None):
    cfg = yaml.safe_load((proj / "news_short.yaml").read_text())
    slug = proj.name
    work = ROOT / "output" / slug / "news_v2"
    work.mkdir(parents=True, exist_ok=True)
    segs = json.loads((work / "script_v2.json").read_text())
    words = voice(cfg, work, " ".join(segs))
    hl = {norm(w) for w in cfg.get("highlight_words", [])}
    for w in words:
        w["hl"] = norm(w["w"]) in hl
    cursor = {"i": 0}

    def at(cue: str, start_from: int = 0) -> float:
        for k in range(start_from, len(words)):
            if norm(words[k]["w"]) == norm(cue):
                return words[k]["s"], k
        raise SystemExit(f"cue {cue!r} not found after word {start_from}")

    shots, k = [], 0
    for s in cfg["shots"]:
        t, k = at(s["cue"], k)
        d = {x: y for x, y in s.items() if x != "cue"}
        d["start"] = 0.0 if not shots else t
        shots.append(d)
    for i, s in enumerate(shots):
        s["end"] = shots[i + 1]["start"] if i + 1 < len(shots) else words[-1]["e"] + 4
    overlays, k = [], 0
    for o in cfg["overlays"]:
        t, k = at(o["cue"], k)
        u, _ = at(o["until"], k)
        d = {x: y for x, y in o.items() if x not in ("cue", "until")}
        d.update(start=t, end=u)
        overlays.append(d)
    lead = cfg.get("lead", 0.35)
    total = (test if test else words[-1]["e"] + 0.6) + lead
    props = {"words": words if not test else [w for w in words if w["s"] < test], "shots": shots, "overlays": overlays,
             "lead": lead, "accent": cfg.get("accent", "#FFD23F")}
    pj = work / "props.json"
    pj.write_text(json.dumps(props, ensure_ascii=False, indent=1))
    frames = int(round(total * 30))
    silent = work / "video_silent.mp4"
    subprocess.run(["npx", "remotion", "render", "src/index.ts", "NewsShort", str(silent), f"--props={pj}",
                    f"--frames=0-{frames - 1}", "--codec=h264", "--crf=17", "--pixel-format=yuv420p", "--concurrency=4",
                    "--log=error", f"--browser-executable={CH}"], check=True, cwd=ROOT / "remotion")
    # audio: voice (delayed by lead) + synthesised music bed (soft Am-F-C-G pad, ducked) + whoosh on each cut
    cuts = [s["start"] + lead for s in shots[1:] if s["start"] + lead < total]
    pad = ("aevalsrc='0.20*(sin(2*PI*220*t)+0.7*sin(2*PI*261.63*t)+0.6*sin(2*PI*329.63*t))*(0.6+0.4*sin(2*PI*0.25*t))"
           f"':s=48000:d={total:.2f},lowpass=f=900,volume=0.10,afade=t=in:d=1.2,afade=t=out:st={max(0, total - 1.0):.2f}:d=1.0[bed]")
    sfx = "".join(f"anoisesrc=d=0.35:c=pink:a=0.5,bandpass=f=1800:w=1600,afade=t=in:d=0.12,afade=t=out:st=0.12:d=0.23,"
                  f"volume=0.22,adelay={int(c * 1000)}|{int(c * 1000)}[w{i}];" for i, c in enumerate(cuts))
    mix = ("[0:a]adelay={d}|{d},atrim=0:{T:.2f},apad=whole_dur={T:.2f},asplit=2[v][vk];".format(d=int(lead * 1000), T=total)
           + pad.replace("[bed]", "[bed0]") + ";[bed0][vk]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[bed];"
           + sfx + "[v][bed]" + "".join(f"[w{i}]" for i in range(len(cuts)))
           + f"amix=inputs={2 + len(cuts)}:normalize=0,atrim=0:{total:.2f},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]")
    wav = work / "mix.wav"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(work / "voice_v2.mp3"), "-filter_complex", mix,
         "-map", "[out]", "-c:a", "pcm_s16le", str(wav)])
    out = ROOT / "output" / ("short_pt_cbs_style_test.mp4" if test else "short_pt_cbs_prazo.mp4")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(silent), "-i", str(wav), "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)])
    print(out.relative_to(ROOT), f"{total:.1f}s")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(ROOT / a[0], float(a[a.index("--test") + 1]) if "--test" in a else None)
