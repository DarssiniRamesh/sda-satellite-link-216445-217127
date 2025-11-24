from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ..models.config_models import Configuration, ConfigurationHistory, ConfigurationVersion, ErrorResponse
from ..services.config_store import ConfigStore, get_config_store

router = APIRouter(prefix="/config", tags=["config"])


class RollbackRequest(BaseModel):
    version: str = Field(..., min_length=2)


@router.get(
    "",
    summary="Get current configuration",
    response_model=Configuration,
    responses={404: {"model": ErrorResponse, "description": "No configuration set."}},
)
# PUBLIC_INTERFACE
def get_config(store: ConfigStore = Depends(get_config_store)) -> Configuration:
    """Return the current configuration."""
    cfg = store.get_current()
    if not cfg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No configuration set")
    return cfg


@router.post(
    "",
    summary="Update configuration",
    response_model=ConfigurationVersion,
    responses={400: {"model": ErrorResponse}},
)
# PUBLIC_INTERFACE
def set_config(payload: Configuration, store: ConfigStore = Depends(get_config_store)) -> ConfigurationVersion:
    """Update configuration with validation bounds enforced by schema."""
    return store.set_config(payload)


@router.get(
    "/history",
    summary="Get configuration history",
    response_model=ConfigurationHistory,
)
# PUBLIC_INTERFACE
def get_history(store: ConfigStore = Depends(get_config_store)) -> ConfigurationHistory:
    """Return version history and current version."""
    return store.history()


@router.post(
    "/rollback",
    summary="Rollback to a previous version",
    response_model=ConfigurationVersion,
    responses={404: {"model": ErrorResponse}},
)
# PUBLIC_INTERFACE
def rollback(req: RollbackRequest, store: ConfigStore = Depends(get_config_store)) -> ConfigurationVersion:
    """Rollback configuration to a previous version."""
    try:
        return store.rollback(req.version)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
