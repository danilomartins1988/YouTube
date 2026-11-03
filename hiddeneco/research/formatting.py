"""Turn numbers into on-screen and spoken forms without changing what they mean."""
from __future__ import annotations

import math

_HALF_STEPS = {1.5: "one and a half times", 2.0: "twice", 2.5: "two and a half times",
               3.0: "three times", 3.5: "three and a half times", 4.0: "four times", 5.0: "five times"}


def sig_round(x: float, sig: int) -> float:
    if x == 0:
        return 0.0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)


def usd(x: float) -> str:
    return f"${x:,.0f}"


def usd_rough(x: float) -> str:
    """'almost 100,000 dollars' when within 1% below a 2-sig-fig round number, else 3 sig figs."""
    two = sig_round(x, 2)
    if two > x and (two - x) / two <= 0.01:
        return f"almost {two:,.0f} dollars"
    return f"roughly {sig_round(x, 3):,.0f} dollars"


def millions(x: float) -> str:
    return f"{x / 1e6:.1f} million"


def millions_words(x: float) -> str:
    return f"about {x / 1e6:.1f} million"


def ratio(x: float) -> str:
    return f"{x:.1f}×"


def ratio_words(r: float) -> str:
    target = min(_HALF_STEPS, key=lambda k: abs(k - r))
    gap = (r - target) / target
    if abs(gap) <= 0.03:
        return f"about {_HALF_STEPS[target]}"
    if -0.10 <= gap < 0:
        return f"almost {_HALF_STEPS[target]}"
    if 0 < gap <= 0.10:
        return f"more than {_HALF_STEPS[target]}"
    return f"about {r:.1f} times"


def percent(x: float, digits: int = 1) -> str:
    return f"{x:.{digits}f}%"


FORMATTERS = {
    "usd": usd, "usd_rough": usd_rough, "millions": millions, "millions_words": millions_words,
    "ratio": ratio, "ratio_words": ratio_words, "percent": percent, "raw": str,
}
