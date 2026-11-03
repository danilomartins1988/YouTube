"""Per-video cost ledger. Unknown prices stay unknown (None) rather than being guessed."""
from __future__ import annotations

import json
from pathlib import Path

from hiddeneco.config import settings
from hiddeneco.models import CostLine


def tts_cost(provider: str, chars: int, step: str = "tts", estimated: bool = True) -> CostLine:
    price = settings()["pricing"].get(provider, {})
    per_1k = price.get("usd_per_1k_chars")
    usd = None if per_1k is None else round(per_1k * chars / 1000, 4)
    return CostLine(step=step, provider=provider, units=chars, unit="characters",
                    usd_per_unit=None if per_1k is None else per_1k / 1000, usd=usd, estimated=estimated,
                    note=f"pricing verified_on: {price.get('verified_on', 'unknown')}")


def compute_cost(seconds: float, step: str) -> CostLine:
    price = settings()["pricing"]["local_compute"]
    hours = seconds / 3600
    return CostLine(step=step, provider="local_cpu", units=round(hours, 4), unit="cpu_hours", estimated=False,
                    usd_per_unit=price["usd_per_cpu_hour"],
                    usd=round(hours * price["usd_per_cpu_hour"], 4),
                    note=price["verified_on"])


class CostLedger:
    def __init__(self, path: Path):
        self.path = path
        self.lines: list[CostLine] = []
        if path.exists():
            self.lines = [CostLine(**x) for x in json.loads(path.read_text())["lines"]]

    def replace_step(self, step: str, line: CostLine) -> None:
        self.lines = [x for x in self.lines if x.step != step] + [line]
        self.save()

    def total(self) -> tuple[float, bool]:
        """Return (known total, whether any line has an unknown price)."""
        known = sum(x.usd for x in self.lines if x.usd is not None)
        return round(known, 4), any(x.usd is None for x in self.lines)

    def save(self) -> None:
        total, unknown = self.total()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(
            {"lines": [x.model_dump() for x in self.lines], "total_usd_known": total,
             "has_unknown_prices": unknown}, indent=2))

    def markdown(self, brl_per_usd: float | None = None) -> str:
        """Estimated (before running) and actual (what was really consumed) lines, separately."""
        rows = ["| Kind | Step | Provider | Units | USD | Note |", "|---|---|---|---|---|---|"]
        for x in sorted(self.lines, key=lambda x: (not x.estimated, x.step)):
            usd = "unknown" if x.usd is None else f"${x.usd:.4f}"
            rows.append(f"| {'estimate' if x.estimated else 'actual'} | {x.step} | {x.provider} | "
                        f"{x.units:g} {x.unit} | {usd} | {x.note} |")
        actual = [x for x in self.lines if not x.estimated]
        total = round(sum(x.usd for x in actual if x.usd is not None), 4)
        unknown = any(x.usd is None for x in actual)
        rows.append(f"| **actual total** | | | | **${total:.4f}**{' + unknown' if unknown else ''} | |")
        if brl_per_usd:
            rows.append(f"| | | | | ~BRL {total * brl_per_usd:.2f} | at an assumed {brl_per_usd} BRL/USD |")
        return "\n".join(rows)
