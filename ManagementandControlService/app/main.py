import asyncio
import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .routers import config as config_router
from .routers import telemetry as telemetry_router
from .routers import fcch as fcch_router
from .routers import mgmt as mgmt_router
from .routers import timing as timing_router
from .routers import updates as updates_router
from .services.telemetry_service import get_telemetry_service
from .models.config_models import LinkQuality, LinkState

logger = logging.getLogger(__name__)


# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application for the Management and Control Service.

    Returns:
        FastAPI: The configured FastAPI app instance with OpenAPI metadata and routes registered.
    """
    app = FastAPI(
        title="Management and Control Service",
        description=(
            "Provides management, configuration, control, and telemetry interfaces for the Optical Communications Terminal (OCT) "
            "system in compliance with SDA OCT Standard v4.0.0. Includes REST endpoints and WebSocket interfaces."
        ),
        version="0.2.0",
        openapi_tags=[
            {"name": "health", "description": "Service health and readiness endpoints."},
            {"name": "config", "description": "Configuration management (versioning, rollback)."},
            {"name": "telemetry", "description": "Telemetry aggregation and streaming."},
            {"name": "fcch", "description": "Fast Control Channel signaling stubs."},
            {"name": "mgmt", "description": "MGMT frame encode/decode registry endpoints."},
            {"name": "timing", "description": "TWTT and eTWTT computation helpers."},
            {"name": "updates", "description": "On-orbit reprogrammability stubs and status."},
        ],
    )

    # Register routers
    app.include_router(config_router.router)
    app.include_router(telemetry_router.router)
    app.include_router(fcch_router.router)
    app.include_router(mgmt_router.router)
    app.include_router(timing_router.router)
    app.include_router(updates_router.router)

    @app.get(
        "/health",
        tags=["health"],
        summary="Health check",
        description="Returns service health status and basic metadata.",
        responses={
            200: {
                "description": "Service is healthy.",
                "content": {
                    "application/json": {
                        "example": {
                            "status": "ok",
                            "service": "ManagementandControlService",
                            "version": "0.2.0",
                        }
                    }
                },
            }
        },
    )
    # PUBLIC_INTERFACE
    def health() -> JSONResponse:
        """
        Health check endpoint for the Management and Control Service.

        Returns:
            JSONResponse: JSON object indicating the service health and version.
        """
        payload = {
            "status": "ok",
            "service": "ManagementandControlService",
            "version": "0.2.0",
        }
        return JSONResponse(content=payload, status_code=200)

    # PUBLIC_INTERFACE
    def websocket_usage_note() -> str:
        """
        Provides a short note about WebSocket usage for real-time telemetry.

        Returns:
            str: A message directing users to WebSocket documentation.
        """
        return "Real-time telemetry and update status via: /telemetry/ws (JSON snapshots)."

    @app.get(
        "/ws-docs",
        tags=["health"],
        summary="WebSocket usage help",
        description="Project-level note for real-time WebSocket connection info.",
        responses={200: {"description": "Usage note returned."}},
    )
    # PUBLIC_INTERFACE
    def get_ws_docs() -> JSONResponse:
        """
        Route providing guidance on WebSocket usage and documentation location.

        Returns:
            JSONResponse: A note for how to discover WebSocket endpoints when available.
        """
        return JSONResponse(content={"note": websocket_usage_note()}, status_code=200)

    # Seed a minimal periodic telemetry update to demonstrate WS streaming (optional)
    async def seed_telemetry() -> None:
        svc = get_telemetry_service()
        q = 0.0
        while True:
            # create a changing BLER and RSSI for demo; values within bounds
            q = (q + 0.05) % 1.0
            lq = LinkQuality(bler=q, rssi=-60.0 + q * 5.0, sync_status="SYNCED", frame_loss=q * 0.1)
            svc.update(LinkState.linked if q < 0.9 else LinkState.degraded, lq)
            await asyncio.sleep(0.5)

    @app.on_event("startup")
    async def _startup() -> None:
        try:
            asyncio.create_task(seed_telemetry())
        except Exception:  # pragma: no cover
            logger.warning("Failed to start telemetry seed task")

    return app


# The ASGI application instance used by uvicorn: `uvicorn app.main:app`
app = create_app()
