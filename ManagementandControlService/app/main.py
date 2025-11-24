from __future__ import annotations

import logging
import os
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseSettings, Field

# Configure basic logging for the service
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("ManagementandControlService")


class Settings(BaseSettings):
    """
    Service configuration settings.

    Values are loaded from environment variables and an optional .env file
    located at the project root or this service directory.
    """

    SERVICE_NAME: str = Field("ManagementandControlService", description="Service name")
    ENVIRONMENT: str = Field("development", description="Runtime environment")
    VERSION: str = Field("0.1.0", description="Service version")
    PORT: int = Field(5000, description="Default port to run the service")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate settings once; FastAPI will reuse this instance
settings = Settings()

# FastAPI application instance with basic metadata
app = FastAPI(
    title="Management and Control Service",
    description=(
        "Provides management, configuration, control functions, telemetry, and "
        "real-time streaming for the OCT system per SDA OCT Standard v4.0.0."
    ),
    version=settings.VERSION,
    openapi_tags=[
        {"name": "health", "description": "Service health and readiness checks"},
        {"name": "meta", "description": "Service metadata and version information"},
    ],
)


# PUBLIC_INTERFACE
@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Returns HTTP 200 with simple status information if the service is healthy.",
    response_model=Dict[str, str],
)
def health() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        JSON object containing status and service name.
    """
    logger.debug("Health check requested")
    return {"status": "ok", "service": settings.SERVICE_NAME}


# PUBLIC_INTERFACE
@app.get(
    "/version",
    tags=["meta"],
    summary="Service version",
    description="Returns the current version and environment for the service.",
    response_model=Dict[str, str],
)
def version() -> Dict[str, str]:
    """
    Version endpoint.

    Returns:
        JSON object containing version and environment.
    """
    logger.debug("Version requested")
    return {"version": settings.VERSION, "environment": settings.ENVIRONMENT}
