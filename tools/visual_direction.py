"""Visual direction plan for an episode (adaptive visual storytelling, standard of 2026-11-08).

  python tools/visual_direction.py plan <slug> [--deliverable documentary] [--doc docs/episodes/NN-name] [--force]
      Reads the script, scores each chapter against the tone lexicon, and writes
        projects/<slug>/visual_direction.yaml   (APPLIED by the pipeline: palette, tones, tone shifts, presenter)
        <doc>/VISUAL_DIRECTION.md               (the 12-point plan for humans)
      An existing visual_direction.yaml is kept (it is meant to be edited by hand) unless --force.
  python tools/visual_direction.py doc <slug> [--doc ...]
      Re-writes only VISUAL_DIRECTION.md from the current visual_direction.yaml.

The classification is a starting point: a director should read it, adjust tones per chapter and turning points, and
commit the YAML. Tones: bright, thriller, crisis, strategy, trade, tech, history, reflective.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

LEXICON = {
    "thriller": "fraud never existed missing scandal auditor audit prosecutor prosecutors deceive false fake trustee whistleblower manipulation "
                "secret secretly accused charges suspicion suspicions investigation police wanted vanished hidden lie lies forged short sellers",
    "crisis": "collapse collapsed collapses bankrupt bankruptcy insolvency crash crashed panic run contagion crisis default bailout plunge plunged "
              "fell losses lost failure failed squeeze emergency fear chaos tears halved",
    "strategy": "rival rivals competitor competition acquisition merger merge stake takeover monopoly strategy deal market share ambition bet "
                "control customers suppliers investors brand profit",
    "trade": "ship ships shipping port ports container containers cargo flag flags route routes supply chain logistics canal tanker sea ocean "
             "crew registry owners trade exports imports",
    "tech": "chip chips machine machines laser lasers wafer light semiconductor semiconductors ai software lithography data center mirror mirrors "
            "engineers technology invention nanometres research",
    "history": "century centuries empire war wars colonial founded history historic nineteen eighteen ancient old dynasty",
}
TONE_WORDS = {k: set(v.split()) for k, v in LEXICON.items()}

DIRECTION = {  # the 12-point plan per tone (what the engine does with it is in remotion/src/animation-engine/tone.tsx)
    "bright": dict(palette="sky blue, gold, green; saturated", lighting="even daylight, soft shadows", intensity="lively, bouncy",
                   character="warm: smiles, hops, points; walks into scenes", backgrounds="open outdoor sets", charts="rounded bars, big numbers",
                   transitions="scan wipes, quick pops", music="A-minor pad, 6 s chords"),
    "thriller": dict(palette="slate, ink blue, desaturated; gold for money, red for the lie", lighting="low-key, one pool of light on the evidence, heavy vignette, film grain",
                     intensity="slow, deliberate; moments of stillness before revelations", character="serious: examines documents, connects evidence, points at gaps; never smiles or hops",
                     backgrounds="night offices, archives, vaults, courtrooms; no smiling sun, no clouds", charts="thin lines on dark screens, red highlights on inconsistencies",
                     transitions="slow cuts, scan lines, stamps", music="low A-minor pad with E-major tension, heartbeat pulse, 55 Hz drone"),
    "crisis": dict(palette="storm reds and bruised purples, high contrast", lighting="dusk, alarm pulse growing with the crisis",
                   intensity="accelerating; shakes and fast camera at the breaking points", character="restrained: draws cascades and contagion, no jokes",
                   backgrounds="trading floors, bank fronts, streets with queues; storm skies", charts="steep falls, warning indicators, contagion networks",
                   transitions="hard cuts, hits", music="D-minor progression, faster pulse, low drone"),
    "strategy": dict(palette="cool greys and blues, one accent per rival", lighting="clean, even, slight vignette", intensity="measured, diagrammatic",
                     character="neutral: draws maps of rivals, decisions and consequences", backgrounds="boardrooms, maps, company towers",
                     charts="side-by-side comparisons, networks", transitions="clean slides", music="C-major pad, light pulse"),
    "trade": dict(palette="ocean blues, cargo colours, bright but no faces in the sky", lighting="daylight, long horizons", intensity="exploratory, steady motion",
                  character="warm: walks through ports, draws routes", backgrounds="seas, ports, canals, cranes", charts="maps with moving routes, flows",
                  transitions="pans along routes", music="C-major pad, 5 s chords"),
    "tech": dict(palette="deep navy, cyan glow, white; precise", lighting="dark with cyan glow and a soft spotlight", intensity="precise, layered builds",
                 character="neutral: assembles components, draws cutaways", backgrounds="clean rooms, machines, data centres", charts="layered component diagrams, glowing networks",
                 transitions="scan lines, zoom-ins", music="E-minor pad with a high shimmer"),
    "history": dict(palette="sepia, parchment, muted primaries", lighting="archival, warm vignette, grain", intensity="calm, timeline-driven",
                    character="neutral: draws timelines and maps", backgrounds="period streets, maps, archives", charts="timelines, old-style ledgers",
                    transitions="page turns, dissolves", music="D-minor pad, slow 8 s chords"),
    "spectacle": dict(palette="vivid night-race colours, magenta and electric blue glow", lighting="floodlights, glow, light vignette", intensity="fast, energetic, camera tracking",
                      character="warm: points at the money behind the show", backgrounds="circuits, pit lanes, grandstands, studios", charts="bold bars, big numbers",
                      transitions="fast wipes, light sweeps", music="E-minor progression, 4 s chords, driving pulse"),
    "reflective": dict(palette="low-light blue-grey", lighting="dim, soft spotlight", intensity="slow, few elements", character="serious, still",
                       backgrounds="empty rooms, the opening image revisited", charts="one final number", transitions="slow fades",
                       music="slow A-minor pad, 9 s chords"),
}
PALETTES = {  # merged over project.yaml palette (cards, kinetic text, studio, chrome)
    "thriller": {"bg": "#0F1520", "bg2": "#1A2332", "ink": "#ECE7DC", "muted": "#8D98A8", "land": "#2A3546", "border": "#3E4C62",
                 "accent": "#D9A441", "accent2": "#7FA6C9", "accent3": "#5FAF83", "risk": "#E0473F"},
    "crisis": {"bg": "#1C1216", "bg2": "#2C1A1F", "ink": "#F3E9E4", "muted": "#B39A9A", "land": "#3A262B", "border": "#5A3A40",
               "accent": "#F2B134", "accent2": "#7FA6C9", "accent3": "#6FBF7F", "risk": "#FF4B3E"},
    "tech": {"bg": "#081226", "bg2": "#0F1F3F", "ink": "#E8F4FF", "muted": "#8AA4C2", "land": "#16294A", "border": "#2B4A78",
             "accent": "#3FD0FF", "accent2": "#9B8CFF", "accent3": "#3DDC97", "risk": "#FF5A6E"},
    "history": {"bg": "#EFE4CC", "bg2": "#F7F0DE", "ink": "#2E2416", "muted": "#7A6A52", "land": "#D8C59C", "border": "#8A7350",
                "accent": "#B5651D", "accent2": "#3E6A8A", "accent3": "#5E7D3A", "risk": "#A8322D"},
    "strategy": {"bg": "#E9EEF3", "bg2": "#F6F8FA", "ink": "#14202E", "muted": "#5A6B7E", "land": "#C9D6E3", "border": "#40566E",
                 "accent": "#E08A00", "accent2": "#2F6FD1", "accent3": "#23995A", "risk": "#D93A3A"},
}
SERIOUS = {"thriller", "crisis", "reflective"}


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def score(text: str) -> Counter:
    ws = words(text)
    bigrams = [" ".join(p) for p in zip(ws, ws[1:])]
    c = Counter()
    for tone, vocab in TONE_WORDS.items():
        c[tone] = sum(1 for w in ws if w in vocab) + 2 * sum(1 for b in bigrams if b in LEXICON[tone])
    return c


def classify(script: dict) -> dict:
    chapters, order = {}, []
    for s in script["segments"]:
        ch = s.get("chapter", "") or "(none)"
        if ch not in chapters:
            chapters[ch] = ""
            order.append(ch)
        chapters[ch] += " " + (s.get("narration") or "")
    total = Counter()
    per = {}
    for ch in order:
        sc = score(chapters[ch])
        per[ch] = sc
        total.update(sc)
    primary = total.most_common(1)[0][0] if total and total.most_common(1)[0][1] > 0 else "bright"
    secondary = [t for t, v in total.most_common(4) if t != primary and v >= 0.35 * total[primary]][:2]
    plan = []
    for i, ch in enumerate(order):
        sc = per[ch]
        best, val = (sc.most_common(1)[0] if sc else (primary, 0))
        tone = best if val >= 3 and val >= 1.4 * max(1, sc[primary]) else primary
        if i == len(order) - 1 and primary in SERIOUS:
            tone = "reflective"                      # conclusions of serious stories calm down
        plan.append({"chapter": ch, "tone": tone, "scores": dict(sc.most_common(3))})
    return {"primary": primary, "secondary": secondary, "chapters": plan, "totals": dict(total.most_common())}


def write_yaml(slug: str, res: dict, out: Path) -> dict:
    primary = res["primary"]
    vd = {
        "primary_tone": primary,
        "secondary_tones": res["secondary"],
        "palette": PALETTES.get(primary, {}),
        "presenter": {"demeanor": "serious" if primary in SERIOUS else ("neutral" if primary in {"strategy", "tech", "history"} else "warm"),
                      "min_sequences": 3 if primary in SERIOUS else 4},
        "chapters": [{"chapter": c["chapter"], "tone": c["tone"]} for c in res["chapters"] if c["chapter"] != "(none)"],
        "turning_points": [],
        "thumbnail": {"tone": primary, "headline": [], "idea": "one dominant object that states the central mystery"},
    }
    if not vd["palette"]:
        del vd["palette"]
    header = (f"# Visual direction for {slug} (APPLIED by the pipeline; see hiddeneco/visual_direction.py).\n"
              f"# Draft from tools/visual_direction.py: edit tones per chapter, add turning_points "
              f"[{{segment, cue, to}}], then commit.\n")
    out.write_text(header + yaml.safe_dump(vd, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    return vd


def write_doc(slug: str, vd: dict, res: dict | None, script: dict, doc: Path) -> None:
    p = vd.get("primary_tone", "bright")
    D = DIRECTION.get(p, DIRECTION["bright"])
    lines = [f"# Visual direction: {script.get('title', slug)}", "",
             "Generated by `tools/visual_direction.py` from the script, then reviewed. The YAML twin "
             f"(`projects/{slug}/visual_direction.yaml`) is applied to the render: palette, scene tones, tone shifts, "
             "presenter demeanour and the music bed all follow it.", "",
             f"1. **Primary emotional tone:** {p}",
             f"2. **Secondary tones:** {', '.join(vd.get('secondary_tones') or []) or 'none'}",
             f"3. **Colour palette:** {D['palette']}" + (f" (episode palette: bg {vd['palette'].get('bg')}, accent {vd['palette'].get('accent')}, risk {vd['palette'].get('risk')})" if vd.get('palette') else ""),
             f"4. **Lighting and contrast:** {D['lighting']}",
             f"5. **Animation intensity:** {D['intensity']}",
             f"6. **Character behaviour:** {D['character']} (demeanour `{(vd.get('presenter') or {}).get('demeanor', 'warm')}`, "
             f"at least {(vd.get('presenter') or {}).get('min_sequences', 4)} presenter sequences, only where they explain)",
             f"7. **Background design:** {D['backgrounds']}",
             f"8. **Charts and diagrams:** {D['charts']}",
             f"9. **Transitions:** {D['transitions']}",
             f"10. **Music and sound:** {D['music']}; the bed changes with each chapter's tone and crossfades at turning points",
             "11. **Key emotional turning points:**"]
    tps = vd.get("turning_points") or []
    chs = vd.get("chapters") or []
    prev = None
    for c in chs:
        if prev and c["tone"] != prev:
            lines.append(f"    - chapter \"{c['chapter']}\": {prev} → {c['tone']}")
        prev = c["tone"]
    for tp in tps:
        lines.append(f"    - inside `{tp['segment']}` at \"{tp['cue']}\": → {tp['to']}" + (f" ({tp['why']})" if tp.get("why") else ""))
    if not tps and len({c['tone'] for c in chs}) <= 1:
        lines.append("    - none: one atmosphere throughout")
    lines += ["12. **Scene-specific requirements:**"]
    for r in vd.get("requirements") or []:
        lines.append(f"    - {r}")
    lines += ["", "## Tone by chapter", "", "| Chapter | Tone | Lexicon scores |", "|---|---|---|"]
    sc = {c["chapter"]: c.get("scores", {}) for c in (res or {}).get("chapters", [])}
    for c in chs:
        lines.append(f"| {c['chapter']} | {c['tone']} | {', '.join(f'{k} {v}' for k, v in sc.get(c['chapter'], {}).items()) or '-'} |")
    th = vd.get("thumbnail") or {}
    lines += ["", "## Thumbnail (designed separately from the film)", "",
              f"- Tone: {th.get('tone', p)}; headline: {' / '.join(th.get('headline') or []) or '(to write)'}",
              f"- Dominant idea: {th.get('idea', '')}"]
    doc.mkdir(parents=True, exist_ok=True)
    (doc / "VISUAL_DIRECTION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "doc"])
    ap.add_argument("slug")
    ap.add_argument("--deliverable", default="documentary")
    ap.add_argument("--doc", default=None)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    proj = ROOT / "projects" / a.slug
    script = yaml.safe_load((proj / "deliverables" / a.deliverable / "script.yaml").read_text(encoding="utf-8"))
    out = proj / "visual_direction.yaml"
    res = classify(script)
    if a.cmd == "plan" and (a.force or not out.exists()):
        vd = write_yaml(a.slug, res, out)
        print(f"wrote {out.relative_to(ROOT)}: primary {res['primary']}, secondary {res['secondary']}")
    else:
        vd = yaml.safe_load(out.read_text(encoding="utf-8"))
        print(f"kept {out.relative_to(ROOT)} (primary {vd.get('primary_tone')}); classifier says {res['primary']}")
    if a.doc:
        write_doc(a.slug, vd, res, script, ROOT / a.doc)
        print(f"wrote {a.doc}/VISUAL_DIRECTION.md")


if __name__ == "__main__":
    main()
