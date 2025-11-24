"""
Shim entrypoint for running uvicorn from the ManagementandControlService directory.

Usage (from this directory):
    uvicorn main:app --host 0.0.0.0 --port 5000

This file robustly exposes `app` by attempting multiple import strategies so that
it works both when executed inside the container and in local development.
Order of attempts:
1) from app.main import app
2) Adjust sys.path to include parent directory and import from ManagementandControlService.app.main
"""

from __future__ import annotations

import os
import sys

# Try relative-style import when current dir is ManagementandControlService
try:
    from app.main import app  # type: ignore
except Exception:
    # Fallback: adjust sys.path to include parent directory (repo root)
    # so that "ManagementandControlService.app.main" becomes importable
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    try:
        from ManagementandControlService.app.main import app  # type: ignore
    except Exception as e:
        # Final safety: provide a clear error to help diagnose import issues
        raise ImportError(
            "Unable to import FastAPI app. Tried:\n"
            "  1) from app.main import app\n"
            "  2) After sys.path fallback, from ManagementandControlService.app.main import app\n"
            f"Working directory: {os.getcwd()}\n"
            f"__file__: {__file__}\n"
            f"sys.path: {sys.path}\n"
        ) from e


# PUBLIC_INTERFACE
def get_app():
    """
    Return the FastAPI app for programmatic usage.

    Returns:
        The FastAPI application instance.
    """
    return app
