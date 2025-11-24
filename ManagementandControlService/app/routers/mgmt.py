from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ..models.mgmt_frames import MGMTFrame, MGMTFrameType
from ..services.mgmt_registry import MGMTRegistryService, get_mgmt_service

router = APIRouter(prefix="/mgmt", tags=["mgmt"])


class EncodeRequest(BaseModel):
    frame_type: MGMTFrameType
    header: Dict[str, Any] = Field(default_factory=dict)
    payload_hex: str = Field(default="")


class EncodeResponse(BaseModel):
    frame_hex: str


class DecodeRequest(BaseModel):
    frame_hex: str


class DecodeResponse(BaseModel):
    frame_type: MGMTFrameType
    header: Dict[str, Any]
    payload_hex: str


@router.post("/encode", summary="Encode MGMT frame", response_model=EncodeResponse)
# PUBLIC_INTERFACE
def encode_frame(req: EncodeRequest, reg: MGMTRegistryService = Depends(get_mgmt_service)) -> EncodeResponse:
    """Encode a management frame to a hex string using the codec registry."""
    try:
        payload = bytes.fromhex(req.payload_hex) if req.payload_hex else b""
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload hex") from exc
    frame = MGMTFrame(frame_type=req.frame_type, header=req.header, payload=payload)
    raw = reg.encode(frame)
    return EncodeResponse(frame_hex=raw.hex())


@router.post("/decode", summary="Decode MGMT frame", response_model=DecodeResponse)
# PUBLIC_INTERFACE
def decode_frame(req: DecodeRequest, reg: MGMTRegistryService = Depends(get_mgmt_service)) -> DecodeResponse:
    """Decode a hex-encoded management frame using the codec registry."""
    try:
        raw = bytes.fromhex(req.frame_hex)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid frame hex") from exc
    try:
        frame = reg.decode(raw)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Decode error: {exc}") from exc
    return DecodeResponse(frame_type=frame.frame_type, header=frame.header, payload_hex=frame.payload.hex())
