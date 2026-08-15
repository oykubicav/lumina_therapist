"""Request-ID middleware.

Attaches a UUID to every request (or reuses X-Request-ID header from a
reverse proxy). Available in handlers as `request.state.request_id`.
Returned as X-Request-ID response header for client-side correlation.

Also emits a single structured access log per request with:
  request_id, method, path, status, duration_ms
NO body content is ever logged — that's the whole point.
"""

from __future__ import annotations

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


log = logging.getLogger("api.access")


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = rid
        start = time.time()
        response = None
        status = 500
        try:
            response = await call_next(request)
            status = response.status_code
            return response
        finally:
            duration_ms = (time.time() - start) * 1000
            log.info(
                "http_request",
                extra={
                    "request_id": rid,
                    "route": f"{request.method} {request.url.path}",
                    "status_code": status,
                    "duration_ms": round(duration_ms, 1),
                },
            )
            if response is not None:
                response.headers["x-request-id"] = rid
