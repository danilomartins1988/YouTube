"""Build manifest for reproducibility: inputs, tool versions and settings that produced a video."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from hiddeneco import __version__
from hiddeneco.config import REPO_ROOT


def _first_line(cmd: list[str]) -> str | None:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return (out.stdout or out.stderr).strip().splitlines()[0]
    except Exception:
        return None


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def write(out: Path, inputs: list[Path], extra: dict) -> Path:
    git = _first_line(["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"])
    dirty = bool(_first_line(["git", "-C", str(REPO_ROOT), "status", "--porcelain"]))
    data = {
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "hiddeneco_version": __version__,
        "git_commit": git, "git_dirty": dirty,
        "python": sys.version.split()[0], "platform": platform.platform(),
        "tools": {"ffmpeg": _first_line(["ffmpeg", "-version"]),
                  "festival": _first_line(["festival", "--version"]),
                  "espeak-ng": _first_line(["espeak-ng", "--version"])},
        "inputs": {str(p.relative_to(REPO_ROOT)) if p.is_relative_to(REPO_ROOT) else str(p): _sha(p)
                   for p in inputs if p.exists()},
        **extra,
    }
    path = out / "build_manifest.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path
