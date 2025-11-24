from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any, Dict, Protocol

# Explicit re-exports for import clarity
__all__ = [
    "MGMTFrameType",
    "MGMTFrame",
    "FrameCodecRegistry",
]


class MGMTFrameType(str, enum.Enum):
    IDLE = "IDLE"
    DATA = "DATA"
    MGMT = "MGMT"


@dataclass
class MGMTFrame:
    """Simple management frame container (stub).

    Dataclass is used intentionally for a lightweight container that is not part of Pydantic models.
    This type is not exposed directly in OpenAPI; routers convert to/from hex strings.
    """
    frame_type: MGMTFrameType
    header: Dict[str, Any]
    payload: bytes


class Encoder(Protocol):
    def encode(self, frame: MGMTFrame) -> bytes: ...


class Decoder(Protocol):
    def decode(self, raw: bytes) -> MGMTFrame: ...


class BasicEncoder:
    """Naive encoder for demonstration; DO NOT use for production."""
    def encode(self, frame: MGMTFrame) -> bytes:
        # Very simple format: type|len(header)|header(json-ish repr)|payload
        header_repr = repr(frame.header).encode("utf-8")
        return b"|".join(
            [
                frame.frame_type.value.encode("utf-8"),
                str(len(header_repr)).encode("utf-8"),
                header_repr,
                frame.payload,
            ]
        )


class BasicDecoder:
    def decode(self, raw: bytes) -> MGMTFrame:
        # Reverse of BasicEncoder; minimal validation.
        parts = raw.split(b"|", 3)
        if len(parts) != 4:
            raise ValueError("Invalid frame format.")
        ft = MGMTFrameType(parts[0].decode("utf-8"))
        header_len = int(parts[1].decode("utf-8"))
        header_bytes = parts[2][:header_len]
        payload = parts[3]
        # safe parsing of repr'd dict
        from ast import literal_eval
        try:
            header = literal_eval(header_bytes.decode("utf-8"))
            if not isinstance(header, dict):
                header = {}
        except Exception:
            header = {}
        return MGMTFrame(frame_type=ft, header=header, payload=payload)


class FrameCodecRegistry:
    """Registry to map frame types or protocol versions to encoder/decoder."""
    def __init__(self) -> None:
        self._encoder: Encoder = BasicEncoder()
        self._decoder: Decoder = BasicDecoder()

    def encode(self, frame: MGMTFrame) -> bytes:
        return self._encoder.encode(frame)

    def decode(self, data: bytes) -> MGMTFrame:
        return self._decoder.decode(data)
