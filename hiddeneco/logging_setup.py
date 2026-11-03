"""Structured JSON-lines logging: one file per project run plus human-readable console output."""
from __future__ import annotations

import json
import logging
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

_LOGGER_NAME = "hiddeneco"


class JsonLineFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "event": record.getMessage(),
        }
        payload.update(getattr(record, "fields", {}) or {})
        return json.dumps(payload, default=str)


class ConsoleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        fields = getattr(record, "fields", None)
        if fields:
            base += "  " + " ".join(f"{k}={v}" for k, v in fields.items())
        return base[:400]


def get_logger() -> logging.Logger:
    logger = logging.getLogger(_LOGGER_NAME)
    if not logger.handlers:
        from hiddeneco.config import env

        logger.setLevel(env("HIDDENECO_LOG_LEVEL", "INFO"))
        console = logging.StreamHandler(sys.stderr)
        console.setFormatter(ConsoleFormatter("%(asctime)s %(levelname)-7s %(message)s", "%H:%M:%S"))
        logger.addHandler(console)
        logger.propagate = False
    return logger


def attach_run_log(log_dir: Path) -> Path:
    """Add a JSON-lines file handler for this project run (idempotent per path)."""
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / "run.jsonl"
    logger = get_logger()
    for h in logger.handlers:
        if isinstance(h, logging.FileHandler) and Path(h.baseFilename) == path.resolve():
            return path
    fh = logging.FileHandler(path, encoding="utf-8")
    fh.setFormatter(JsonLineFormatter())
    logger.addHandler(fh)
    return path


def log(event: str, level: int = logging.INFO, **fields) -> None:
    get_logger().log(level, event, extra={"fields": fields})


@contextmanager
def step(name: str, **fields):
    """Time a pipeline step and log start/finish/failure as structured events."""
    start = time.perf_counter()
    log("step.start", step=name, **fields)
    try:
        yield
    except Exception as exc:
        log("step.error", logging.ERROR, step=name, error=repr(exc),
            seconds=round(time.perf_counter() - start, 3))
        raise
    log("step.done", step=name, seconds=round(time.perf_counter() - start, 3), **fields)
