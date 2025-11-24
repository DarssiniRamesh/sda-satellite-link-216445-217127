"""
ManagementandControlService FastAPI application package.

Exposes the FastAPI app instance via app.main:app and provides package-level metadata.
"""

from .main import app as app  # re-export for convenience
