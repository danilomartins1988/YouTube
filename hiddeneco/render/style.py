"""Per-project visual identity: palette, fonts, background texture."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageFont

from hiddeneco.config import REPO_ROOT

FONT_DIRS = [REPO_ROOT / "assets" / "fonts", Path("/usr/share/fonts/opentype/inter"),
             Path("/usr/share/fonts/truetype/inter"), Path("/usr/share/fonts"),
             Path("~/.local/share/fonts").expanduser(), Path("~/.fonts").expanduser(),
             Path("~/Library/Fonts").expanduser(), Path("/Library/Fonts"),
             Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"]
FALLBACKS = ["DejaVuSans-Bold", "DejaVuSans", "LiberationSans-Bold", "Arial"]


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


@lru_cache(maxsize=64)
def find_font(name: str) -> str | None:
    for d in FONT_DIRS:
        if not d.exists():
            continue
        for ext in (".otf", ".ttf"):
            direct = d / f"{name}{ext}"
            if direct.exists():
                return str(direct)
        for ext in (".otf", ".ttf"):
            hits = list(d.rglob(f"{name}{ext}"))
            if hits:
                return str(hits[0])
    return None


@lru_cache(maxsize=256)
def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for candidate in [name] + FALLBACKS:
        path = find_font(candidate)
        if path:
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


class Style:
    def __init__(self, style_cfg: dict, width: int = 1920, height: int = 1080, fps: int = 30):
        self.name = style_cfg.get("name", "default")
        self.palette = {k: hex_rgb(v) for k, v in style_cfg["palette"].items()}
        self.fonts = style_cfg["fonts"]
        self.motifs = set(style_cfg.get("motifs", []))
        self.W, self.H, self.fps = width, height, fps
        self._bg = None
        self._grain = None

    def c(self, name: str) -> tuple[int, int, int]:
        return self.palette.get(name) or hex_rgb(name)

    def f(self, role: str, size: int) -> ImageFont.FreeTypeFont:
        return font(self.fonts.get(role, role), int(size))

    def background(self) -> Image.Image:
        if self._bg is None:
            W, H = self.W, self.H
            y, x = np.mgrid[0:H, 0:W].astype(np.float32)
            t = (0.65 * y / H + 0.35 * x / W)[..., None]
            a, b = np.array(self.c("bg"), np.float32), np.array(self.c("bg2"), np.float32)
            img = a * (1 - t) + b * t
            d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)[..., None]
            img *= 1 - 0.28 * np.clip(d - 0.35, 0, 1)
            if "ledger-rules" in self.motifs:
                for yy in range(90, H, 54):
                    img[yy:yy + 1, :, :] = img[yy:yy + 1, :, :] * 0.93 + 255 * 0.012
            self._bg = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")
        return self._bg.copy()

    def grain(self, frame: Image.Image, index: int) -> Image.Image:
        if "film-grain" not in self.motifs:
            return frame
        if self._grain is None:
            rng = np.random.default_rng(7)
            self._grain = [rng.normal(0, 2.2, (self.H, self.W, 1)).astype(np.int16) for _ in range(6)]
        # grain refreshes every 3rd frame (~10 fps, like projected film) - far cheaper to encode
        arr = np.asarray(frame, dtype=np.int16) + self._grain[(index // 3) % len(self._grain)]
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
