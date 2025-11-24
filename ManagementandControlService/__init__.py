"""
ManagementandControlService package initializer.

This ensures the directory is treated as a Python package and exposes the FastAPI app instance for imports like:
    from ManagementandControlService import app
"""
from .app.main import app

__all__ = ["app"]
