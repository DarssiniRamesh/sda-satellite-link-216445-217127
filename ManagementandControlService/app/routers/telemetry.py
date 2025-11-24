from __future__ import annotations

import asyncio
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status

from ..models.config_models import ErrorResponse, TelemetrySnapshot
from ..services.telemetry_service import TelemetryService, get_telemetry_service
from ..services.ws_state import WSState, get_ws_state

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.get(
    "",
    summary="Get telemetry data",
    response_model=TelemetrySnapshot,
    responses={404: {"model": ErrorResponse}},
)
# PUBLIC_INTERFACE
def get_telemetry(svc: TelemetryService = Depends(get_telemetry_service)) -> TelemetrySnapshot:
    """Return latest telemetry snapshot if available."""
    snap = svc.get_latest()
    if not snap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No telemetry available")
    return snap


@router.websocket(
    "/ws",
)
# PUBLIC_INTERFACE
async def telemetry_ws(
    websocket: WebSocket,
    svc: TelemetryService = Depends(get_telemetry_service),
    state: WSState = Depends(get_ws_state),
) -> None:
    """
    WebSocket endpoint streaming telemetry snapshots in real-time.

    OperationId: telemetry_ws
    Usage: connect and receive JSON-serialized snapshot messages when updated.
    """
    await state.connect(websocket)

    # Bridge telemetry updates to WS
    def push(snapshot: TelemetrySnapshot) -> None:
        # Fire and forget, ensure no blocking in subscriber thread
        asyncio.create_task(state.broadcast_obj(snapshot.model_dump()))

    svc.subscribe(push)

    try:
        # Keep connection open; echo pings to keepalive
        while True:
            # Receive optional client messages (no-op)
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        await state.disconnect(websocket)
