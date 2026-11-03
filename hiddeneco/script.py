"""Script loading, placeholder rendering and sourcing checks."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from hiddeneco.models import Dossier, Script

PLACEHOLDER = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)(?:\.([a-zA-Z0-9_]+))?\s*(\|cap)?\s*\}\}")
NUMBER_WORDS = re.compile(
    r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|"
    r"hundred|thousand|million|billion|trillion|percent|half|third|thirds|quarter|twice|double|"
    r"triple|dozen)\b", re.IGNORECASE)
DIGITS = re.compile(r"\d")
WORDS = re.compile(r"[A-Za-z']+")


class ScriptError(ValueError):
    pass


def load_script(deliverable_dir: Path) -> Script:
    return Script(**yaml.safe_load((deliverable_dir / "script.yaml").read_text(encoding="utf-8")))


def resolve(dossier: Dossier, claim_id: str, field: str | None):
    claim = dossier.claim(claim_id)
    if field is None:
        if claim.spoken is None:
            raise ScriptError(f"Claim '{claim_id}' has no spoken form")
        return claim.spoken
    if field in ("display", "spoken", "value", "text"):
        return getattr(claim, field)
    if field in claim.fields:
        return claim.fields[field]
    raise ScriptError(f"Claim '{claim_id}' has no field '{field}'")


def _sub(m, dossier: Dossier) -> str:
    text = str(resolve(dossier, m.group(1), m.group(2)))
    return text[:1].upper() + text[1:] if m.group(3) else text


def render_text(template: str, dossier: Dossier) -> str:
    """Fill {{claim}}, {{claim.field}} and {{claim|cap}} (capitalise first letter)."""
    return PLACEHOLDER.sub(lambda m: _sub(m, dossier), template)


def render_value(obj, dossier: Dossier):
    """Recursively render placeholders inside storyboard params."""
    if isinstance(obj, str):
        m = PLACEHOLDER.fullmatch(obj.strip())
        if m and m.group(2) == "value":
            return resolve(dossier, m.group(1), "value")
        return render_text(obj, dossier)
    if isinstance(obj, list):
        return [render_value(x, dossier) for x in obj]
    if isinstance(obj, dict):
        return {k: render_value(v, dossier) for k, v in obj.items()}
    return obj


def placeholder_ids(template: str) -> set[str]:
    return {m.group(1) for m in PLACEHOLDER.finditer(template)}


def sourcing_issues(script: Script, dossier: Dossier) -> list[dict]:
    """Find numbers typed by hand and placeholders not declared in the segment's claims list."""
    known = {c.id for c in dossier.claims}
    issues = []
    for seg in script.segments:
        bare = PLACEHOLDER.sub(" ", seg.narration)
        if DIGITS.search(bare):
            issues.append({"severity": "error", "segment": seg.id,
                           "message": f"Hand-typed digits in narration: '{bare.strip()}'. "
                                      "Use a dossier placeholder."})
        for word in sorted({w.lower() for w in NUMBER_WORDS.findall(bare)}):
            issues.append({"severity": "warning", "segment": seg.id,
                           "message": f"Number word '{word}' outside a placeholder - confirm it is "
                                      "not an unsourced statistic."})
        for cid in placeholder_ids(seg.narration):
            if cid not in known:
                issues.append({"severity": "error", "segment": seg.id, "message": f"Unknown claim '{cid}'"})
            elif cid not in seg.claims:
                issues.append({"severity": "error", "segment": seg.id,
                               "message": f"Placeholder '{cid}' not listed in segment claims"})
        for cid in seg.claims:
            if cid not in known:
                issues.append({"severity": "error", "segment": seg.id, "message": f"Unknown claim '{cid}'"})
    return issues


def word_count(text: str) -> int:
    return len(WORDS.findall(text))


def estimate_seconds(text: str, wpm: float) -> float:
    return word_count(text) / wpm * 60


def to_markdown(script: Script, dossier: Dossier) -> str:
    lines = [f"# {script.title}", "", f"_{script.logline}_", ""]
    for seg in script.segments:
        text = render_text(seg.narration, dossier)
        lines.append(f"## {seg.id}" + (f" - {seg.chapter}" if seg.chapter else ""))
        lines.append("")
        lines.append(text)
        lines.append("")
        notes = []
        for cid in seg.claims:
            c = dossier.claim(cid)
            notes.append(f"`{cid}` [{c.status}] {c.text} (sources: {', '.join(c.source_ids)})")
        if seg.analysis:
            notes.append("Contains editorial interpretation (marked analysis).")
        if seg.source_note:
            notes.append(seg.source_note)
        lines += [f"> {n}  " for n in notes] + [""]
    return "\n".join(lines)
