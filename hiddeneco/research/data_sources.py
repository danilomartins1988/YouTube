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


def gdp_population(codes: list[str], year: int, prefer_api: bool = True) -> dict[str, CountryYear]:
    global _API_FAILED
    if prefer_api and not offline() and not _API_FAILED:
        try:
            data = _from_worldbank_api(codes, year)
            if set(codes) <= set(data):
                log("data.source", method="worldbank_api", year=year, codes=codes)
                return data
        except Exception as exc:  # network blocked, API down, schema change...
            _API_FAILED = True  # don't retry for every claim in this run
            log("data.api_unavailable", error=repr(exc)[:200])
    data = _from_snapshot(codes, year)
    missing = sorted(set(codes) - set(data))
    if missing:
        raise KeyError(f"No data for {missing} in {year}; run `python -m hiddeneco data refresh`")
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
