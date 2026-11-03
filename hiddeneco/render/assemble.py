"""Narration timing, scene rendering and FFmpeg assembly into a 1920x1080 H.264/AAC MP4."""
from __future__ import annotations

import json
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np

from hiddeneco.logging_setup import log
from hiddeneco.models import Dossier, Script, Storyboard, TimedScene
from hiddeneco.render.scenes import SCENES
from hiddeneco.render.style import Style
from hiddeneco.script import render_text
from hiddeneco.tts.base import TTSProvider, wav_seconds


def require_ffmpeg() -> None:
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise RuntimeError(f"{tool} not found. Install FFmpeg (see README).")


def synthesize_narration(script: Script, dossier: Dossier, storyboard: Storyboard, tts: TTSProvider,
                         audio_dir: Path, video_cfg: dict) -> list[TimedScene]:
    """TTS each segment, then lay scenes end to end: lead-in + speech + tail."""
    by_id = {s.id: s for s in script.segments}
    fps = video_cfg["fps"]
    timed, cursor = [], 0.0
    for scene in storyboard.scenes:
        text = render_text(by_id[scene.segment].narration, dossier)
        wav = audio_dir / f"{scene.segment}.wav"
        meta = wav.with_suffix(".json")
        cached = meta.exists() and json.loads(meta.read_text()) == {"text": text, "provider": tts.name,
                                                                    "options": tts.options}
        if cached and wav.exists():
            seconds = wav_seconds(wav)
        else:
            seconds = tts.synthesize(text, wav, video_cfg["audio_sample_rate"])
            meta.write_text(json.dumps({"text": text, "provider": tts.name, "options": tts.options}))
        duration = video_cfg["scene_lead_in"] + seconds + video_cfg["scene_tail"]
        duration = round(duration * fps) / fps          # whole frames keep audio and video locked
        timed.append(TimedScene(scene=scene, narration=text, audio_path=str(wav), audio_seconds=seconds,
                                start=cursor, duration=duration))
        log("tts.segment", segment=scene.segment, seconds=round(seconds, 2), provider=tts.name)
        cursor += duration
    return timed


def build_audio_track(timed: list[TimedScene], out_wav: Path, lead: float, rate: int) -> float:
    total = sum(ts.duration for ts in timed)
    track = np.zeros(int(round(total * rate)) + rate, dtype=np.int32)
    for ts in timed:
        with wave.open(ts.audio_path, "rb") as w:
            if w.getframerate() != rate or w.getnchannels() != 1:
                raise ValueError(f"{ts.audio_path} is not mono {rate} Hz")
            pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.int32)
        start = int(round((ts.start + lead) * rate))
        track[start:start + len(pcm)] += pcm
    track = np.clip(track[: int(round(total * rate))], -32768, 32767).astype(np.int16)
    raw = out_wav.with_name("narration_raw.wav")
    with wave.open(str(raw), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(track.tobytes())
    # broadcast-style loudness normalisation (YouTube plays back around -14 LUFS)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
                    "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(rate), str(out_wav)], check=True)
    return total


def render_scene(ts: TimedScene, style: Style, credits: list[str], out_path: Path, video_cfg: dict,
                 lead: float) -> Path:
    cls = SCENES[ts.scene.type]
    scene = cls(style, ts.scene.params, ts.duration, narration=ts.narration, lead=lead,
                speech=ts.audio_seconds, credits=credits)
    fps = video_cfg["fps"]
    n = int(round(ts.duration * fps))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{style.W}x{style.H}", "-r", str(fps), "-i", "-", "-c:v", "libx264",
           "-preset", video_cfg["preset"], "-crf", str(video_cfg["crf"]), "-pix_fmt", "yuv420p",
           "-r", str(fps), str(out_path)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for i in range(n):
            proc.stdin.write(scene.frame(i / fps, i).tobytes())
    finally:
        proc.stdin.close()
        proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed rendering {ts.scene.id}")
    log("render.scene", scene=ts.scene.id, frames=n, seconds=round(ts.duration, 2))
    return out_path


def concat_and_mux(scene_files: list[Path], audio: Path, out_mp4: Path, work: Path) -> Path:
    lst = work / "scenes.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in scene_files))
    silent = work / "video_only.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(silent)], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(audio),
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", str(out_mp4)], check=True)
    return out_mp4


def srt_time(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(timed: list[TimedScene], lead: float, out: Path, max_chars: int = 84) -> Path:
    """Subtitles: split each segment into sentence-sized cues timed by character share."""
    import re
    cues, n = [], 1
    for ts in timed:
        parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", ts.narration) if p.strip()]
        chunks = []
        for p in parts:
            words, cur = p.split(), ""
            for w in words:
                if len(cur) + len(w) + 1 > max_chars and cur:
                    chunks.append(cur)
                    cur = w
                else:
                    cur = f"{cur} {w}".strip()
            chunks.append(cur)
        total = sum(len(c) for c in chunks) or 1
        t = ts.start + lead
        for c in chunks:
            dur = ts.audio_seconds * len(c) / total
            cues.append(f"{n}\n{srt_time(t)} --> {srt_time(t + dur)}\n{c}\n")
            n += 1
            t += dur
    out.write_text("\n".join(cues), encoding="utf-8")
    return out


def probe(path: Path) -> dict:
    res = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,width,height,r_frame_rate:format=duration", "-of", "json",
                          str(path)], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)
