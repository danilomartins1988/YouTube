"""Narration timing, scene rendering and FFmpeg assembly into H.264/AAC MP4 (16:9 or 9:16)."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np

from hiddeneco import audio as audio_mod
from hiddeneco import timing
from hiddeneco.logging_setup import log
from hiddeneco.models import Deliverable, Dossier, Script, Storyboard, TimedScene
from hiddeneco.render.scenes import SCENES
from hiddeneco.render.style import Style
from hiddeneco.script import render_text
from hiddeneco.speech_text import spoken
from hiddeneco.tts.base import TTSProvider


def require_ffmpeg() -> None:
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise RuntimeError(f"{tool} not found. Install FFmpeg (see README).")


def _sentence_audio(tts: TTSProvider, text: str, cache_dir: Path, rate: int) -> tuple[np.ndarray, bool]:
    """Synthesise one sentence, cached by (provider, options, text). Returns (samples, fresh)."""
    say = spoken(text)   # numbers/years/currency written out the way a narrator says them
    key = hashlib.sha256(json.dumps([tts.name, tts.options, say], sort_keys=True).encode()).hexdigest()[:20]
    wav = cache_dir / f"{key}.wav"
    fresh = not wav.exists()
    if fresh:
        tts.synthesize(say, wav, rate)
    samples, r = audio_mod.read_wav(wav)
    if r != rate:
        raise ValueError(f"{wav} has rate {r}, expected {rate}")
    return samples, fresh


def synthesize_narration(script: Script, dossier: Dossier, storyboard: Storyboard, tts: TTSProvider,
                         audio_dir: Path, fmt: dict, rate: int, fps: int,
                         sentence_gap: float) -> tuple[list[TimedScene], int]:
    """TTS each sentence; lay scenes end to end (lead-in + speech + tail, whole frames).
    Returns the timeline and the number of characters actually sent to the provider."""
    by_id = {s.id: s for s in script.segments}
    cache = audio_dir / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    lead, tail = fmt["scene_lead_in"], fmt["scene_tail"]
    gap = np.zeros(int(sentence_gap * rate), dtype=np.float32)
    timed, cursor, fresh_chars = [], 0.0, 0
    for scene in storyboard.scenes:
        text = render_text(by_id[scene.segment].narration, dossier)
        parts, words, t = [], [], lead
        for i, sent in enumerate(timing.sentences(text)):
            if i:
                parts.append(gap)
                t += len(gap) / rate
            samples, fresh = _sentence_audio(tts, sent, cache, rate)
            fresh_chars += len(sent) if fresh else 0
            dur = len(samples) / rate
            words += timing.word_timings(sent, t, dur)
            parts.append(samples)
            t += dur
        voice = np.concatenate(parts) if parts else np.zeros(1, np.float32)
        wav = audio_mod.write_wav(audio_dir / f"{scene.segment}.wav", voice, rate)
        seconds = len(voice) / rate if parts else 0.0      # silent scenes (e.g. act cards) allowed
        duration = max(lead + seconds + tail, float(scene.params.get("min_seconds", 0)))
        duration = round(duration * fps) / fps   # whole frames keep A/V locked
        timed.append(TimedScene(scene=scene, narration=text, audio_path=str(wav), audio_seconds=seconds,
                                start=cursor, duration=duration, words=words))
        log("tts.segment", segment=scene.segment, seconds=round(seconds, 2), provider=tts.name)
        cursor += duration
    return timed, fresh_chars


def sfx_events(timed: list[TimedScene], enabled: bool) -> list[tuple[float, str, float]]:
    """Automatic transition whooshes plus cue-anchored effects declared in the storyboard."""
    if not enabled:
        return []
    events = []
    for i, ts in enumerate(timed):
        if i == 0:
            events.append((ts.start + 0.05, "hit", 0.32))
        else:
            events.append((ts.start - 0.2, "whoosh", 0.22))
        for fx in ts.scene.sfx:
            at = timing.cue_time(ts.words, fx["cue"]) if "cue" in fx else fx.get("at", 0.0)
            if at is None:
                log("audio.cue_missing", scene=ts.scene.id, cue=fx.get("cue"))
                continue
            events.append((ts.start + at + fx.get("offset", 0.0), fx["kind"], fx.get("gain", 0.25)))
    return events


def build_audio_track(timed: list[TimedScene], out_dir: Path, deliverable: Deliverable, fmt: dict,
                      rate: int) -> tuple[Path, Path]:
    """Returns (final loudness-normalised mix, voice-only track used for QC)."""
    total = sum(ts.duration for ts in timed)
    voice = np.zeros(int(round(total * rate)), dtype=np.float32)
    for ts in timed:
        samples, _ = audio_mod.read_wav(Path(ts.audio_path))
        s = int(round(ts.start * rate)) + int(round(fmt["scene_lead_in"] * rate))
        e = min(len(voice), s + len(samples))
        voice[s:e] += samples[: e - s]
    peak = np.max(np.abs(voice)) or 1.0
    voice *= 0.8 / peak
    voice_path = audio_mod.write_wav(out_dir / "voice_only.wav", voice, rate)
    events = sfx_events(timed, deliverable.audio.get("sfx", True))
    mixed = audio_mod.mix(voice, events, deliverable.audio.get("music", True), rate)
    raw = audio_mod.write_wav(out_dir / "mix_raw.wav", mixed, rate)
    final = audio_mod.loudnorm(raw, out_dir / "mix.wav", fmt["loudness_lufs"], rate)
    log("audio.mixed", seconds=round(total, 2), sfx=len(events), music=deliverable.audio.get("music", True))
    return final, voice_path


def render_scene(ts: TimedScene, style: Style, credits: list[str], out_path: Path, vcfg: dict,
                 fmt: dict, captions: bool) -> Path:
    cls = SCENES[ts.scene.type]
    scene = cls(style, ts.scene.params, ts.duration, narration=ts.narration, lead=fmt["scene_lead_in"],
                speech=ts.audio_seconds, credits=credits, words=ts.words,
                captions=timing.caption_chunks(ts.words) if captions else None,
                fade=fmt.get("fade", 0.35), safe=fmt.get("safe_zone"))
    fps = vcfg["fps"]
    n = int(round(ts.duration * fps))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{style.W}x{style.H}", "-r", str(fps), "-i", "-", "-c:v", "libx264",
           "-preset", vcfg["preset"], "-crf", str(vcfg["crf"]), "-pix_fmt", "yuv420p",
           "-threads", str(vcfg.get("encoder_threads", 0)),
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


def _render_job(args):
    ts_json, style_cfg, size, credits, out_path, vcfg, fmt, captions = args
    ts = TimedScene.model_validate_json(ts_json)
    style = Style(style_cfg, size[0], size[1], vcfg["fps"])
    return str(render_scene(ts, style, credits, Path(out_path), vcfg, fmt, captions))


def render_scenes_parallel(jobs: list[tuple], workers: int) -> None:
    """Render scenes in separate processes (each also runs its own x264 encoder)."""
    if workers <= 1 or len(jobs) <= 1:
        for j in jobs:
            _render_job(j)
        return
    import multiprocessing as mp
    with mp.get_context("spawn").Pool(workers) as pool:
        for _ in pool.imap_unordered(_render_job, jobs):
            pass


def concat_and_mux(scene_files: list[Path], audio: Path, out_mp4: Path, work: Path) -> Path:
    lst = work / "scenes.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in scene_files))
    silent = work / "video_only.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(silent)], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent), "-i", str(audio),
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", str(out_mp4)], check=True)
    return out_mp4


def srt_time(sec: float) -> str:
    ms = int(round(max(0.0, sec) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def caption_cues(timed: list[TimedScene], max_words: int = 7, max_chars: int = 42) -> list[dict]:
    """Absolute-time caption cues (sidecar subtitles) built from word timings."""
    cues = []
    for ts in timed:
        for c in timing.caption_chunks(ts.words, max_words=max_words, max_chars=max_chars):
            cues.append({"text": c["text"], "start": ts.start + c["start"], "end": ts.start + c["end"]})
    for a, b in zip(cues, cues[1:]):          # hold each cue until the next one (max 0.6 s extra)
        a["end"] = min(b["start"], a["end"] + 0.6)
    return cues


def write_srt(timed: list[TimedScene], out: Path) -> Path:
    cues = caption_cues(timed)
    out.write_text("\n".join(f"{i}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n{c['text']}\n"
                             for i, c in enumerate(cues, 1)), encoding="utf-8")
    return out


def probe(path: Path) -> dict:
    res = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels"
                          ":format=duration,bit_rate,size", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True)
    return json.loads(res.stdout)
