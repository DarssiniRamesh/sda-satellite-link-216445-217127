from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from ..models.config_models import FCCHOpcode
from ..models.fcch import FCCHLinkQualityPayload, FCCHMessage
from ..services.fcch_service import FCCHService, get_fcch_service

router = APIRouter(prefix="/fcch", tags=["fcch"])


class FCCHSendRequest(FCCHMessage):  # reuse fields; message is already serializable
    pass


@router.post(
    "/send",
    summary="Send FCCH message",
    response_model=dict,
)
# PUBLIC_INTERFACE
def fcch_send(req: FCCHSendRequest, svc: FCCHService = Depends(get_fcch_service)) -> dict:
    """Accept an FCCH message for transmission (stub)."""
    svc.send(req)
    return {"status": "queued"}


@router.get(
    "/peek",
    summary="Peek recent FCCH messages",
    response_model=List[FCCHMessage],
)
# PUBLIC_INTERFACE
def fcch_peek(limit: int = 10, svc: FCCHService = Depends(get_fcch_service)) -> List[FCCHMessage]:
    """Return recent FCCH messages stored in memory (debug)."""
    return svc.peek(limit=limit)
