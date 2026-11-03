"""Build the source-backed research dossier for a project.

Inputs : projects/<slug>/sources.yaml   (human-curated sources + claims + data-claim specs)
Outputs: output/<slug>/research/dossier.json and dossier.md

Rules enforced here:
* every claim must cite at least one known source id with a URL and access date;
* data claims are computed from cited datasets, never typed in by hand;
* anything not verified is surfaced in an explicit "requires verification" list.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

from hiddeneco.config import ProjectPaths
from hiddeneco.logging_setup import log
from hiddeneco.models import VERIFIED_STATUSES, Claim, Dossier, Source
from hiddeneco.research import data_sources
from hiddeneco.research.formatting import FORMATTERS


class DossierError(ValueError):
    pass


def _data_claim(spec: dict, cache: dict) -> tuple[Claim, dict]:
    year = int(spec["year"])
    codes = list(spec.get("countries") or [c for c in (spec.get("country"), spec.get("other")) if c])
    key = (tuple(sorted(codes)), year)
    if key not in cache:
        cache[key] = data_sources.gdp_population(codes, year)
    data = cache[key]
    metric = spec["metric"]
    fmt_s = FORMATTERS[spec.get("spoken_format", "raw")]
    fmt_d = FORMATTERS[spec.get("display_format", "raw")]
    c = spec.get("country")
    if metric == "gdp_per_capita_usd":
        value = data[c].gdp_per_capita_usd
        text = f"{data[c].name}'s GDP per capita in {year} was {FORMATTERS['usd'](value)} (current US$)."
    elif metric == "population":
        value = data[c].population
        text = f"{data[c].name}'s population in {year} was {value:,.0f}."
    elif metric == "ratio_gdp_per_capita":
        o = spec["other"]
        value = data[c].gdp_per_capita_usd / data[o].gdp_per_capita_usd
        text = (f"In {year}, {data[c].name}'s GDP per capita was {value:.2f} times that of "
                f"{data[o].name} ({FORMATTERS['usd'](data[c].gdp_per_capita_usd)} vs "
                f"{FORMATTERS['usd'](data[o].gdp_per_capita_usd)}).")
    elif metric == "gdp_per_capita_usd_table":
        value = [{"code": k, "name": spec.get("labels", {}).get(k, data[k].name),
                  "value": data[k].gdp_per_capita_usd} for k in codes]
        text = f"GDP per capita (current US$), {year}: " + "; ".join(
            f"{v['name']} {FORMATTERS['usd'](v['value'])}" for v in value)
        claim = Claim(id=spec["id"], text=text, value=value, source_ids=spec["source_ids"],
                      status="data_derived", fields={"year": year},
                      derived_from={"metric": metric, "year": year,
                                    "method": sorted({data[k].method for k in codes})})
        return claim, {k: data[k].__dict__ for k in codes}
    else:
        raise DossierError(f"Unknown data metric '{metric}' in claim {spec['id']}")
    claim = Claim(id=spec["id"], text=text, spoken=fmt_s(value), display=fmt_d(value), value=value,
                  source_ids=spec["source_ids"], status="data_derived", fields={"year": year},
                  derived_from={"metric": metric, "year": year,
                                "method": sorted({data[k].method for k in codes})})
    return claim, {k: data[k].__dict__ for k in codes}


def build_dossier(paths: ProjectPaths) -> Dossier:
    spec = yaml.safe_load((paths.project_dir / "sources.yaml").read_text(encoding="utf-8"))
    project = yaml.safe_load((paths.project_dir / "project.yaml").read_text(encoding="utf-8"))
    sources = [Source(**s) for s in spec["sources"]]
    claims = [Claim(**c) for c in spec.get("claims", [])]
    datasets: dict = {}
    cache: dict = {}
    for dc in spec.get("data_claims", []):
        claim, raw = _data_claim(dc, cache)
        claims.append(claim)
        datasets[dc["id"]] = raw
    dossier = Dossier(slug=paths.slug, title=project["title"],
                      generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                      sources=sources, claims=claims, datasets=datasets,
                      open_questions=spec.get("open_questions", []))
    validate(dossier)
    return dossier


def validate(dossier: Dossier) -> None:
    ids = [s.id for s in dossier.sources]
    if len(ids) != len(set(ids)):
        raise DossierError("Duplicate source ids")
    cids = [c.id for c in dossier.claims]
    if len(cids) != len(set(cids)):
        raise DossierError("Duplicate claim ids")
    for s in dossier.sources:
        if not s.url.startswith(("https://", "http://")):
            raise DossierError(f"Source {s.id} has no valid URL")
    for c in dossier.claims:
        if not c.source_ids:
            raise DossierError(f"Claim {c.id} cites no source")
        for sid in c.source_ids:
            if sid not in ids:
                raise DossierError(f"Claim {c.id} cites unknown source '{sid}'")
        if c.status == "human_verified" and not c.verified_by:
            raise DossierError(f"Claim {c.id} is human_verified but has no verified_by")


def unverified(dossier: Dossier) -> list[Claim]:
    return [c for c in dossier.claims if c.status not in VERIFIED_STATUSES]


def to_markdown(d: Dossier) -> str:
    lines = [f"# Research dossier: {d.title}", "", f"Generated {d.generated_at}.", "",
             "## Claims", "", "| ID | Claim | Status | Sources |", "|---|---|---|---|"]
    for c in d.claims:
        lines.append(f"| `{c.id}` | {c.text} | **{c.status}** | {', '.join(c.source_ids)} |")
    pending = unverified(d)
    lines += ["", "## Claims that require verification before publishing", ""]
    if pending:
        for c in pending:
            lines.append(f"- `{c.id}` ({c.status}): {c.text}  \n  _Note:_ {c.verification_note or '-'}")
    else:
        lines.append("None.")
    lines += ["", "## Sources", "", "| ID | Title | Publisher | Published | Accessed | Kind | URL |",
              "|---|---|---|---|---|---|---|"]
    for s in d.sources:
        lines.append(f"| `{s.id}` | {s.title} | {s.publisher} | {s.published or 'n/a'} | {s.accessed} "
                     f"| {s.kind} | {s.url} |")
    if d.open_questions:
        lines += ["", "## Open research questions", ""] + [f"- {q}" for q in d.open_questions]
    return "\n".join(lines) + "\n"


def write(d: Dossier, paths: ProjectPaths) -> Path:
    out = paths.out_sub("research")
    (out / "dossier.json").write_text(d.model_dump_json(indent=2), encoding="utf-8")
    (out / "dossier.md").write_text(to_markdown(d), encoding="utf-8")
    log("dossier.written", claims=len(d.claims), unverified=len(unverified(d)), path=str(out))
    return out / "dossier.json"


def load(paths: ProjectPaths) -> Dossier:
    return Dossier(**json.loads((paths.out / "research" / "dossier.json").read_text(encoding="utf-8")))
