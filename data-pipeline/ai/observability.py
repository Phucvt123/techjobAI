"""Small observability helpers for AI endpoints and agent runs."""

from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from typing import Iterator


logger = logging.getLogger("techjob_ai")

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s "
            "event=%(event)s session_id=%(session_id)s %(message)s"
        )
    )
    logger.addHandler(handler)

logger.setLevel(logging.INFO)


def log_ai_event(event: str, session_id: str = "-", **fields) -> None:
    """Log a structured-ish AI event without requiring extra dependencies."""
    safe_fields = {
        key: value
        for key, value in fields.items()
        if value is not None
    }
    message = " ".join(f"{key}={value!r}" for key, value in safe_fields.items())
    logger.info(message, extra={"event": event, "session_id": session_id})


@contextmanager
def timed_ai_event(event: str, session_id: str = "-", **fields) -> Iterator[dict]:
    """Measure latency and emit one completion/failure log event."""
    started = time.perf_counter()
    context: dict = {}
    try:
        yield context
        log_ai_event(
            f"{event}.success",
            session_id=session_id,
            latency_ms=round((time.perf_counter() - started) * 1000),
            **fields,
            **context,
        )
    except Exception as exc:
        log_ai_event(
            f"{event}.error",
            session_id=session_id,
            latency_ms=round((time.perf_counter() - started) * 1000),
            error_type=type(exc).__name__,
            error=str(exc)[:300],
            **fields,
            **context,
        )
        raise
