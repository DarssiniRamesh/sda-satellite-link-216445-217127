from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..models.config_models import ErrorResponse, Update
from ..services.ws_state import WSState, get_ws_state

router = APIRouter(prefix="/updates", tags=["updates"])


class UpdateAck(BaseModel):
    accepted: bool
    requested_version: str
    message: str


@router.post(
    "",
    summary="Initiate software/firmware update",
    response_model=UpdateAck,
    responses={400: {"model": ErrorResponse}},
)
# PUBLIC_INTERFACE
async def initiate_update(req: Update, ws: WSState = Depends(get_ws_state)) -> UpdateAck:
    """
    Accept an update request and broadcast state transitions on WebSocket.

    Note: This is a stub. Real implementation must stream signed packages,
    verify via cryptographic signatures, and apply with rollback safeguards.
    """
    if not req.version:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="version required")

    # Broadcast a simple lifecycle over WS without blocking the response.
    async def lifecycle() -> None:
        stages = ["accepted", "downloading", "verifying", "applying", "restarting", "completed"]
        for stage in stages:
            await ws.broadcast_obj(
                {
                    "type": "update_status",
                    "stage": stage,
                    "updateType": req.type.value,
                    "targetVersion": req.version,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            )
            await asyncio.sleep(0.05)

    asyncio.create_task(lifecycle())
    return UpdateAck(accepted=True, requested_version=req.version, message="Update initiated")
