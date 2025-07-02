import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Any

import orjson
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        log_dict: dict[str, Any] = {
            "level": record.levelname,
            "time": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S"),
            "msg": record.getMessage(),
            "logger": record.name,
            "request_id": request_id.get(None),
        }
        if record.exc_info:
            log_dict["exc_info"] = self.formatException(record.exc_info)
        return orjson.dumps(log_dict).decode()


request_id: ContextVar[str | None] = ContextVar("request_id", default=None)


def setup_logging() -> None:
    """Конфигурируем root-логгер один раз при старте приложения."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
        force=True,
    )


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        _token = request_id.set(str(uuid.uuid4()))
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id.get()
            return response
        finally:
            request_id.reset(_token)
