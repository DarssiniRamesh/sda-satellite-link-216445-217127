from __future__ import annotations

from typing import Dict, List, Tuple

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..models.config_models import ETWTTEntry, TWTTData
from ..models.twtt import ETWTTRequest, TWTTRequest
from ..services.timing_service import TimingService, get_timing_service

router = APIRouter(prefix="/twtt", tags=["timing"])


class TWTTResponse(BaseModel):
    data: TWTTData


class ETWTTResponse(BaseModel):
    avg_rms_err: int
    segments_count: int


@router.post(
    "",
    summary="Compute TWTT from tx/rx timestamps",
    response_model=TWTTResponse,
)
# PUBLIC_INTERFACE
def compute_twtt_api(req: TWTTRequest, svc: TimingService = Depends(get_timing_service)) -> TWTTResponse:
    """Compute TWTT structure from timestamps."""
    data = svc.compute_twtt(req.tx_timestamp_ns, req.rx_timestamp_ns)
    return TWTTResponse(data=data)


@router.post(
    "/etwtt",
    summary="Aggregate eTWTT segments",
    response_model=ETWTTResponse,
)
# PUBLIC_INTERFACE
def compute_etwtt_api(req: ETWTTRequest, svc: TimingService = Depends(get_timing_service)) -> ETWTTResponse:
    """Aggregate eTWTT entries into simple metrics."""
    avg, count = svc.compute_etwtt(req.segments)
    return ETWTTResponse(avg_rms_err=avg, segments_count=count)
