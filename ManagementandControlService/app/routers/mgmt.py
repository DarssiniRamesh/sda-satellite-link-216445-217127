from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

# Import only existing exports from mgmt_frames
from ..models.mgmt_frames import MGMTFrame, MGMTFrameType
from ..services.mgmt_registry import MGMTRegistryService, get_mgmt_service

router = APIRouter(prefix="/mgmt", tags=["mgmt"])


class EncodeRequest(BaseModel):
    """Request body for encoding a management frame."""
    frame_type: MGMTFrameType
    header: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary header map.")
    payload_hex: str = Field(default="", description="Hex-encoded payload bytes.")


class EncodeResponse(BaseModel):
    """Response containing the encoded frame as hex."""
    frame_hex: str


class DecodeRequest(BaseModel):
    """Request body containing a hex-encoded frame for decoding."""
    frame_hex: str


class DecodeResponse(BaseModel):
    """Decoded frame fields."""
    frame_type: MGMTFrameType
    header: Dict[str, Any]
    payload_hex: str


@router.post(
    "/encode",
    summary="Encode MGMT frame",
    description="Encode a management frame into bytes using the codec registry and return as a hex string.",
    response_model=EncodeResponse,
)
# PUBLIC_INTERFACE
def encode_frame(req: EncodeRequest, reg: MGMTRegistryService = Depends(get_mgmt_service)) -> EncodeResponse:
    """Encode a management frame to a hex string using the codec registry."""
    try:
        payload = bytes.fromhex(req.payload_hex) if req.payload_hex else b""
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload hex") from exc
    # Use MGMTFrame (correct existing type) not nonexistent 'MGMT'
    frame = MGMTFrame(frame_type=req.frame_type, header=req.header, payload=payload)
    raw = reg.encode(frame)
    return EncodeResponse(frame_hex=raw.hex())


@router.post(
    "/decode",
    summary="Decode MGMT frame",
    description="Decode a hex-encoded management frame using the codec registry and return its fields.",
    response_model=DecodeResponse,
)
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
