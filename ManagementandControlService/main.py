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

# Allowed ports for the environment. Do not change without coordination.
_ALLOWED_PORTS: Final[List[int]] = [3000, 3001, 3002, 5000]
_DEFAULT_PORT: Final[int] = 3000
_DEFAULT_HOST: Final[str] = "0.0.0.0"


def _get_port_from_env() -> int:
    """
    Resolve the port from the environment variable PORT, ensuring it is within the allowed set.

    Returns:
        int: The resolved port number. Defaults to 3000.
    """
    raw_port = os.getenv("PORT", "").strip()
    if raw_port:
        try:
            port = int(raw_port)
            if port in _ALLOWED_PORTS:
                return port
            logging.getLogger(__name__).warning(
                "PORT %s not allowed; falling back to default %s", port, _DEFAULT_PORT
            )
        except ValueError:
            logging.getLogger(__name__).warning(
                "Invalid PORT value '%s'; falling back to default %s", raw_port, _DEFAULT_PORT
            )
    return _DEFAULT_PORT


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
    uvicorn.run("main:app", host=host, port=port, reload=False)
