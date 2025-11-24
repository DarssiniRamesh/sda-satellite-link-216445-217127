"""
ASGI shim module.

This module re-exports the FastAPI application instance from app.main so that
both `uvicorn main:app` and `uvicorn app.main:app` resolve correctly.
"""

from app.main import app as app  # noqa: F401

# PUBLIC_INTERFACE
def get_app():
    """Return the FastAPI app instance for external tooling."""
    return app
