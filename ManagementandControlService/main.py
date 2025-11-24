"""
ASGI shim module.

This module re-exports the FastAPI application instance from app.main so that
both `uvicorn main:app` and `uvicorn app.main:app` resolve correctly.
"""

from fastapi import FastAPI
from app.main import app as app  # noqa: F401

# PUBLIC_INTERFACE
def get_app() -> FastAPI:
    """
    Return the FastAPI app instance for external tooling or programmatic execution.

    Returns:
        FastAPI: The configured FastAPI application instance re-exported from app.main.
    """
    return app
