"""Concrete TTS providers: espeak-ng and Piper (free, local), ElevenLabs and OpenAI (paid, opt-in),
and a silent provider for tests."""
from __future__ import annotations

import math
import shutil
import struct
import subprocess
import sys
import wave
from pathlib import Path

import requests

from hiddeneco.config import env
from hiddeneco.tts.base import TTSProvider


class EspeakProvider(TTSProvider):
    """espeak-ng: always-available offline fallback. Robotic, but free and deterministic."""
    name = "espeak"

    def available(self):
        return (True, "") if shutil.which("espeak-ng") else (False, "espeak-ng not installed")

    def _synthesize(self, text, out_path):
        o = self.options
        subprocess.run(["espeak-ng", "-v", o.get("voice", "en-gb-x-rp"),
                        "-s", str(o.get("words_per_minute", 160)), "-p", str(o.get("pitch", 45)),
                        "-w", str(out_path), text], check=True)
        return out_path


class FestivalProvider(TTSProvider):
    """Festival with the CMU ARCTIC 'slt' HTS voice: free, offline, clearer than espeak.
    Install: apt install festival festvox-us-slt-hts (Debian/Ubuntu)."""
    name = "festival"

    def available(self):
        if not shutil.which("text2wave"):
            return False, "festival not installed (apt install festival festvox-us-slt-hts)"
        return True, ""

    def _synthesize(self, text, out_path):
        txt = out_path.with_suffix(".txt")
        txt.write_text(text, encoding="utf-8")
        voice = self.options.get("voice", "cmu_us_slt_arctic_hts")
        subprocess.run(["text2wave", "-eval", f"(voice_{voice})", str(txt), "-o", str(out_path)],
                       check=True, capture_output=True)
        txt.unlink(missing_ok=True)
        return out_path


def kokoro_voice(k, spec: str):
    """'am_fenrir' or a weighted blend like 'am_fenrir:0.5+am_michael:0.5' (weights normalised)."""
    if "+" not in spec and ":" not in spec:
        return spec
    import numpy as np
    parts = [(p.split(":")[0].strip(), float(p.split(":")[1]) if ":" in p else 1.0) for p in spec.split("+")]
    total = sum(w for _, w in parts)
    return (sum(w / total * k.get_voice_style(name) for name, w in parts)).astype(np.float32)


class KokoroProvider(TTSProvider):
    """Kokoro-82M via kokoro-onnx: free, local, natural-sounding (Apache-2.0 weights).
    pip install kokoro-onnx; download kokoro-v1.0.onnx + voices-v1.0.bin and set the env vars."""
    name = "kokoro"

    def _paths(self):
        m = env(self.options.get("model_path_env", "KOKORO_MODEL_PATH"))
        v = env(self.options.get("voices_path_env", "KOKORO_VOICES_PATH"))
        return (Path(m) if m else None), (Path(v) if v else None)

    def available(self):
        try:
            import kokoro_onnx  # noqa: F401
        except ImportError:
            return False, "pip install kokoro-onnx"
        m, v = self._paths()
        if not (m and m.exists() and v and v.exists()):
            return False, "set KOKORO_MODEL_PATH and KOKORO_VOICES_PATH to the downloaded model files"
        return True, ""

    def _synthesize(self, text, out_path):
        import numpy as np
        from kokoro_onnx import Kokoro
        m, v = self._paths()
        k = Kokoro(str(m), str(v))
        samples, rate = k.create(
            text, voice=kokoro_voice(k, self.options.get("voice", "am_michael")),
            speed=float(self.options.get("speed", 1.0)), lang=self.options.get("lang", "en-us"))
        pcm = (np.clip(samples, -1, 1) * 32767).astype("<i2")
        with wave.open(str(out_path), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(rate)
            w.writeframes(pcm.tobytes())
        return out_path


class PiperProvider(TTSProvider):
    """Piper: free local neural TTS (https://github.com/rhasspy/piper). Needs a downloaded voice;
    check each voice's MODEL_CARD for its licence before commercial use."""
    name = "piper"

    def _voice(self) -> Path | None:
        p = env(self.options.get("voice_path_env", "PIPER_VOICE_PATH"))
        return Path(p) if p else None

    def available(self):
        try:
            import piper  # noqa: F401
        except ImportError:
            return False, "pip install piper-tts"
        v = self._voice()
        if not v or not v.exists() or not Path(str(v) + ".json").exists():
            return False, "set PIPER_VOICE_PATH to a voice .onnx (with .onnx.json beside it)"
        return True, ""

    def _synthesize(self, text, out_path):
        cmd = [sys.executable, "-m", "piper", "-m", str(self._voice()), "-f", str(out_path),
               "--length-scale", str(self.options.get("length_scale", 1.0))]
        subprocess.run(cmd, input=text.encode("utf-8"), check=True)
        return out_path


class ElevenLabsProvider(TTSProvider):
    name = "elevenlabs"
    paid = True
    raw_suffix = ".mp3"

    def available(self):
        if not env(self.options.get("api_key_env", "ELEVENLABS_API_KEY")):
            return False, "ELEVENLABS_API_KEY not set"
        if not self.options.get("voice_id"):
            return False, "tts.providers.elevenlabs.voice_id not set in config/settings.yaml"
        return True, ""

    def _synthesize(self, text, out_path):
        o = self.options
        resp = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{o['voice_id']}",
            headers={"xi-api-key": env(o.get("api_key_env", "ELEVENLABS_API_KEY")),
                     "Content-Type": "application/json"},
            json={"text": text, "model_id": o.get("model_id", "eleven_multilingual_v2")}, timeout=120)
        resp.raise_for_status()
        out_path.write_bytes(resp.content)
        return out_path


class OpenAIProvider(TTSProvider):
    name = "openai"
    paid = True

    def available(self):
        if not env(self.options.get("api_key_env", "OPENAI_API_KEY")):
            return False, "OPENAI_API_KEY not set"
        return True, ""

    def _synthesize(self, text, out_path):
        o = self.options
        resp = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={"Authorization": f"Bearer {env(o.get('api_key_env', 'OPENAI_API_KEY'))}"},
            json={"model": o.get("model", "tts-1-hd"), "voice": o.get("voice", "onyx"), "input": text,
                  "response_format": "wav",
                  # style direction is only supported by the gpt-4o family of TTS models
                  **({"instructions": o["instructions"]} if o.get("instructions")
                     and str(o.get("model", "")).startswith("gpt-4o") else {})},
            timeout=120)
        resp.raise_for_status()
        out_path.write_bytes(resp.content)
        return out_path


class SilentProvider(TTSProvider):
    """Writes a quiet tone of the estimated narration length. For tests and layout previews."""
    name = "silent"

    def available(self):
        return True, ""

    def _synthesize(self, text, out_path):
        from hiddeneco.script import estimate_seconds
        seconds = max(0.5, estimate_seconds(text, self.options.get("words_per_minute", 150)))
        rate = 22050
        with wave.open(str(out_path), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(rate)
            frames = bytearray()
            for i in range(int(seconds * rate)):
                frames += struct.pack("<h", int(800 * math.sin(2 * math.pi * 220 * i / rate)))
            w.writeframes(bytes(frames))
        return out_path


PROVIDERS = {p.name: p for p in (FestivalProvider, KokoroProvider, EspeakProvider, PiperProvider, ElevenLabsProvider,
                                 OpenAIProvider, SilentProvider)}


def get_provider(name: str, settings: dict, allow_paid: bool = False) -> TTSProvider:
    if name not in PROVIDERS:
        raise KeyError(f"Unknown TTS provider '{name}'. Choose from {sorted(PROVIDERS)}")
    cls = PROVIDERS[name]
    if cls.paid and not allow_paid:
        raise PermissionError(f"'{name}' is a paid service. Re-run with --allow-paid after reviewing "
                              "the cost estimate (python -m hiddeneco estimate <slug> --tts "
                              f"{name}).")
    return cls(settings["tts"]["providers"].get(name, {}))


def default_provider_name(settings: dict) -> str:
    """First *available* provider from tts.default_provider (a name or a list of names)."""
    choice = settings["tts"]["default_provider"]
    names = [choice] if isinstance(choice, str) else list(choice)
    for name in names:
        cls = PROVIDERS[name]
        if not cls.paid and cls(settings["tts"]["providers"].get(name, {})).available()[0]:
            return name
    raise RuntimeError(f"None of the default TTS providers is available: {names}. Run `python -m hiddeneco tts-check`.")
