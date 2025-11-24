from fastapi import FastAPI
from fastapi.responses import JSONResponse

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
        version="0.1.0",
        openapi_tags=[
            {"name": "health", "description": "Service health and readiness endpoints."},
        ],
    )

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
                            "version": "0.1.0",
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
            "version": "0.1.0",
        }
        return JSONResponse(content=payload, status_code=200)

    # PUBLIC_INTERFACE
    def websocket_usage_note() -> str:
        """
        Provides a short note about WebSocket usage for future real-time telemetry.

        Returns:
            str: A message directing users to future WebSocket documentation.
        """
        return "WebSocket endpoints will be documented in /docs and /openapi.json when added."

    @app.get(
        "/ws-docs",
        tags=["health"],
        summary="WebSocket usage help",
        description="Project-level note for real-time WebSocket connection info. Placeholder until WebSocket endpoints are implemented.",
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

    return app


# The ASGI application instance used by uvicorn: `uvicorn app.main:app`
app = create_app()
