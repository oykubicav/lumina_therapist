"""Structured JSON logging with PII scrub in log fields.

Rules:
- NEVER log raw user_message. If a route wants to log context, it should
  log user_hash (session store computes this).
- Every log record includes request_id when available.
- Log level defaults to INFO; set LOG_LEVEL=DEBUG for local development.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "ts": time.time(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        # Merge in any extra fields set via logger.info(..., extra={...})
        for k in ("request_id", "session_id", "turn_id", "route",
                  "duration_ms", "status_code", "safety_route",
                  "intent_module", "rewrites", "used_fallback",
                  "critic_passed"):
            v = getattr(record, k, None)
            if v is not None:
                payload[k] = v
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging():
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
    # Quiet down noisy libraries
    for noisy in ("uvicorn.access", "urllib3", "httpx"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
