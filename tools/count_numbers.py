"""Count spoken numbers/percentages in narration text (story-over-stats budget: <=12 per film, <=1 per scene).

    python tools/count_numbers.py <file> [<file>...]     # any text/markdown/yaml/json with narration
Counts digit groups (incl. $, %, decimals) and spelled-out number words. Prints total and the densest lines.
"""
import re, sys
WORDS = r"\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|trillion|percent|half|quarter|third)\b"
NUM = r"[$€£]?\d[\d,]*(\.\d+)?\s?(%|percent|bn|billion|million|trillion|k)?"
total, rows = 0, []
for path in sys.argv[1:]:
    for i, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        n = len(re.findall(NUM, line)) + len(re.findall(WORDS, line, re.I))
        if n:
            total += n; rows.append((n, path, i, line.strip()[:110]))
print(f"numbers mentioned: {total}  (budget: 8-12 spoken per film)")
for n, p, i, l in sorted(rows, reverse=True)[:12]:
    print(f"{n:>3}  {p}:{i}  {l}")
