from __future__ import annotations

import enum
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field, PositiveInt, field_validator, model_validator


class AcquisitionMode(str, enum.Enum):
    beaconless = "beaconless"
    cooperative = "cooperative"


class OperationalMode(str, enum.Enum):
    standby = "standby"
    setup = "setup"
    acquisition = "acquisition"
    fine_acquisition = "fine_acquisition"
    communication = "communication"
    stop = "stop"
    prepare = "prepare"


class StateMachine(str, enum.Enum):
    pat = "pat"


class UpdateType(str, enum.Enum):
    software = "software"
    firmware = "firmware"
    protocol = "protocol"


class FCCHOpcode(str, enum.Enum):
    # Minimal stub opcodes for Fast Control Channel signaling
    NOP = "NOP"
    LINK_QUALITY = "LINK_QUALITY"
    ENTER_SAFE = "ENTER_SAFE"
    EXIT_SAFE = "EXIT_SAFE"
    HEARTBEAT = "HEARTBEAT"


class LinkState(str, enum.Enum):
    unsynced = "unsynced"
    acquiring = "acquiring"
    aligned = "aligned"
    linked = "linked"
    degraded = "degraded"
    fault = "fault"


class LinkQuality(BaseModel):
    """Link quality snapshot used in telemetry and FCCH reporting."""
    bler: float = Field(..., ge=0.0, le=1.0, description="Block Error Rate [0..1].")
    rssi: float = Field(..., description="Received Signal Strength Indicator (dBm or arb. units).")
    sync_status: str = Field(..., description="Synchronization status string, e.g., SYNCED/UNSYNCED.")
    frame_loss: float = Field(0.0, ge=0.0, le=1.0, description="Frame loss rate [0..1].")
    irradiance: Optional[float] = Field(None, description="Optional irradiance measure.")


class TWTTData(BaseModel):
    """Two-Way Time Transfer basic structure."""
    tx_timestamp_ns: int = Field(..., ge=0)
    rx_timestamp_ns: int = Field(..., ge=0)
    round_trip_time_ns: int = Field(..., ge=0)
    one_way_delay_ns: int = Field(..., ge=0)


class ETWTTEntry(BaseModel):
    """Enhanced TWTT segmented data entry."""
    segment_id: PositiveInt
    tx_tod_seconds: int = Field(..., ge=0, le=86400, description="Seconds of day [0..86400].")
    tx_ts: int = Field(..., ge=0, description="TX timestamp [ns].")
    tx_interval: int = Field(..., ge=0, description="Interval [ns].")
    pdelay_start: int = Field(..., ge=0)
    pdelay_dev: int = Field(..., ge=0)
    rms_err: int = Field(..., ge=0)


class PVTRData(BaseModel):
    """Position, Velocity, Time, Rotation data placeholder for telemetry."""
    sc_position_velocity: Dict[str, Any] = Field(default_factory=dict)
    sc_attitude_quaternion: Dict[str, Any] = Field(default_factory=dict)
    sc_to_oct_translation: Dict[str, Any] = Field(default_factory=dict)
    sc_to_oct_rotation_quaternion: Dict[str, Any] = Field(default_factory=dict)
    oct_los_unit_vector: Dict[str, Any] = Field(default_factory=dict)
    oct_lever_arm_vector: Dict[str, Any] = Field(default_factory=dict)
    timestamp: Optional[datetime] = None


class ConfigurationParameters(BaseModel):
    """Arbitrary parameters map; validate key constraints here if needed."""
    acquisition_time_s: Optional[float] = Field(
        None, ge=0.0, le=100.0, description="PAT acquisition time in seconds (≤ 100 s per acceptance note)."
    )
    tx_latency_ms: Optional[float] = Field(
        None, ge=0.0, le=15.0, description="Transmit latency ms (≤ 15 ms per acceptance note)."
    )
    rx_latency_ms: Optional[float] = Field(
        None, ge=0.0, le=15.0, description="Receive latency ms (≤ 15 ms per acceptance note)."
    )
    # Additional parameters allowed
    other: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_latency_bounds(self) -> "ConfigurationParameters":
        # Acceptance: ≤ 15 ms each
        if self.tx_latency_ms is not None and self.tx_latency_ms > 15.0:
            raise ValueError("tx_latency_ms exceeds 15 ms acceptance bound.")
        if self.rx_latency_ms is not None and self.rx_latency_ms > 15.0:
            raise ValueError("rx_latency_ms exceeds 15 ms acceptance bound.")
        # Acceptance: acquisition ≤ 100 s
        if self.acquisition_time_s is not None and self.acquisition_time_s > 100.0:
            raise ValueError("acquisition_time_s exceeds 100 s acceptance bound.")
        return self


class Configuration(BaseModel):
    """Top-level Configuration schema."""
    stateMachine: StateMachine = Field(..., description="State machine identifier (e.g., PAT).")
    acquisitionMode: AcquisitionMode = Field(..., description="Acquisition mode.")
    operationalMode: OperationalMode = Field(..., description="Operational mode.")
    parameters: ConfigurationParameters = Field(default_factory=ConfigurationParameters)

    @field_validator("operationalMode")
    @classmethod
    def validate_operational(cls, v: OperationalMode) -> OperationalMode:
        # Placeholder for cross-field validation if needed
        return v


class ConfigurationVersion(BaseModel):
    version: str = Field(..., description="Version identifier (monotonic increasing by service).")
    applied_at: datetime = Field(..., description="UTC timestamp of application.")
    config: Configuration


class ConfigurationHistory(BaseModel):
    versions: List[ConfigurationVersion] = Field(default_factory=list)
    current_version: Optional[str] = None


class TelemetrySnapshot(BaseModel):
    state: LinkState = Field(..., description="High-level link state.")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    linkQuality: LinkQuality = Field(..., description="Aggregated link quality.")
    PVTR: Optional[PVTRData] = None
    TWTT: Optional[TWTTData] = None
    eTWTT: Optional[List[ETWTTEntry]] = None


class Status(BaseModel):
    systemStatus: str = Field(..., description="System status (healthy/degraded/fault).")
    details: Dict[str, Any] = Field(default_factory=dict)


class Command(BaseModel):
    action: str = Field(..., min_length=1)
    parameters: Dict[str, Any] = Field(default_factory=dict)


class Update(BaseModel):
    type: UpdateType
    version: str = Field(..., min_length=1)
    payload_b64: Optional[str] = Field(
        None, description="Base64-encoded payload, kept optional for stub. Use chunked upload in production."
    )


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None


# Utility types
ConfigKV = Tuple[str, Configuration]
