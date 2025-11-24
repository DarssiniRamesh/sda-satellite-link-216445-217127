from __future__ import annotations

from typing import List, Optional, Tuple

from ..models.config_models import ETWTTEntry, TWTTData
from ..models.twtt import compute_etwtt_stats, compute_twtt


class TimingService:
    """Computations related to TWTT and eTWTT."""

    # PUBLIC_INTERFACE
    def compute_twtt(self, tx_ns: int, rx_ns: int) -> TWTTData:
        """Compute TWTT structure from tx/rx timestamps."""
        return compute_twtt(tx_ns, rx_ns)

    # PUBLIC_INTERFACE
    def compute_etwtt(self, entries: List[ETWTTEntry]) -> Tuple[int, int]:
        """Return (avg_rms_err, segments_count)."""
        return compute_etwtt_stats(entries)


_timing_singleton: Optional[TimingService] = None


# PUBLIC_INTERFACE
def get_timing_service() -> TimingService:
    """FastAPI dependency provider for TimingService singleton."""
    global _timing_singleton
    if _timing_singleton is None:
        _timing_singleton = TimingService()
    return _timing_singleton
