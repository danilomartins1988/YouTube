"""Statistical data access. Official API first, licensed mirror second, committed snapshot last.

Every value returned carries the method used so the dossier can report it honestly.
"""
from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass
from pathlib import Path

import requests

from hiddeneco.config import REPO_ROOT, offline
from hiddeneco.logging_setup import log

SNAPSHOT = REPO_ROOT / "data" / "snapshots" / "worldbank_gdp_population.csv"
WB_API = "https://api.worldbank.org/v2/country/{codes}/indicator/{indicator}?format=json&date={year}&per_page=500"
MIRRORS = {
    "gdp": "https://raw.githubusercontent.com/datasets/gdp/main/data/gdp.csv",
    "population": "https://raw.githubusercontent.com/datasets/population/main/data/population.csv",
}


@dataclass
class CountryYear:
    code: str
    name: str
    year: int
    gdp_usd: float | None
    population: float | None
    gdp_per_capita_usd: float | None
    method: str            # "worldbank_api:NY.GDP.PCAP.CD" or "derived:GDP/population (snapshot)"


def _from_worldbank_api(codes: list[str], year: int, timeout: float = 15) -> dict[str, CountryYear]:
    out: dict[str, CountryYear] = {}
    joined = ";".join(codes)
    series = {}
    for key, ind in (("pc", "NY.GDP.PCAP.CD"), ("gdp", "NY.GDP.MKTP.CD"), ("pop", "SP.POP.TOTL")):
        resp = requests.get(WB_API.format(codes=joined, indicator=ind, year=year), timeout=timeout)
        resp.raise_for_status()
        payload = resp.json()
        if len(payload) < 2 or payload[1] is None:
            raise RuntimeError(f"World Bank API returned no data for {ind}")
        series[key] = {row["countryiso3code"]: row for row in payload[1]}
    for code in codes:
        pc = series["pc"].get(code)
        if not pc or pc["value"] is None:
            continue
        out[code] = CountryYear(code=code, name=pc["country"]["value"], year=year,
                                gdp_usd=(series["gdp"].get(code) or {}).get("value"),
                                population=(series["pop"].get(code) or {}).get("value"),
                                gdp_per_capita_usd=pc["value"],
                                method="worldbank_api:NY.GDP.PCAP.CD")
    return out


def _from_snapshot(codes: list[str], year: int, path: Path = SNAPSHOT) -> dict[str, CountryYear]:
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["country_code"] in codes and int(row["year"]) == year:
                gdp, pop = float(row["gdp_current_usd"]), float(row["population"])
                out[row["country_code"]] = CountryYear(
                    code=row["country_code"], name=row["country_name"], year=year, gdp_usd=gdp,
                    population=pop, gdp_per_capita_usd=gdp / pop,
                    method="derived:NY.GDP.MKTP.CD / SP.POP.TOTL (committed snapshot)")
    return out


_API_FAILED = False
_USED: set[str] = set()     # "api" / "snapshot": which kinds of source this run has drawn from


def reset_run() -> None:
    """Start a fresh run: retry the API and forget which sources were used."""
    global _API_FAILED
    _API_FAILED = False
    _USED.clear()


def force_snapshot() -> None:
    """Use only the committed snapshot for the rest of this run."""
    global _API_FAILED
    _API_FAILED = True
    _USED.clear()


def sources_used() -> set[str]:
    return set(_USED)


def gdp_population(codes: list[str], year: int, prefer_api: bool = True) -> dict[str, CountryYear]:
    global _API_FAILED
    if prefer_api and not offline() and not _API_FAILED:
        try:
            data = _from_worldbank_api(codes, year)
            if set(codes) <= set(data):
                _USED.add("api")
                log("data.source", method="worldbank_api", year=year, codes=codes)
                return data
        except Exception as exc:  # network blocked, API down, schema change...
            _API_FAILED = True  # don't retry for every claim in this run
            log("data.api_unavailable", error=repr(exc)[:200])
    data = _from_snapshot(codes, year)
    missing = sorted(set(codes) - set(data))
    if missing:
        raise KeyError(f"No data for {missing} in {year}; run `python -m hiddeneco data refresh`")
    _USED.add("snapshot")
    log("data.source", method="snapshot", year=year, codes=codes)
    return data


def refresh_snapshot(codes: list[str] | None = None, path: Path = SNAPSHOT, timeout: float = 60) -> int:
    """Re-download the licensed mirror CSVs and rewrite the committed snapshot subset."""
    existing = set()
    if codes is None and path.exists():
        with open(path, newline="", encoding="utf-8") as fh:
            existing = {r["country_code"] for r in csv.DictReader(fh)}
    wanted = set(codes or existing)
    tables = {}
    for key, url in MIRRORS.items():
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        tables[key] = {(r["Country Code"], int(r["Year"])): (r["Country Name"], r["Value"])
                       for r in csv.DictReader(io.StringIO(resp.text))}
    rows = []
    for (code, year), (name, gdp) in sorted(tables["gdp"].items()):
        if code in wanted and year >= 2000 and (code, year) in tables["population"]:
            rows.append([code, name, year, gdp, tables["population"][(code, year)][1]])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["country_code", "country_name", "year", "gdp_current_usd", "population"])
        w.writerows(rows)
    log("data.snapshot_refreshed", rows=len(rows), path=str(path))
    return len(rows)


def dump(data: dict[str, CountryYear]) -> str:
    return json.dumps({k: v.__dict__ for k, v in data.items()}, indent=2)


def gdp_per_capita_series(codes: list[str], y0: int, y1: int) -> tuple[dict[str, list[dict]], str, dict]:
    """{code: [{year, value}]} plus the method used and country names. API first, snapshot fallback."""
    global _API_FAILED
    if not offline() and not _API_FAILED:
        try:
            url = WB_API.format(codes=";".join(codes), indicator="NY.GDP.PCAP.CD", year=f"{y0}:{y1}")
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            rows = resp.json()[1]
            out, names = {c: [] for c in codes}, {}
            for r in rows:
                c = r["countryiso3code"]
                if c in out and r["value"] is not None:
                    out[c].append({"year": int(r["date"]), "value": r["value"]})
                    names[c] = r["country"]["value"]
            if all(len(v) == y1 - y0 + 1 for v in out.values()):
                _USED.add("api")
                return {c: sorted(v, key=lambda x: x["year"]) for c, v in out.items()}, \
                    "worldbank_api:NY.GDP.PCAP.CD", names
        except Exception as exc:
            _API_FAILED = True
            log("data.api_unavailable", error=repr(exc)[:200])
    out, names = {c: [] for c in codes}, {}
    with open(SNAPSHOT, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            c, y = row["country_code"], int(row["year"])
            if c in out and y0 <= y <= y1:
                out[c].append({"year": y, "value": float(row["gdp_current_usd"]) / float(row["population"])})
                names[c] = row["country_name"]
    missing = [c for c, v in out.items() if len(v) != y1 - y0 + 1]
    if missing:
        raise KeyError(f"Incomplete series for {missing} in {y0}-{y1}")
    _USED.add("snapshot")
    return {c: sorted(v, key=lambda x: x["year"]) for c, v in out.items()}, \
        "derived:NY.GDP.MKTP.CD / SP.POP.TOTL (committed snapshot)", names
