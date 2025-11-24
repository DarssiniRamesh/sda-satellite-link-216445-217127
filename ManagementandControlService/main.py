"""
Top-level ASGI entrypoint for the Management and Control Service.

- Exposes `app` imported from src.api.main so `uvicorn main:app` works.
- When executed directly, runs uvicorn bound to 0.0.0.0 honoring env PORT,
  defaulting to 3000 per project standard.
"""

from __future__ import annotations

import logging
import os
from typing import Final, List

from src.api.main import app as app  # re-export for ASGI import
"""FastAPI app instance re-exported for uvicorn entrypoint (main:app)."""

# Explicit re-export for linters and import tools
__all__ = ["app", "get_bind_host", "get_bind_port"]

# Port/host defaults
_DEFAULT_PORT: Final[int] = 3000
_DEFAULT_HOST: Final[str] = "0.0.0.0"


def _parse_port(value: str | None, default: int) -> int:
    """
    Parse a port value from string and validate range 1..65535.

    Args:
        value: The string value from the environment or None.
        default: The fallback port if parsing/validation fails.

    Returns:
        int: The validated port.
    """
    if not value:
        return default
    value = value.strip()
    try:
        port = int(value)
    except (TypeError, ValueError):
        logging.getLogger(__name__).warning("Invalid PORT value '%s'; falling back to default %s", value, default)
        return default
    if 1 <= port <= 65535:
        return port
    logging.getLogger(__name__).warning("PORT %s out of range; falling back to default %s", port, default)
    return default


def _get_port_from_env() -> int:
    """
    Resolve the port from the environment variable PORT.

    Accepts any valid port in range 1..65535. Defaults to 3000.
    """
    return _parse_port(os.getenv("PORT"), _DEFAULT_PORT)


def _configure_logging() -> None:
    """
    Configure basic application logging for local development runs.
    In production, rely on the platform's logging configuration.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    logging.getLogger(__name__).info("Logging configured.")


# PUBLIC_INTERFACE
def get_bind_host() -> str:
    """Return the bind host for the service."""
    return _DEFAULT_HOST


# PUBLIC_INTERFACE
def get_bind_port() -> int:
    """Return the bind port derived from environment with allowed defaults."""
    return _get_port_from_env()


if __name__ == "__main__":
    # Optional dev runner: uvicorn is imported here to avoid dependency at import-time for ASGI.
    _configure_logging()
    host = get_bind_host()
    port = get_bind_port()

    try:
        import uvicorn  # type: ignore
    except Exception as exc:
        logging.getLogger(__name__).error(
            "Failed to import uvicorn. Ensure dependencies are installed. Error: %s", exc
        )
        raise

    logging.getLogger(__name__).info("Starting server on %s:%s", host, port)
    logging.getLogger(__name__).info("Swagger UI: http://%s:%s/docs", host, port)
    logging.getLogger(__name__).info("OpenAPI JSON: http://%s:%s/openapi.json", host, port)
    uvicorn.run("main:app", host=host, port=port, reload=False)
