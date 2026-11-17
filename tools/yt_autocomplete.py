"""Collect real YouTube autocomplete suggestions (US English) for SEO research. Evidence only: no volumes.

    python tools/yt_autocomplete.py "why are chinese cars" "chinese ev" [--expand]   # --expand adds a..z suffixes
Prints JSON {seed: [suggestions]}. Source: suggestqueries.google.com (ds=yt, hl=en, gl=us). Timestamp included.
"""
import json, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone

def suggest(q):
    url = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(
        {"client": "firefox", "ds": "yt", "hl": "en", "gl": "us", "q": q})
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read().decode("utf-8", "replace"))[1]

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    expand = "--expand" in sys.argv
    out = {"collected_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "source": "YouTube autocomplete (US, en)", "results": {}}
    for seed in args:
        qs = [seed] + ([f"{seed} {c}" for c in "abcdefghijklmnopqrstuvwxyz"] if expand else [])
        for q in qs:
            try:
                out["results"][q] = suggest(q)
            except Exception as e:  # noqa: BLE001
                out["results"][q] = f"ERROR {e}"
            time.sleep(0.3)
    print(json.dumps(out, indent=1, ensure_ascii=False))
