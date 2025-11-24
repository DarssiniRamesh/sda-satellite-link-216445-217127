"""
Service layer package for Management and Control Service.

Contains:
- ConfigStore: in-memory versioned configuration with rollback
- TelemetryService: aggregate latest telemetry and allow subscription hooks
- FCCHService: stub for fast control channel signaling
- FrameCodecRegistry: singleton codec registry for MGMT frames
- TimingService: helpers for TWTT/eTWTT computations
- WSState: simple publish/subscribe for WebSocket broadcasting
"""
