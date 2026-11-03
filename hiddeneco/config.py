"""Settings loading. Secrets come only from environment variables (optionally a local .env)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_dotenv(path: Path | None = None) -> None:
    """Minimal .env loader (KEY=VALUE lines). Never overrides variables already set."""
    path = path or REPO_ROOT / ".env"
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return value if value not in (None, "") else default


@lru_cache(maxsize=1)
def settings() -> dict[str, Any]:
    load_dotenv()
    with open(REPO_ROOT / "config" / "settings.yaml", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def offline() -> bool:
    return env("HIDDENECO_OFFLINE", "0") == "1"


@dataclass(frozen=True)
class ProjectPaths:
    """Paths for one topic (slug) and, optionally, one deliverable of it.

    projects/<slug>/                      topic-level: project.yaml, sources.yaml
    projects/<slug>/deliverables/<id>/    deliverable.yaml, script.yaml, storyboard.yaml
    output/<slug>/research/               shared dossier
    output/<slug>/<id>/                   everything rendered for that deliverable
    """
    slug: str
    root: Path
    deliverable: str | None = None

    @property
    def project_dir(self) -> Path:
        return self.root / "projects" / self.slug

    @property
    def deliverable_dir(self) -> Path:
        if self.deliverable is None:
            return self.project_dir
        return self.project_dir / "deliverables" / self.deliverable

    @property
    def topic_out(self) -> Path:
        return self.root / "output" / self.slug

    @property
    def research_out(self) -> Path:
        p = self.topic_out / "research"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def out(self) -> Path:
        return self.topic_out if self.deliverable is None else self.topic_out / self.deliverable

    def out_sub(self, name: str) -> Path:
        p = self.out / name
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def final_video(self) -> Path:
        suffix = f"--{self.deliverable}" if self.deliverable else ""
        return self.out / f"{self.slug}{suffix}.mp4"

    def for_deliverable(self, deliverable: str) -> "ProjectPaths":
        return ProjectPaths(self.slug, self.root, deliverable)

    def deliverables(self) -> list[str]:
        d = self.project_dir / "deliverables"
        return sorted(p.name for p in d.iterdir() if (p / "deliverable.yaml").exists()) if d.exists() else []


def project_paths(slug: str, root: Path | None = None, deliverable: str | None = None) -> ProjectPaths:
    return ProjectPaths(slug=slug, root=root or REPO_ROOT, deliverable=deliverable)
