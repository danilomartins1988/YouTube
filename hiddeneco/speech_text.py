"""Turn display text into what a narrator should *say* before it reaches a TTS engine.

Captions keep the written form ("In 1815", "$99,557", "52.7 percent"); the voice receives
"In eighteen fifteen", "ninety-nine thousand five hundred fifty-seven dollars",
"fifty-two point seven percent". This removes the most common source of robotic-sounding
narration: engines guessing how to read numbers.
"""
from __future__ import annotations

import re

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
        "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
SCALES = [(10 ** 12, "trillion"), (10 ** 9, "billion"), (10 ** 6, "million"), (1000, "thousand")]


def int_words(n: int) -> str:
    if n < 0:
        return "minus " + int_words(-n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    if n < 1000:
        rest = n % 100
        return ONES[n // 100] + " hundred" + (" " + int_words(rest) if rest else "")
    for value, name in SCALES:
        if n >= value:
            rest = n % value
            return int_words(n // value) + " " + name + (" " + int_words(rest) if rest else "")
    raise AssertionError


def year_words(y: int) -> str:
    """1815 -> eighteen fifteen; 1900 -> nineteen hundred; 2005 -> two thousand five;
    2023 -> twenty twenty-three."""
    if 2000 <= y <= 2009:
        return "two thousand" + (" " + ONES[y % 10] if y % 10 else "")
    hi, lo = divmod(y, 100)
    if lo == 0:
        return int_words(hi) + " hundred"
    return int_words(hi) + " " + ("oh " + ONES[lo] if lo < 10 else int_words(lo))


def number_words(token: str) -> str:
    """'100,000' -> one hundred thousand; '52.7' -> fifty-two point seven."""
    token = token.replace(",", "")
    if "." in token:
        whole, frac = token.split(".", 1)
        return int_words(int(whole or 0)) + " point " + " ".join(ONES[int(d)] for d in frac)
    return int_words(int(token))


_MONEY = re.compile(r"\$(\d[\d,]*(?:\.\d+)?)(\s+(?:million|billion|trillion))?")
_HASH = re.compile(r"#(\d+)")
_PERCENT = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s?%")
_YEAR = re.compile(r"(?<![\d,.$])\b(1[0-9]{3}|20[0-9]{2})\b(?![\d,.]*\d)(?!\s?%)")
_NUMBER = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)")
_TIMES = re.compile(r"(\d(?:\.\d+)?)×")


def spoken(text: str) -> str:
    out = _MONEY.sub(lambda m: number_words(m.group(1)) + (m.group(2) or "") + " dollars", text)
    out = _HASH.sub(lambda m: "number " + number_words(m.group(1)), out)
    out = _TIMES.sub(lambda m: number_words(m.group(1)) + " times", out)
    out = _PERCENT.sub(lambda m: number_words(m.group(1)) + " percent", out)
    out = _YEAR.sub(lambda m: year_words(int(m.group(1))), out)
    out = _NUMBER.sub(lambda m: number_words(m.group(1)), out)
    return re.sub(r"\s{2,}", " ", out)
