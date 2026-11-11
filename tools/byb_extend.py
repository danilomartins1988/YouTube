"""Insert extra segments (script.yaml), claims (sources.yaml) and scenes (generator) into a Before You Buy episode.

Text insertion keeps the files' comments and formatting. Used 2026-11-11 to lengthen the six Nov 2026 editions for
the faster series voice (alloy). Spec: a Python file defining SLUG, GEN, CLAIMS (YAML text appended to sources.yaml)
and SEGS = [{after, id, chapter, narration, claims, scene}] where `scene` is generator code inserted after the
generator block of the segment named in `after`.
Run: python tools/byb_extend.py spec.py   (idempotent: segments whose id already exists are skipped)
"""
from __future__ import annotations

import re
import runpy
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def wrap(s: str, indent: str) -> str:
    return textwrap.fill(" ".join(s.split()), width=120, initial_indent="", subsequent_indent=indent)


def main(spec_path: str) -> None:
    spec = runpy.run_path(spec_path)
    slug, gen = spec["SLUG"], ROOT / spec["GEN"]
    sp = ROOT / "projects" / slug / "deliverables/documentary/script.yaml"
    srcp = ROOT / "projects" / slug / "sources.yaml"
    script, src, code = sp.read_text(), srcp.read_text(), gen.read_text()
    for seg in spec["SEGS"]:
        if f"- id: {seg['id']}\n" in script:
            continue
        # script: insert before the segment that follows `after`
        m = re.search(rf"^- id: {re.escape(seg['after'])}\n", script, re.M)
        assert m, seg["after"]
        nxt = re.search(r"^- id: ", script[m.end():], re.M)
        pos = m.end() + nxt.start() if nxt else len(script)
        block = (f"- id: {seg['id']}\n  chapter: {seg['chapter']}\n  narration: {wrap(seg['narration'], '    ')}\n"
                 f"  claims:\n" + "".join(f"  - {c}\n" for c in seg["claims"]))
        if seg.get("analysis"):
            block += f"  analysis: true\n  source_note: {seg.get('source_note', 'Our calculation from sourced figures.')}\n"
        script = script[:pos] + block + script[pos:]
        # generator: insert after the block of the scene bound to `after`
        gm = re.search(rf'^\w+\("[^"]+", "{re.escape(seg["after"])}"', code, re.M)
        assert gm, f"generator scene for {seg['after']}"
        gn = re.search(r'^(stage|board|card|kinetic|add|disclaimer|# =)', code[gm.end():], re.M)
        gpos = gm.end() + gn.start() if gn else len(code)
        code = code[:gpos] + textwrap.dedent(seg["scene"]).strip() + "\n" + code[gpos:]
    if spec.get("CLAIMS") and spec["CLAIMS"].strip().split("\n")[0].strip() not in src:
        src = src.rstrip("\n") + "\n\n" + spec["CLAIMS"].strip("\n") + "\n"   # CLAIMS already indented like the file
    sp.write_text(script), srcp.write_text(src), gen.write_text(code)
    print("ok", slug)


if __name__ == "__main__":
    main(sys.argv[1])
