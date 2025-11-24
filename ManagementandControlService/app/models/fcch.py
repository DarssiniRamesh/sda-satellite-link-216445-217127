from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from .config_models import FCCHOpcode, LinkQuality


class FCCHMessage(BaseModel):
    """Compact Fast Control Channel message envelope."""
    opcode: FCCHOpcode
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FCCHLinkQualityPayload(BaseModel):
    """Payload used with LINK_QUALITY opcode."""
    link_quality: LinkQuality
    note: Optional[str] = None
