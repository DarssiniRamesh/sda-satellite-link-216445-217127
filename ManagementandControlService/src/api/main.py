from __future__ import annotations

from typing import Dict, Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance.

    Returns:
        FastAPI: Configured FastAPI application with health endpoints and CORS.
    """
    application = FastAPI(
        title="Management and Control Service",
        description="FastAPI app providing management, control, and telemetry interfaces.",
        version="0.1.0",
        openapi_tags=[{"name": "Health", "description": "Service health and readiness"}],
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/", summary="Health Check", tags=["Health"])
    # PUBLIC_INTERFACE
    def health_check() -> Dict[str, str]:
        """Simple health check endpoint."""
        return {"message": "Healthy"}

    @application.get("/health", summary="Readiness/Health probe", tags=["Health"])
    # PUBLIC_INTERFACE
    def readiness() -> Dict[str, str]:
        """Readiness endpoint for liveness probes."""
        return {"status": "ok"}

    return application


# Expose `app` at module level for ASGI servers and imports.
# PUBLIC_INTERFACE
app: Final[FastAPI] = create_app()
