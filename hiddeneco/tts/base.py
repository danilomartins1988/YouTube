"""Text-to-speech adapter interface.

Every provider writes a WAV file; the pipeline then normalises it to 48 kHz mono so the
assembler never cares which engine produced it. Paid providers refuse to run unless the caller
passes allow_paid=True (CLI: --allow-paid), so nothing is billed by accident.
"""
from __future__ import annotations

import abc
import shutil
import subprocess
import wave
from pathlib import Path

from hiddeneco.costs import tts_cost
from hiddeneco.models import CostLine


class TTSUnavailable(RuntimeError):
    pass


class TTSProvider(abc.ABC):
    name: str = "base"
    paid: bool = False

    def __init__(self, options: dict | None = None):
        self.options = options or {}

    @abc.abstractmethod
    def available(self) -> tuple[bool, str]:
        """Return (ok, reason)."""

    @abc.abstractmethod
    def _synthesize(self, text: str, out_path: Path) -> Path:
        """Write raw audio for text; return the written path (any format ffmpeg can read)."""

    def synthesize(self, text: str, out_wav: Path, sample_rate: int = 48000) -> float:
        ok, reason = self.available()
        if not ok:
            raise TTSUnavailable(f"{self.name}: {reason}")
        out_wav.parent.mkdir(parents=True, exist_ok=True)
        from hiddeneco.retry import retry
        raw_path = out_wav.with_suffix(".raw" + self.raw_suffix)
        # network providers can fail transiently; local ones simply succeed first time
        raw = retry(lambda: self._synthesize(text, raw_path), attempts=4 if self.paid else 1,
                    what=f"tts:{self.name}")
        normalise_wav(raw, out_wav, sample_rate, tempo=float(self.options.get("tempo", 1.0)),
                      polish=self.options.get("voice_polish"))
        if raw != out_wav:
            raw.unlink(missing_ok=True)
        return wav_seconds(out_wav)

    raw_suffix = ".wav"

    def estimate_cost(self, chars: int) -> CostLine:
        return tts_cost(self.name, chars)


def normalise_wav(src: Path, dst: Path, sample_rate: int = 48000, tempo: float = 1.0,
                  polish: str | None = None) -> None:
    """Resample to mono 16-bit PCM, trim leading/trailing silence, optionally change tempo
    without changing pitch."""
    if not shutil.which("ffmpeg"):
        raise TTSUnavailable("ffmpeg not found on PATH")
    trim = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,"
            "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.08,areverse")
    if abs(tempo - 1.0) > 1e-3:
        trim += f",atempo={tempo:.3f}"
    # voice polish (configurable in settings: tts.voice_polish): EQ, gentle compression, soft room
    # A provider can override it (tts.providers.<name>.voice_polish); "none" disables it.
    if polish is None:
        from hiddeneco.config import settings
        polish = settings()["tts"].get("voice_polish",
                                       "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2")
    if polish and polish.strip().lower() != "none":
        trim += "," + polish
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-af", trim,
                    "-ac", "1", "-ar", str(sample_rate), "-sample_fmt", "s16", str(dst)], check=True)


def wav_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()
