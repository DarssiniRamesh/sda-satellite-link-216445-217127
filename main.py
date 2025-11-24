"""
Repository root entrypoint for running the Management and Control Service with:

    uvicorn main:app --host 0.0.0.0 --port 5000

This module imports the FastAPI app instance from the ManagementandControlService package
so preview runners and CI can start the service using `main:app`.
"""
# Try to import app from the service package; if that fails, adjust sys.path and retry
try:
    from ManagementandControlService import app  # type: ignore # noqa: F401
except Exception:
    import os
    import sys

    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    try:
        from ManagementandControlService import app  # type: ignore # noqa: F401
    except Exception as e:  # pragma: no cover
        raise ImportError(
            "Unable to import FastAPI app from ManagementandControlService.\n"
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
