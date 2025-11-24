"""
Repository root entrypoint for running the Management and Control Service with:

    uvicorn main:app --host 0.0.0.0 --port 5000

This module imports the FastAPI app instance from the ManagementandControlService package
so preview runners and CI can start the service using `main:app`.
"""
from ManagementandControlService import app  # noqa: F401

# PUBLIC_INTERFACE
def get_app():
    """Return the FastAPI app for programmatic usage."""
    return app
