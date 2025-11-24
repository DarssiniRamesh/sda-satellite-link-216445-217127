from __future__ import annotations

from typing import Optional

# Import only valid, exported symbols from mgmt_frames
from ..models.mgmt_frames import FrameCodecRegistry, MGMTFrame


class MGMTRegistryService:
    """Thin wrapper around codec registry for DI compatibility."""

    def __init__(self) -> None:
        self._registry = FrameCodecRegistry()

    # PUBLIC_INTERFACE
    def encode(self, frame: MGMTFrame) -> bytes:
        """Encode MGMT frame to bytes.

        Args:
            frame: The management frame to encode.

        Returns:
            bytes: The raw encoded bytes.
        """
        return self._registry.encode(frame)

    # PUBLIC_INTERFACE
    def decode(self, data: bytes) -> MGMTFrame:
        """Decode bytes into MGMT frame.

        Args:
            data: The raw frame bytes to decode.

        Returns:
            MGMTFrame: The decoded frame.
        """
        return self._registry.decode(data)


_mgmt_singleton: Optional[MGMTRegistryService] = None


# PUBLIC_INTERFACE
def get_mgmt_service() -> MGMTRegistryService:
    """FastAPI dependency provider for MGMTRegistryService singleton."""
    global _mgmt_singleton
    if _mgmt_singleton is None:
        _mgmt_singleton = MGMTRegistryService()
    return _mgmt_singleton
