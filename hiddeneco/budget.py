"""Hard spending cap for paid APIs.

Every paid request is checked *before* it is sent: if the estimated cost of the request plus what was
already spent for this topic would exceed the cap, the request is refused and the build stops.
Spending is recorded per topic in output/<slug>/paid_spend.json, so the cap holds across rebuilds.
Estimates use the (conservative) prices in config/settings.yaml - check the vendor's bill too.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from hiddeneco.logging_setup import log


class BudgetExceeded(RuntimeError):
    pass


class Budget:
    def __init__(self, path: Path, cap_usd: float, usd_per_1k_chars: float | None, provider: str):
        if usd_per_1k_chars is None:
            raise BudgetExceeded(f"No price configured for paid provider '{provider}'; refusing to spend blindly.")
        self.path, self.cap, self.rate, self.provider = path, float(cap_usd), float(usd_per_1k_chars), provider
        self.data = json.loads(path.read_text()) if path.exists() else {"cap_usd": self.cap, "entries": []}

    @property
    def spent(self) -> float:
        return round(sum(e["usd"] for e in self.data["entries"]), 6)

    def cost(self, chars: int) -> float:
        return chars * self.rate / 1000

    def remaining(self) -> float:
        return round(self.cap - self.spent, 6)

    def check(self, chars: int, what: str = "") -> None:
        need = self.cost(chars)
        if self.spent + need > self.cap + 1e-9:
            raise BudgetExceeded(
                f"Paid TTS refused: {what or 'request'} needs ~${need:.4f}, already spent ${self.spent:.4f} "
                f"of the ${self.cap:.2f} cap.")

    def charge(self, chars: int, what: str) -> None:
        entry = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "provider": self.provider,
                 "chars": chars, "usd": round(self.cost(chars), 6), "what": what[:80]}
        self.data["entries"].append(entry)
        self.data["cap_usd"] = self.cap
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2))
        log("budget.charge", provider=self.provider, chars=chars, usd=entry["usd"], spent=self.spent, cap=self.cap)
