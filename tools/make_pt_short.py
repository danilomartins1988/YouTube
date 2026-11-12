"""Kinetic-typography Short in Brazilian Portuguese for the owner's personal-brand channel (no characters, no avatar:
"um vídeo apenas com textos e minha voz"). Not The Hidden Economics: no channel name or intro.

1. Narration: the owner's own cloned voice on ElevenLabs (voice/model/settings from the project's tts_overrides.elevenlabs),
   one request per segment to /with-timestamps (character alignment -> word timings). Cached per (voice, settings, text):
   re-running never re-synthesises unchanged text. The API key is injected by the network proxy (never read here).
2. Words + beats (big keyword blocks cued to words) -> Remotion composition `KineticShort` (1080x1920, silent).
3. FFmpeg muxes the narration (with gaps) under the video, plus a 3 s disclaimer end card already in the composition.

Run: python tools/make_pt_short.py projects/short-pt-cbs-prazo
"""
from __future__ import annotations

import base64
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
GAP = 0.32          # silence between segments (s)
LEAD = 0.25         # silence before the first word
END_CARD = 3.2      # disclaimer card (s)


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def synth(text: str, o: dict, cache: Path) -> tuple[Path, list[dict]]:
    key = hashlib.sha256(json.dumps([o.get("voice_id"), o.get("model_id"), o.get("voice_settings"), o.get("language_code"), text],
                                    sort_keys=True).encode()).hexdigest()[:20]
    mp3, js = cache / f"{key}.mp3", cache / f"{key}.json"
    if not (mp3.exists() and js.exists()):
        body = {"text": text, "model_id": o.get("model_id", "eleven_multilingual_v2")}
        if o.get("voice_settings"):
            body["voice_settings"] = o["voice_settings"]
        if o.get("language_code"):
            body["language_code"] = o["language_code"]
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{o['voice_id']}/with-timestamps",
                          headers={"xi-api-key": "proxy-injected", "Content-Type": "application/json"}, json=body, timeout=180)
        r.raise_for_status()
        j = r.json()
        mp3.write_bytes(base64.b64decode(j["audio_base64"]))
        js.write_text(json.dumps(j.get("alignment") or j.get("normalized_alignment")), encoding="utf-8")
        print(f"  synthesised {len(text)} chars")
    al = json.loads(js.read_text())
    chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    words, cur, a = [], "", None
    for c, s, e in zip(chars, st, en):
        if c.isspace():
            if cur:
                words.append({"w": cur, "s": a, "e": prev_e})
            cur, a = "", None
            continue
        if not cur:
            a = s
        cur += c
        prev_e = e
    if cur:
        words.append({"w": cur, "s": a, "e": prev_e})
    return mp3, words


def main(proj: Path):
    p = yaml.safe_load((proj / "project.yaml").read_text())
    o = p["tts_overrides"]["elevenlabs"]
    sc = yaml.safe_load((proj / "deliverables/documentary/script.yaml").read_text())
    beats = yaml.safe_load((proj / "beats.yaml").read_text())
    work = ROOT / "output" / p["slug"]
    cache = work / "tts_cache"
    cache.mkdir(parents=True, exist_ok=True)
    words, segs, t, parts = [], [], LEAD, []
    for seg in sc["segments"]:
        mp3, ws = synth(" ".join(seg["narration"].split()), o, cache)
        dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)]).strip())
        for k, w in enumerate(ws):
            words.append({"w": w["w"], "s": round(t + w["s"], 3), "e": round(t + w["e"], 3), "seg": seg["id"], "i": k})
        segs.append({"id": seg["id"], "s": round(t, 3), "e": round(t + dur, 3)})
        parts.append((mp3, t))
        t += dur + GAP
    total = t - GAP + 0.4
    # resolve beat cues: {cue: "word"} -> time of the first word in that segment starting with it (accent/case-insensitive)
    norm = lambda s: re.sub(r"[^0-9a-zà-ú]", "", s.lower())
    out_beats = []
    for b in beats["beats"]:
        seg = next(s for s in segs if s["id"] == b["seg"])
        def at(cue, default):
            if cue is None:
                return default
            cand = [w for w in words if w["seg"] == b["seg"] and norm(w["w"]).startswith(norm(cue))]
            if not cand:
                raise SystemExit(f"beat cue {cue!r} not found in {b['seg']}")
            return cand[0]["s"]
        els = []
        for el in b["els"]:
            e = dict(el)
            e["at"] = round(at(el.get("cue"), seg["s"]), 3)
            if el.get("until_cue"):
                e["until"] = round(at(el["until_cue"], seg["e"]) - 0.05, 3)
            if el.get("cue_list"):
                e["cues"] = [round(at(c, seg["s"]), 3) for c in el["cue_list"]]
            els.append(e)
        out_beats.append({"seg": b["seg"], "s": seg["s"], "e": seg["e"], "bg": b.get("bg"), "els": els})
    props = {"words": words, "beats": out_beats, "total": round(total, 3), "endCard": END_CARD,
             "disclaimer": beats["disclaimer"], "asof": beats["asof"]}
    (work / "props.json").write_text(json.dumps(props, ensure_ascii=False, indent=1), encoding="utf-8")
    # narration track
    fc = "".join(f"[{i}:a]adelay={int(s * 1000)}|{int(s * 1000)}[a{i}];" for i, (_, s) in enumerate(parts))
    fc += "".join(f"[a{i}]" for i in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{total + END_CARD:.3f},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for mp3, _ in parts:
        cmd += ["-i", str(mp3)]
    run(cmd + ["-filter_complex", fc, "-map", "[out]", "-c:a", "pcm_s16le", str(work / "voice.wav")])
    frames = int(round((total + END_CARD) * 30))
    silent = work / "video_silent.mp4"
    ch = "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell"
    subprocess.run(["npx", "remotion", "render", "src/index.ts", "KineticShort", str(silent), f"--props={work / 'props.json'}",
                    f"--frames=0-{frames - 1}", "--codec=h264", "--crf=18", "--pixel-format=yuv420p", "--concurrency=4",
                    "--log=error", f"--browser-executable={ch}"], check=True, cwd=ROOT / "remotion")
    out = ROOT / "output" / f"{p['slug'].replace('-', '_')}.mp4"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(silent), "-i", str(work / "voice.wav"), "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)])
    print(f"{out.relative_to(ROOT)} {total + END_CARD:.1f}s, {sum(len(' '.join(s['narration'].split())) for s in sc['segments'])} chars")


if __name__ == "__main__":
    main(ROOT / sys.argv[1])
