"""Write the machine-readable scene manifest for a built deliverable (mandatory from Episode 06).

For every scene: narration segment, start/end time, visual objective, animation type, the keyframes
(every narration cue the animation is tied to, resolved to an absolute time from the word timings),
assets, sources and the transition into the next scene.

    python tools/scene_manifest.py <slug> <out.json> [deliverable]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import yaml  # noqa: E402
from hiddeneco.config import project_paths  # noqa: E402

sys.path.insert(0, str(ROOT / "tools"))
from export_episode_docs import DESCRIBE  # noqa: E402

norm = lambda w: re.sub(r"[^\w%]", "", w.lower())  # noqa: E731  (same rule as remotion/src/lib/anim.ts)


def cue_time(words: list[dict], phrase: str) -> float | None:
    target = [norm(x) for x in str(phrase).split() if norm(x)]
    seq = [norm(w["word"]) for w in words]
    for i in range(len(seq) - len(target) + 1):
        if seq[i:i + len(target)] == target:
            return words[i]["start"]
    return None


def walk(obj, path=""):
    """Yield (path, spec) for every dict in the params that carries a narration cue."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "cue" or k.endswith("_cue"):
                yield f"{path}.{k}".lstrip("."), obj, v
            yield from walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")


def main() -> None:
    slug, out = sys.argv[1], Path(sys.argv[2])
    did = sys.argv[3] if len(sys.argv) > 3 else "documentary"
    paths = project_paths(slug, deliverable=did)
    timeline = json.loads((paths.out / "timeline.json").read_text())
    scenes = timeline["scenes"] if isinstance(timeline, dict) else timeline
    project = yaml.safe_load((paths.project_dir / "project.yaml").read_text())
    transition = project.get("style", {}).get("transition", "fade")
    rows = []
    for i, ts in enumerate(scenes):
        sc = ts["scene"]
        words = ts.get("words", [])
        keyframes = []
        for where, spec, phrase in walk(sc.get("params", {})):
            at = cue_time(words, phrase) if isinstance(phrase, str) else None
            label = spec.get("label") or spec.get("text") or spec.get("kicker") or spec.get("id") or where
            keyframes.append({"param": where, "cue": phrase, "label": str(label)[:80],
                              "scene_time_s": round(at + float(spec.get("offset", 0) or 0), 2) if at is not None else None,
                              "absolute_s": round(ts["start"] + at + float(spec.get("offset", 0) or 0), 2) if at is not None else None})
        keyframes.sort(key=lambda k: (k["absolute_s"] is None, k["absolute_s"] or 0))
        unresolved = [k["cue"] for k in keyframes if k["absolute_s"] is None]
        rows.append({
            "index": i + 1, "id": sc["id"], "segment": sc["segment"], "type": sc["type"],
            "start_s": round(ts["start"], 2), "end_s": round(ts["start"] + ts["duration"], 2), "duration_s": round(ts["duration"], 2),
            "visual_objective": sc.get("note") or DESCRIBE.get(sc["type"], ""),
            "narration": ts.get("narration", ""),
            "keyframes": keyframes, "unresolved_cues": unresolved,
            "assets": sc.get("assets", []), "sources": sc.get("sources", []),
            "transition_out": "end" if i == len(scenes) - 1 else transition,
        })
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"slug": slug, "deliverable": did, "scenes": rows}, indent=2, ensure_ascii=False), encoding="utf-8")
    n_unres = sum(len(r["unresolved_cues"]) for r in rows)
    print(f"wrote {out}: {len(rows)} scenes, {sum(len(r['keyframes']) for r in rows)} keyframes, {n_unres} unresolved cues")


if __name__ == "__main__":
    main()
