"""Retry with exponential backoff for flaky network calls (paid TTS, data APIs)."""
from __future__ import annotations

import time
from typing import Callable, TypeVar

from hiddeneco.logging_setup import log

T = TypeVar("T")


def retry(fn: Callable[[], T], attempts: int = 4, base_delay: float = 2.0, what: str = "call",
          retry_on: tuple[type[BaseException], ...] = (Exception,), sleep=time.sleep) -> T:
    for i in range(1, attempts + 1):
        try:
            return fn()
        except retry_on as exc:
            if i == attempts:
                raise
            delay = base_delay * 2 ** (i - 1)
            log("retry", what=what, attempt=i, delay_s=delay, error=repr(exc)[:200])
            sleep(delay)
    raise AssertionError("unreachable")
