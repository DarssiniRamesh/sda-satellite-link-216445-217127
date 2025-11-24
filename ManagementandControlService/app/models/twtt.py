from __future__ import annotations

from typing import List, Tuple

from pydantic import BaseModel, Field

from .config_models import ETWTTEntry, TWTTData


class TWTTRequest(BaseModel):
    tx_timestamp_ns: int = Field(..., ge=0)
    rx_timestamp_ns: int = Field(..., ge=0)


class ETWTTRequest(BaseModel):
    segments: List[ETWTTEntry] = Field(default_factory=list)


def compute_twtt(tx_ns: int, rx_ns: int) -> TWTTData:
    """Compute round-trip and one-way delay assuming symmetric path.

    Requirements:
    - REQ-MGMT-TWTT: validate timestamp ordering (rx >= tx) and compute deltas.
    """
    if rx_ns < tx_ns:
        raise ValueError("REQ-MGMT-TWTT: rx_timestamp_ns must be >= tx_timestamp_ns")
    rtt = rx_ns - tx_ns
    return TWTTData(tx_timestamp_ns=tx_ns, rx_timestamp_ns=rx_ns, round_trip_time_ns=rtt, one_way_delay_ns=rtt // 2)


def compute_etwtt_stats(entries: List[ETWTTEntry]) -> Tuple[int, int]:
    """Return (avg_rms_err, segments_count) as a simple aggregate metric."""
    if not entries:
        return 0, 0
    total = sum(int(e.rms_err) for e in entries)
    return total // len(entries), len(entries)
