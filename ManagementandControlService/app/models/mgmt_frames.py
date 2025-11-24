from __future__ import annotations

"""
Lightweight management frame primitives and a basic codec registry.

Exports:
- MGMTFrameType: Enum of frame categories.
- MGMTFrame: Dataclass container for a management frame (not a Pydantic model).
- FrameCodecRegistry: Simple encoder/decoder registry for demo purposes.

Note: This module intentionally avoids embedding operational logic within Pydantic models.
"""

import enum
from dataclasses import dataclass
from typing import Any, Dict, Protocol
from ast import literal_eval

# Explicit re-exports for import clarity
__all__ = [
    "MGMTFrameType",
    "MGMTFrame",
    "FrameCodecRegistry",
]


class MGMTFrameType(str, enum.Enum):
    """Enumeration of management frame types."""
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
    """Protocol for encoder implementations."""
    def encode(self, frame: MGMTFrame) -> bytes: ...


class Decoder(Protocol):
    """Protocol for decoder implementations."""
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
    """Decoder counterpart to BasicEncoder with minimal validation and safe parsing."""
    def decode(self, raw: bytes) -> MGMTFrame:
        # Reverse of BasicEncoder; minimal validation.
        parts = raw.split(b"|", 3)
        if len(parts) != 4:
            raise ValueError("Invalid frame format.")
        ft = MGMTFrameType(parts[0].decode("utf-8"))
        # Defensive parsing and bounds check
        try:
            header_len = int(parts[1].decode("utf-8"))
            if header_len < 0:
                raise ValueError("Negative header length.")
        except Exception as exc:
            raise ValueError("Invalid header length.") from exc

        header_bytes = parts[2][:header_len]
        payload = parts[3]

        # safe parsing of repr'd dict (literal_eval is safer than eval/exec)
        try:
            header_obj = literal_eval(header_bytes.decode("utf-8")) if header_bytes else {}
            header = header_obj if isinstance(header_obj, dict) else {}
        except Exception:
            header = {}

        return MGMTFrame(frame_type=ft, header=header, payload=payload)


class FrameCodecRegistry:
    """Registry to map frame types or protocol versions to encoder/decoder."""
    def __init__(self) -> None:
        self._encoder: Encoder = BasicEncoder()
        self._decoder: Decoder = BasicDecoder()

    # PUBLIC_INTERFACE
    def encode(self, frame: MGMTFrame) -> bytes:
        """Encode a management frame into raw bytes using the active encoder."""
        return self._encoder.encode(frame)

    # PUBLIC_INTERFACE
    def decode(self, data: bytes) -> MGMTFrame:
        """Decode raw bytes into a management frame using the active decoder."""
        return self._decoder.decode(data)
