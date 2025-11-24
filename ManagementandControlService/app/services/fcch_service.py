from __future__ import annotations

import logging
from typing import Dict, List, Optional

from ..models.config_models import FCCHOpcode
from ..models.fcch import FCCHMessage

logger = logging.getLogger(__name__)


class FCCHService:
    """Stubbed handler for Fast Control Channel messaging."""

    def __init__(self) -> None:
        self._buffer: List[FCCHMessage] = []

    # PUBLIC_INTERFACE
    def send(self, message: FCCHMessage) -> None:
        """Accept a message for FCCH; in production this would serialize and send via PHY."""
        logger.debug("FCCH SEND %s", message.opcode)
        self._buffer.append(message)

    # PUBLIC_INTERFACE
    def peek(self, limit: int = 10) -> List[FCCHMessage]:
        """Return recent messages without removing them."""
        return list(self._buffer[-limit:])

    # PUBLIC_INTERFACE
    def clear(self) -> int:
        """Clear message buffer; returns number cleared."""
        n = len(self._buffer)
        self._buffer.clear()
        return n


_fcch_singleton: Optional[FCCHService] = None


# PUBLIC_INTERFACE
def get_fcch_service() -> FCCHService:
    """FastAPI dependency provider for FCCHService singleton."""
    global _fcch_singleton
    if _fcch_singleton is None:
        _fcch_singleton = FCCHService()
    return _fcch_singleton
