from __future__ import annotations

from typing import Dict, Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os


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

    # Log OpenAPI/docs URLs on startup for discoverability in preview/local environments
    logger = logging.getLogger(__name__)

    @application.on_event("startup")
    async def _log_docs_urls() -> None:
        port = os.getenv("PORT") or "3000"
        host = "0.0.0.0"
        try:
            # Validate port to avoid logging garbage
            p = int(port)
            if not (1 <= p <= 65535):
                port = "3000"
        except ValueError:
            port = "3000"
        logger.info("Management and Control Service started")
        logger.info("Swagger UI: http://%s:%s/docs", host, port)
        logger.info("OpenAPI JSON: http://%s:%s/openapi.json", host, port)

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
