from __future__ import annotations

from typing import Optional

from ..models.mgmt_frames import FrameCodecRegistry, MGMTFrame


class MGMTRegistryService:
    """Thin wrapper around codec registry for DI compatibility."""

    def __init__(self) -> None:
        self._registry = FrameCodecRegistry()

    # PUBLIC_INTERFACE
    def encode(self, frame: MGMTFrame) -> bytes:
        """Encode MGMT frame to bytes."""
        return self._registry.encode(frame)

    # PUBLIC_INTERFACE
    def decode(self, data: bytes) -> MGMTFrame:
        """Decode bytes into MGMT frame."""
        return self._registry.decode(data)


_mgmt_singleton: Optional[MGMTRegistryService] = None


# PUBLIC_INTERFACE
def get_mgmt_service() -> MGMTRegistryService:
    """FastAPI dependency provider for MGMTRegistryService singleton."""
    global _mgmt_singleton
    if _mgmt_singleton is None:
        _mgmt_singleton = MGMTRegistryService()
    return _mgmt_singleton
