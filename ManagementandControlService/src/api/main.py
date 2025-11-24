from __future__ import annotations

from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    application = FastAPI(
        title="Management and Control Service",
        description="FastAPI app providing management, control, and telemetry interfaces.",
        version="0.1.0",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/", summary="Health Check", tags=["Health"])
    def health_check() -> Dict[str, str]:
        """Simple health check endpoint."""
        return {"message": "Healthy"}

    return application


# Expose `app` at module level for ASGI servers and imports.
app: FastAPI = create_app()
