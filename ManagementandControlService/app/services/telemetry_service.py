from __future__ import annotations

import logging
from datetime import datetime
from typing import Callable, List, Optional

from ..models.config_models import LinkQuality, LinkState, TelemetrySnapshot, PVTRData, TWTTData, ETWTTEntry

logger = logging.getLogger(__name__)

Subscriber = Callable[[TelemetrySnapshot], None]


class TelemetryService:
    """
    Aggregates latest telemetry and notifies subscribers.

    Production systems should push high-rate data to a DB/stream and throttle notifications.
    """

    def __init__(self) -> None:
        self._latest: Optional[TelemetrySnapshot] = None
        self._subscribers: List[Subscriber] = []

    # PUBLIC_INTERFACE
    def get_latest(self) -> Optional[TelemetrySnapshot]:
        """Return latest telemetry snapshot if available."""
        return self._latest

    # PUBLIC_INTERFACE
    def update(
        self,
        state: LinkState,
        link_quality: LinkQuality,
        pvtr: Optional[PVTRData] = None,
        twtt: Optional[TWTTData] = None,
        etwtt: Optional[List[ETWTTEntry]] = None,
    ) -> TelemetrySnapshot:
        """Update the latest telemetry and notify subscribers."""
        snap = TelemetrySnapshot(
            state=state,
            timestamp=datetime.utcnow(),
            linkQuality=link_quality,
            PVTR=pvtr,
            TWTT=twtt,
            eTWTT=etwtt,
        )
        self._latest = snap
        self._notify(snap)
        return snap

    def subscribe(self, fn: Subscriber) -> None:
        """Subscribe to telemetry updates (used by WebSocket broadcaster)."""
        self._subscribers.append(fn)

    def _notify(self, snap: TelemetrySnapshot) -> None:
        for fn in list(self._subscribers):
            try:
                fn(snap)
            except Exception as exc:  # defensive
                logger.error("Telemetry subscriber error: %s", exc, exc_info=False)


_telemetry_singleton: Optional[TelemetryService] = None


# PUBLIC_INTERFACE
def get_telemetry_service() -> TelemetryService:
    """FastAPI dependency provider for TelemetryService singleton."""
    global _telemetry_singleton
    if _telemetry_singleton is None:
        _telemetry_singleton = TelemetryService()
    return _telemetry_singleton
